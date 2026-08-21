#!/usr/bin/env python3
"""Executable gates for App Factory V1.2 Execution Fabric."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "engine/execution_engine.py",
    "engine/ci_executor.py",
    "core/EXECUTION_FABRIC.md",
    "skills/execution-router/SKILL.md",
    "tests/v1_2/test_execution_engine.py",
    "tests/v1_2/test_ci_executor.py",
    "tests/v1_2/test_cli_integration.py",
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
        stop("V1.2 required files missing: " + ", ".join(missing))


def validate_unit_tests() -> None:
    result = run(sys.executable, "-m", "unittest", "discover", "-s", "tests/v1_2", "-v")
    if "FAILED" in result.stdout or "FAILED" in result.stderr:
        stop("V1.2 unit tests failed")


def validate_fresh_project_routing() -> None:
    with tempfile.TemporaryDirectory(prefix="app-factory-v12-") as raw:
        project = Path(raw)
        (project / "PROJECT_STATE.md").write_text(
            "# PROJECT_STATE\n\n## Objetivo atual\n\nContinuar um sistema escolar.\n",
            encoding="utf-8",
        )
        (project / "app.py").write_text("def run():\n    return 1\n", encoding="utf-8")
        resumed = run(sys.executable, str(ROOT / "scripts/factory.py"), "--root", str(project), "resume")
        payload = json.loads(resumed.stdout)
        if payload["execution"]["backend"] != "current_agent":
            stop("planning did not stay on current_agent")

        run(sys.executable, str(ROOT / "scripts/factory.py"), "--root", str(project), "record", "plan-ready")
        verified = run(
            sys.executable,
            str(ROOT / "scripts/factory.py"),
            "--root",
            str(project),
            "record",
            "implementation-ready",
        )
        payload = json.loads(verified.stdout)
        if payload["next"]["action"] != "verify" or payload["execution"]["backend"] != "github_ci":
            stop("verification did not route to github_ci")


def validate_no_implicit_local_backend() -> None:
    with tempfile.TemporaryDirectory(prefix="app-factory-v12-local-") as raw:
        project = Path(raw)
        result = run(
            sys.executable,
            str(ROOT / "scripts/factory.py"),
            "--root",
            str(project),
            "route",
            "verify",
            "--interactive-browser",
            check=False,
        )
        if result.returncode != 2:
            stop("interactive capability unexpectedly received an implicit local backend")
        payload = json.loads(result.stdout)
        if payload.get("backend") is not None:
            stop("interactive capability must remain unresolved until local backend is explicitly available")


def main() -> int:
    validate_files()
    validate_unit_tests()
    validate_fresh_project_routing()
    validate_no_implicit_local_backend()
    print("OK: V1.2 capability routing, current-agent lane, CI executor and fallback contracts validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
