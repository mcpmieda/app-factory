#!/usr/bin/env python3
"""Validação estrutural mínima da App Factory usando apenas a stdlib."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "AGENTS.md",
    "APP_FACTORY_PLAN.md",
    "core/ENTRYPOINT.md",
    "core/PRINCIPLES.md",
    "core/HUMAN_INTERACTION.md",
    "core/TASK_ROUTER.md",
    "core/WORKFLOW.md",
    "core/RISK_MODEL.md",
    "core/DEFINITION_OF_DONE.md",
    "core/CONTEXT_ENGINE.md",
    "core/AUTONOMY_ENGINE.md",
    "core/EXECUTION_FABRIC.md",
    "engine/context_engine.py",
    "engine/autonomy_engine.py",
    "engine/execution_engine.py",
    "engine/ci_executor.py",
    "scripts/factory.py",
    "ui/UI_POLICY.md",
    "ui/MOTION_POLICY.md",
    "skills/factory-router/SKILL.md",
    "skills/context-engine/SKILL.md",
    "skills/autonomy-engine/SKILL.md",
    "skills/execution-router/SKILL.md",
    "skills/ui-builder/SKILL.md",
    "templates/project/AGENTS.md",
]

SKILL_HEADER = re.compile(
    r"^---\s*\n(?:(?!^---$).)*?^name:\s*.+$.*?^description:\s*.+$.*?^---$",
    re.MULTILINE | re.DOTALL,
)


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail("Arquivos obrigatórios ausentes: " + ", ".join(missing))

    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skill_files:
        fail("Nenhuma Skill encontrada em skills/*/SKILL.md")

    for skill in skill_files:
        text = skill.read_text(encoding="utf-8")
        if not SKILL_HEADER.search(text):
            fail(f"Frontmatter inválido ou incompleto: {skill.relative_to(ROOT)}")

    print(f"OK: {len(REQUIRED)} arquivos obrigatórios e {len(skill_files)} Skills validados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
