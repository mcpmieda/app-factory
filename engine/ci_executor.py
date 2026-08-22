from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

ALLOWED_PACKAGE_SCRIPTS = (
    "format:check",
    "lint",
    "typecheck",
    "check",
    "test",
    "test:coverage",
    "test:visual",
    "build",
    "e2e:ci",
    "e2e",
)

KNOWN_PYTHON_VALIDATORS = (
    "scripts/validate_factory.py",
    "scripts/validate_v1_release.py",
    "scripts/validate_v1_1.py",
    "scripts/validate_v1_2.py",
    "scripts/validate_v1_3.py",
    "scripts/validate_v1_4.py",
)


@dataclass(frozen=True)
class Gate:
    gate_id: str
    kind: str
    argv: tuple[str, ...]
    source: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.gate_id,
            "kind": self.kind,
            "argv": list(self.argv),
            "source": self.source,
        }


@dataclass(frozen=True)
class GateRun:
    gate_id: str
    returncode: int
    stdout_tail: str
    stderr_tail: str

    @property
    def success(self) -> bool:
        return self.returncode == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.gate_id,
            "returncode": self.returncode,
            "success": self.success,
            "stdout_tail": self.stdout_tail,
            "stderr_tail": self.stderr_tail,
        }


def package_manager(root: Path) -> str | None:
    for marker, manager in (
        ("pnpm-lock.yaml", "pnpm"),
        ("yarn.lock", "yarn"),
        ("bun.lock", "bun"),
        ("bun.lockb", "bun"),
        ("package-lock.json", "npm"),
    ):
        if (root / marker).is_file():
            return manager
    if (root / "package.json").is_file():
        return "npm"
    return None


def install_argv(root: Path) -> tuple[str, ...] | None:
    manager = package_manager(root)
    if manager == "npm":
        # A package.json without a lockfile is not a reproducible CI install contract.
        return ("npm", "ci") if (root / "package-lock.json").is_file() else None
    if manager == "pnpm":
        return ("pnpm", "install", "--frozen-lockfile")
    if manager == "yarn":
        return ("yarn", "install", "--immutable")
    if manager == "bun":
        return ("bun", "install", "--frozen-lockfile")
    return None


def package_gate_argv(manager: str, script: str) -> tuple[str, ...]:
    if manager == "npm":
        return ("npm", "run", script)
    return (manager, "run", script)


def discover_declared_gates(root: Path | str) -> list[Gate]:
    root = Path(root).resolve()
    gates: list[Gate] = []

    package = root / "package.json"
    manager = package_manager(root)
    if package.is_file() and manager:
        try:
            value = json.loads(package.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            value = {}
        scripts = value.get("scripts", {}) if isinstance(value, dict) else {}
        if isinstance(scripts, dict):
            for script in ALLOWED_PACKAGE_SCRIPTS:
                if script in scripts:
                    gates.append(Gate(
                        gate_id=f"package:{script}",
                        kind="package-script",
                        argv=package_gate_argv(manager, script),
                        source="package.json allowlist",
                    ))

    for relative in KNOWN_PYTHON_VALIDATORS:
        path = root / relative
        if path.is_file():
            gates.append(Gate(
                gate_id=f"python:{relative}",
                kind="python-validator",
                argv=(sys.executable, relative),
                source="known validator allowlist",
            ))

    return gates


def build_ci_plan(root: Path | str) -> dict[str, Any]:
    root = Path(root).resolve()
    manager = package_manager(root)
    install = install_argv(root)
    gates = discover_declared_gates(root)
    package_present = (root / "package.json").is_file()
    return {
        "schema_version": 1,
        "package_manager": manager,
        "install_argv": list(install) if install else None,
        "reproducible_install": bool(install) if package_present else None,
        "gates": [gate.to_dict() for gate in gates],
        "security": {
            "shell": False,
            "prompt_commands": False,
            "secrets_required": False,
            "source": "repository-owned allowlisted gates only",
        },
    }


def tail(text: str, limit: int = 4000) -> str:
    return text[-limit:]


def run_declared_gates(
    root: Path | str,
    *,
    gate_ids: Iterable[str] | None = None,
    timeout_seconds: int = 900,
) -> list[GateRun]:
    root = Path(root).resolve()
    discovered = discover_declared_gates(root)
    selected_ids = set(gate_ids or ())
    selected = [gate for gate in discovered if not selected_ids or gate.gate_id in selected_ids]
    if selected_ids:
        missing = selected_ids - {gate.gate_id for gate in discovered}
        if missing:
            raise ValueError(f"Unknown or undeclared gate ids: {', '.join(sorted(missing))}")

    env = os.environ.copy()
    env.setdefault("CI", "true")
    results: list[GateRun] = []
    for gate in selected:
        completed = subprocess.run(
            list(gate.argv),
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            timeout=max(1, int(timeout_seconds)),
            check=False,
            shell=False,
        )
        result = GateRun(
            gate_id=gate.gate_id,
            returncode=completed.returncode,
            stdout_tail=tail(completed.stdout),
            stderr_tail=tail(completed.stderr),
        )
        results.append(result)
        if not result.success:
            break
    return results
