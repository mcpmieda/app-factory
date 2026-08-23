#!/usr/bin/env python3
"""Validate Agent Conformance corpus, scorer and reference solutions."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "evals/agent-conformance/README.md",
    "evals/agent-conformance/cases/functional-spec-and-plan.json",
    "evals/agent-conformance/cases/docs-change-stays-light.json",
    "scripts/agent_conformance.py",
    "tests/agent_conformance/test_agent_conformance.py",
    "research/EVALUATION_EVIDENCE_RESEARCH.md",
    ".github/workflows/validate-agent-conformance.yml",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def run(*argv: str) -> None:
    subprocess.run([sys.executable, *argv], cwd=ROOT, check=True)


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail("Agent Conformance files missing: " + ", ".join(missing))

    harness = (ROOT / "scripts/agent_conformance.py").read_text(encoding="utf-8")
    for marker in (
        "ACTION_KINDS",
        "BEHAVIORAL_ASSERTIONS",
        "safe_relative_path",
        "run_reference_case",
        "score_workspace",
        "shell=False",
    ):
        if marker not in harness:
            fail(f"Agent Conformance harness missing guardrail: {marker}")

    run("scripts/agent_conformance.py", "validate-corpus")
    run("-m", "unittest", "discover", "-s", "tests/agent_conformance", "-p", "test_*.py", "-v")
    run("scripts/agent_conformance.py", "run-reference")
    print("OK: agent conformance corpus audited; negative scorer tests and reference solutions passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
