#!/usr/bin/env python3
"""Validate Semantic Assurance structure, deterministic engine and Factory wiring."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "core/SEMANTIC_ASSURANCE.md",
    "engine/semantic_assurance.py",
    "scripts/semantic_assurance.py",
    "skills/semantic-assurance/SKILL.md",
    "templates/project/SEMANTICS.md",
    "tests/semantic_assurance/test_semantic_assurance.py",
    "research/SEMANTIC_ASSURANCE_RESEARCH.md",
    ".github/workflows/validate-semantic-assurance.yml",
]

WIRING = {
    "core/SEMANTIC_VERIFICATION.md": ["SEMANTIC_ASSURANCE.md", "qualidade da própria especificação"],
    "core/ENTRYPOINT.md": ["Semantic Assurance", "semantic depth"],
    "core/WORKFLOW.md": ["Semantic Assurance", "semantic-assurance.json"],
    "core/DEFINITION_OF_DONE.md": ["Semantic Assurance", "semantic-assurance.json"],
    "skills/factory-router/SKILL.md": ["semantic-assurance", "semantic depth"],
    "skills/app-planner/SKILL.md": ["Semantic Assurance", "scenario", "domain", "formal"],
    "skills/semantic-verification/SKILL.md": ["semantic-assurance", "qualidade da especificação"],
    "templates/project/AGENTS.md": ["SEMANTIC_ASSURANCE.md", "SEMANTICS.md"],
    "templates/project/PROJECT_STATE.md": ["profundidade semântica", "semantic-assurance.json"],
    "PROJECT_STATE.md": ["Semantic Assurance", "19"],
    "README.md": ["Semantic Assurance", "19 Skills"],
    "APP_FACTORY_PLAN.md": ["Semantic Assurance", "Semantic Verification"],
    "docs/DECISIONS.md": ["Semantic Assurance", "EARS", "FRET"],
    "docs/CODEX_PLUGIN.md": ["Semantic Assurance", "19 Skills"],
}

PRESERVE = [
    "engine/context_engine.py",
    "engine/autonomy_engine.py",
    "engine/execution_engine.py",
    "engine/learning_engine.py",
    "engine/semantic_verification.py",
    "engine/independent_verification.py",
    "core/API_ENGINEERING.md",
    "core/SYSTEM_ENGINEERING.md",
    "core/INDEPENDENT_VERIFICATION.md",
    "starters/web-admin/recipes/auth-better-auth/recipe.json",
    "starters/web-admin/recipes/database-drizzle-postgres/recipe.json",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def require_markers(path: str, markers: list[str]) -> None:
    target = ROOT / path
    if not target.is_file():
        fail(f"missing required integration file: {path}")
    text = target.read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path} missing Semantic Assurance markers: {missing}")


def validate_structure() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail("Semantic Assurance files missing: " + ", ".join(missing))

    core = (ROOT / "core/SEMANTIC_ASSURANCE.md").read_text(encoding="utf-8")
    for marker in (
        "EARS",
        "NASA FRET",
        "Semantic Diff",
        "Z3",
        "Alloy",
        "Quint/TLA+",
        "DMN",
        "OPA/Rego",
        "Cedar",
        "100% não significa",
    ):
        if marker not in core:
            fail(f"Semantic Assurance contract missing marker: {marker}")

    for path, markers in WIRING.items():
        require_markers(path, markers)

    for path in PRESERVE:
        if not (ROOT / path).exists():
            fail(f"regression guard: existing capability missing: {path}")


def run_tests() -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests/semantic_assurance",
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
    print("OK: Semantic Assurance contract, deterministic consistency/coverage/diff engine, proportional formal methods and Factory wiring validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
