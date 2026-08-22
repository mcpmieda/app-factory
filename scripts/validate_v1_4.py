#!/usr/bin/env python3
"""Executable validation for App Factory V1.4 Semantic Verification Layer."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "core/SEMANTIC_VERIFICATION.md",
    "engine/semantic_verification.py",
    "engine/review_packet.py",
    "skills/semantic-verification/SKILL.md",
    "tests/v1_4/test_semantic_verification.py",
    "tests/v1_4/test_autonomy_semantic.py",
    "tests/v1_4/test_cli_semantic.py",
    "tests/v1_4/test_review_packet.py",
    ".github/workflows/validate-v1-4-semantic.yml",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def validate_structure() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail("V1.4 required files missing: " + ", ".join(missing))

    engine = (ROOT / "engine/semantic_verification.py").read_text(encoding="utf-8")
    for marker in (
        'SPEC_PATH = Path("specs/semantic-contract.json")',
        'PLAN_PATH = Path("specs/verification-plan.json")',
        'REVIEW_PATH = Path("specs/review-evidence.json")',
        'REVIEW_MODES = {"independent-agent", "clean-context", "deterministic-ci"}',
        'return "decoupled" if spec.get("risk") in {"medium", "high"} else "any"',
    ):
        if marker not in engine:
            fail(f"Semantic Verification contract marker missing: {marker}")

    packet = (ROOT / "engine/review_packet.py").read_text(encoding="utf-8")
    for marker in (
        ':(exclude)specs/review-evidence.json',
        '"Fresh review input only.',
        '"diff": diff',
    ):
        if marker not in packet:
            fail(f"Clean-context review packet marker missing: {marker}")

    autonomy = (ROOT / "engine/autonomy_engine.py").read_text(encoding="utf-8")
    for marker in ('"specification"', '"spec-ready"', 'validate_verification_plan', 'validate_review_evidence'):
        if marker not in autonomy:
            fail(f"Autonomy semantic gate marker missing: {marker}")


def run_tests() -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests/v1_4",
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
    print("OK: V1.4 semantic spec, traceability, clean-context diff review, stale-evidence and autonomy contracts validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
