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
    "core/SYSTEM_ENGINEERING.md",
    "core/API_ENGINEERING.md",
    "core/SEMANTIC_ASSURANCE.md",
    "core/INDEPENDENT_VERIFICATION.md",
    "core/CONTEXT_ENGINE.md",
    "core/AUTONOMY_ENGINE.md",
    "core/EXECUTION_FABRIC.md",
    "core/LEARNING_ENGINE.md",
    "core/SEMANTIC_VERIFICATION.md",
    "engine/context_engine.py",
    "engine/autonomy_engine.py",
    "engine/execution_engine.py",
    "engine/ci_executor.py",
    "engine/learning_engine.py",
    "engine/semantic_assurance.py",
    "engine/semantic_verification.py",
    "engine/independent_verification.py",
    "engine/review_packet.py",
    "scripts/factory.py",
    "scripts/semantic_assurance.py",
    "scripts/independent_verification.py",
    "ui/UI_POLICY.md",
    "ui/PROFESSIONAL_UI_PROFILE.md",
    "ui/MOTION_POLICY.md",
    "skills/factory-router/SKILL.md",
    "skills/api-engineering/SKILL.md",
    "skills/semantic-assurance/SKILL.md",
    "skills/independent-verification/SKILL.md",
    "skills/context-engine/SKILL.md",
    "skills/autonomy-engine/SKILL.md",
    "skills/execution-router/SKILL.md",
    "skills/learning-engine/SKILL.md",
    "skills/semantic-verification/SKILL.md",
    "skills/ui-builder/SKILL.md",
    "templates/project/AGENTS.md",
    "templates/project/SEMANTICS.md",
    "templates/project/VERIFICATION.md",
]

SKILL_HEADER = re.compile(
    r"^---\s*\n(?:(?!^---$).)*?^name:\s*.+$.*?^description:\s*.+$.*?^---$",
    re.MULTILINE | re.DOTALL,
)


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def require_markers(path: str, markers: list[str]) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path} sem marcadores obrigatórios: {missing}")


def validate_professional_ui() -> None:
    require_markers(
        "ui/PROFESSIONAL_UI_PROFILE.md",
        [
            "professional-default",
            "shadcn/ui",
            "ReUI",
            "HeroUI",
            "quality bar",
            "não armazena nem reproduz código",
            "Visual QA",
            "prefers-reduced-motion",
        ],
    )
    require_markers(
        "ui/UI_POLICY.md",
        [
            "professional-default",
            "ui/PROFESSIONAL_UI_PROFILE.md",
            "Base preferencial: **shadcn/ui**",
            "ReUI seletivamente",
            "HeroUI",
        ],
    )
    require_markers(
        "skills/ui-builder/SKILL.md",
        [
            "professional-default",
            "ui/PROFESSIONAL_UI_PROFILE.md",
            "shadcn/ui como base",
            "ReUI seletivamente",
            "HeroUI",
            "Inventário antes da implementação",
        ],
    )
    require_markers(
        "templates/project/PRODUCT.md",
        ["Professional UI Profile", "professional-default", "density"],
    )
    require_markers(
        "templates/project/ARCHITECTURE.md",
        [
            "Professional UI Profile",
            "professional-default",
            "UI profissional, quando aplicável",
        ],
    )
    require_markers(
        "templates/project/AGENTS.md",
        ["ui/PROFESSIONAL_UI_PROFILE.md", "professional-default"],
    )
    # Guardrail: o novo quality bar não pode inverter a escolha validada do
    # perfil administrativo.
    require_markers(
        "profiles/web-admin/PROFILE.md",
        [
            "shadcn/ui como base do design system",
            "ReUI",
            "HeroUI é perfil visual alternativo",
        ],
    )
    require_markers(
        "starters/web-admin/template/.factory-template.json",
        ['"professionalUiProfile": "professional-default"', '"motionProfile": "ambient"'],
    )
    require_markers(
        "starters/web-admin/template/AGENTS.md",
        [
            "Preserve shadcn/ui as the visual foundation",
            "ReUI",
            "professional-default",
            "ui/PROFESSIONAL_UI_PROFILE.md",
        ],
    )
    require_markers(
        "starters/web-admin/template/PRODUCT.md",
        [
            "visual system: shadcn/ui baseline",
            "ReUI only when",
            "Professional UI Profile: `professional-default`",
        ],
    )
    require_markers(
        "starters/web-admin/template/ARCHITECTURE.md",
        [
            "Tailwind CSS + shadcn/ui",
            "ReUI only when",
            "Professional UI Profile: `professional-default`",
            "HeroUI",
        ],
    )
    require_markers(
        "starters/web-admin/template/PROJECT_STATE.md",
        [
            "design system: shadcn/ui foundation",
            "advanced UI/ReUI: not activated",
            "Professional UI Profile: `professional-default`",
        ],
    )
    require_markers(
        "scripts/create-web-admin.mjs",
        [
            "professionalUiProfile",
            '"professionalUiProfile"',
            "Professional UI Profile:",
        ],
    )
    require_markers(
        "scripts/create-web-admin.test.mjs",
        [
            "baseManifest.professionalUiProfile",
            "professional-default",
            "design system: shadcn\\/ui foundation",
        ],
    )
    require_markers(
        "research/SOURCES.md",
        ["HeroUI Pro", "INSPIRAR", "ui/PROFESSIONAL_UI_PROFILE.md"],
    )


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

    validate_professional_ui()

    print(
        f"OK: {len(REQUIRED)} arquivos obrigatórios, {len(skill_files)} Skills e Professional UI validados."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
