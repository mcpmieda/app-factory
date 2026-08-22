#!/usr/bin/env python3
"""Validate App Factory System Engineering Contract wiring."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "core/SYSTEM_ENGINEERING.md",
    "core/ENTRYPOINT.md",
    "core/PROJECT_SCALE.md",
    "core/WORKFLOW.md",
    "core/DEFINITION_OF_DONE.md",
    "AGENTS.md",
    "skills/factory-router/SKILL.md",
    "skills/app-planner/SKILL.md",
    "profiles/web-app/PROFILE.md",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def require(path: str, *markers: str) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            fail(f"{path}: missing required marker: {marker}")


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail("required files missing: " + ", ".join(missing))

    require(
        "core/SYSTEM_ENGINEERING.md",
        "`website`",
        "`local-app`",
        "`persistent-app`",
        "`multi-user-system`",
        "`production-system`",
        "`critical-system`",
        "Proibição de falsa persistência",
        "Autorização é obrigatória no servidor",
        "Definition of Done adicional",
    )
    require(
        "core/ENTRYPOINT.md",
        "core/SYSTEM_ENGINEERING.md",
        "fonte autoritativa dos dados",
        "multi-user-system",
    )
    require(
        "skills/factory-router/SKILL.md",
        "core/SYSTEM_ENGINEERING.md",
        "authoritative data",
        "multi-user-system",
    )
    require(
        "skills/app-planner/SKILL.md",
        "core/SYSTEM_ENGINEERING.md",
        "fonte autoritativa dos dados",
    )
    require(
        "profiles/web-app/PROFILE.md",
        "localStorage",
        "persistent-app",
        "multi-user-system",
    )
    require(
        "core/DEFINITION_OF_DONE.md",
        "Adequação da arquitetura",
        "persistência final compartilhada",
        "autorização é aplicada server-side",
    )
    require(
        "core/PROJECT_SCALE.md",
        "core/SYSTEM_ENGINEERING.md",
        "Os dois eixos são complementares",
    )
    require(
        "core/WORKFLOW.md",
        "Classificação arquitetural",
        "Falha arquitetural também é falha real",
    )
    require(
        "AGENTS.md",
        "core/SYSTEM_ENGINEERING.md",
        "persistência compartilhada real",
    )

    # Regression guard: the new architecture policy must not replace/remove
    # the established V1.4 semantic/autonomy/execution/learning surfaces.
    preserved = [
        "core/SEMANTIC_VERIFICATION.md",
        "core/AUTONOMY_ENGINE.md",
        "core/EXECUTION_FABRIC.md",
        "core/LEARNING_ENGINE.md",
        "engine/semantic_verification.py",
        "engine/autonomy_engine.py",
        "engine/execution_engine.py",
        "engine/learning_engine.py",
        "starters/web-admin/recipes/auth-better-auth/recipe.json",
        "starters/web-admin/recipes/database-drizzle-postgres/recipe.json",
    ]
    removed = [path for path in preserved if not (ROOT / path).is_file()]
    if removed:
        fail("existing V1.4 capability unexpectedly missing: " + ", ".join(removed))

    print("OK: System Engineering Contract is wired and V1.4 core capabilities remain present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
