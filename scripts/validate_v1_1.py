#!/usr/bin/env python3
"""Executable gates for App Factory V1.1 autonomous context/runtime."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "engine/context_engine.py",
    "engine/autonomy_engine.py",
    "scripts/factory.py",
    "core/CONTEXT_ENGINE.md",
    "core/AUTONOMY_ENGINE.md",
    "skills/context-engine/SKILL.md",
    "skills/autonomy-engine/SKILL.md",
    "tests/v1_1/test_context_engine.py",
    "tests/v1_1/test_autonomy_engine.py",
]


def stop(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def run(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        list(args), cwd=cwd, check=True, capture_output=True, text=True, timeout=120
    )
    return result.stdout


def validate_files() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        stop("V1.1 required files missing: " + ", ".join(missing))


def validate_unit_tests() -> None:
    output = run(sys.executable, "-m", "unittest", "discover", "-s", "tests/v1_1", "-v")
    if "FAILED" in output:
        stop("V1.1 unit tests failed")


def validate_fresh_session_contract() -> None:
    with tempfile.TemporaryDirectory(prefix="app-factory-v11-") as raw:
        project = Path(raw)
        (project / "PROJECT_STATE.md").write_text(
            "# PROJECT_STATE\n\n## Objetivo atual\n\nContinuar o sistema escolar sem contexto de conversa.\n",
            encoding="utf-8",
        )
        (project / "app.py").write_text("def run():\n    return 1\n", encoding="utf-8")
        output = run(sys.executable, str(ROOT / "scripts/factory.py"), "--root", str(project), "resume")
        payload = json.loads(output)
        if payload["action"]["action"] != "plan":
            stop("fresh-session resume did not choose planning")
        if "sistema escolar" not in payload["state"]["goal"]:
            stop("fresh-session resume did not recover goal from PROJECT_STATE.md")
        if not (project / ".factory/context/repo-map.json").is_file():
            stop("fresh-session resume did not create context map")
        if not (project / ".factory/state.json").is_file():
            stop("fresh-session resume did not create autonomous state")


def main() -> int:
    validate_files()
    validate_unit_tests()
    validate_fresh_session_contract()
    print("OK: V1.1 context cache, delta, state machine, bounded repair and fresh-session resume validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
