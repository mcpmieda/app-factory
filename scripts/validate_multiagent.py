#!/usr/bin/env python3
"""Executable gate for provider-neutral multiagent execution."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "engine/work_orchestrator.py",
    "scripts/factory_run.py",
    "core/MULTIAGENT_EXECUTION.md",
    "tests/multiagent/test_work_orchestrator.py",
    "tests/multiagent/test_factory_run_cli.py",
]


def stop(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def run(*args: str, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=cwd, check=check, capture_output=True, text=True, timeout=180
    )


def validate_files() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        stop("Multiagent required files missing: " + ", ".join(missing))


def validate_unit_tests() -> None:
    result = run(
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests/multiagent",
        "-v",
        check=False,
    )
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        stop("Multiagent unit tests failed")


def validate_zero_first_and_remote_fallback() -> None:
    with tempfile.TemporaryDirectory(prefix="app-factory-multiagent-") as raw:
        spec = Path(raw) / "run.json"
        spec.write_text(
            json.dumps({
                "schema_version": 1,
                "run_id": "gate",
                "goal": "prove provider routing",
                "tasks": [
                    {
                        "id": "implementation",
                        "title": "Implementation",
                        "paths": ["src/feature"],
                        "required_capabilities": ["reasoning", "repo_read", "repo_write"],
                    }
                ],
            }),
            encoding="utf-8",
        )
        local = run(
            sys.executable,
            "scripts/factory_run.py",
            "plan",
            str(spec),
            "--providers",
            "jules,opencode_ollama",
        )
        local_payload = json.loads(local.stdout)
        if local_payload["waves"][0]["assignments"][0]["provider"] != "opencode_ollama":
            stop("zero-cost local provider was not preferred when explicitly available")

        remote = run(
            sys.executable,
            "scripts/factory_run.py",
            "plan",
            str(spec),
            "--providers",
            "jules,antigravity",
        )
        remote_payload = json.loads(remote.stdout)
        if remote_payload["waves"][0]["assignments"][0]["provider"] not in {"jules", "antigravity"}:
            stop("remote free-quota fallback was not selected")


def validate_codex_manual_only() -> None:
    providers = json.loads(run(sys.executable, "scripts/factory_run.py", "providers").stdout)
    codex = providers.get("codex") or {}
    if codex.get("automatic") is not False or codex.get("cost_class") != "metered":
        stop("Codex must remain a metered manual-only escalation provider")


def main() -> int:
    validate_files()
    validate_unit_tests()
    validate_zero_first_and_remote_fallback()
    validate_codex_manual_only()
    print("OK: multiagent work graph, safe parallelism, zero-first routing and premium escalation guard validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
