#!/usr/bin/env python3
"""Executable validation for App Factory V1.3 Learning Engine."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "core/LEARNING_ENGINE.md",
    "engine/learning_engine.py",
    "engine/execution_engine.py",
    "scripts/factory.py",
    "skills/learning-engine/SKILL.md",
    "tests/v1_3/test_learning_engine.py",
    "tests/v1_3/test_cli_integration.py",
    ".github/workflows/validate-v1-3-learning.yml",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def validate_structure() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail("V1.3 required files missing: " + ", ".join(missing))

    root_ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    starter_ignore = (ROOT / "starters/web-admin/template/.gitignore").read_text(encoding="utf-8")
    marker = ".factory/learning.json"
    if marker not in root_ignore:
        fail("root .gitignore must keep learning.json local")
    if marker not in starter_ignore:
        fail("web-admin starter .gitignore must keep learning.json local")

    learning = (ROOT / "engine/learning_engine.py").read_text(encoding="utf-8")
    for marker in (
        "EVENT_LIMIT = 500",
        "DEFAULT_MIN_SAMPLES = 5",
        'PROTECTED_HEAVY_BACKENDS = {"local_full"}',
        '"external_telemetry": False',
        'return compact if compact in SAFE_ACTIONS else "other"',
    ):
        if marker not in learning:
            fail(f"Learning Engine contract marker missing: {marker}")


def run_tests() -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests/v1_3",
            "-p",
            "test_*.py",
            "-v",
        ],
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    validate_structure()
    run_tests()
    print("OK: V1.3 Learning Engine privacy, confidence, routing, persistence and CLI contracts validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
