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
    "scripts/skill_routing.py",
    "skills/learning-engine/SKILL.md",
    "tests/v1_3/test_learning_engine.py",
    "tests/v1_3/test_cli_integration.py",
    "tests/v1_3/test_skill_routing.py",
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
    for marker in (".factory/learning.json", ".factory/skill-routing.json"):
        if marker not in root_ignore:
            fail(f"root .gitignore must keep {marker} local")
        if marker not in starter_ignore:
            fail(f"web-admin starter .gitignore must keep {marker} local")

    learning = (ROOT / "engine/learning_engine.py").read_text(encoding="utf-8")
    for marker in (
        "EVENT_LIMIT = 500",
        "DEFAULT_MIN_SAMPLES = 5",
        'PROTECTED_HEAVY_BACKENDS = {"local_full"}',
        '"external_telemetry": False',
        'return compact if compact in SAFE_ACTIONS else "other"',
        "SKILL_ROUTING_SCHEMA_VERSION = 1",
        "SKILL_ROUTING_MAX_SKILLS = 64",
        '"used_for_backend_learning": False',
        '"automatic_delete_recommendation": False',
    ):
        if marker not in learning:
            fail(f"Learning Engine contract marker missing: {marker}")

    routing_doc = (ROOT / "core/LEARNING_ENGINE.md").read_text(encoding="utf-8")
    for marker in (
        "Skill Routing Telemetry",
        ".factory/skill-routing.json",
        "não afirma saber se um modelo leu",
        "nunca remove ou desativa Skill automaticamente",
    ):
        if marker not in routing_doc:
            fail(f"Skill routing documentation marker missing: {marker}")


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
    print("OK: V1.3 backend learning plus privacy-safe aggregate Skill routing telemetry validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
