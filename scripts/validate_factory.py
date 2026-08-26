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
    "core/PROJECT_ADOPTION_GATE.md",
    "core/PRINCIPLES.md",
    "core/HUMAN_INTERACTION.md",
    "core/TASK_ROUTER.md",
    "core/WORKFLOW.md",
    "core/RISK_MODEL.md",
    "core/DEFINITION_OF_DONE.md",
    "core/CHANGE_HYGIENE.md",
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
    "engine/project_adoption.py",
    "scripts/factory.py",
    "scripts/project_adoption_gate.py",
    "scripts/semantic_assurance.py",
    "scripts/independent_verification.py",
    "scripts/agent_conformance.py",
    "scripts/validate_agent_conformance.py",
    "scripts/skill_routing.py",
    "scripts/change_hygiene.py",
    "scripts/validate_change_hygiene.py",
    "evals/agent-conformance/README.md",
    "evals/agent-conformance/cases/functional-spec-and-plan.json",
    "evals/agent-conformance/cases/docs-change-stays-light.json",
    "tests/agent_conformance/test_agent_conformance.py",
    "tests/change_hygiene/test_change_hygiene.py",
    "tests/project_adoption/test_project_adoption.py",
    "research/EVALUATION_EVIDENCE_RESEARCH.md",
    "research/CHANGE_HYGIENE_RESEARCH.md",
    ".coveragerc",
    "requirements/ci-evidence.txt",
    ".github/workflows/validate-agent-conformance.yml",
    ".github/workflows/validate-python-evidence.yml",
    ".github/workflows/validate-change-hygiene.yml",
    "ui/UI_POLICY.md",
    "ui/PROFESSIONAL_UI_PROFILE.md",
    "ui/MOTION_POLICY.md",
    "ui/heroui/README.md",
    "skills/factory-router/SKILL.md",
    "skills/project-adoption/SKILL.md",
    "skills/maintenance/SKILL.md",
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


def validate_project_adoption() -> None:
    require_markers(
        "core/PROJECT_ADOPTION_GATE.md",
        [
            "pre-implementation",
            ".app-factory.json",
            "schemaVersion",
            "React + CSS próprio",
            "shadcn/ui",
            "Semantic-before-code",
            "project_adoption_gate.py",
            "compliance retroativo",
            "Continuidade operacional",
        ],
    )
    require_markers(
        "engine/project_adoption.py",
        ["schemaVersion", "governance", "AD_HOC_DESIGN_SYSTEMS", "Semantic Verification required before code", "review-evidence.json", "VERIFICATION.md"],
    )
    require_markers(
        "scripts/project_adoption_gate.py",
        ["init", "check", "pre-implementation", "delivery", "audit_project", "initialize_project"],
    )
    require_markers(
        "skills/project-adoption/SKILL.md",
        ["core/PROJECT_ADOPTION_GATE.md", "Required order", "React + custom/native CSS", "Client interruption guard", "delivery"],
    )
    require_markers(
        "skills/factory-router/SKILL.md",
        ["project-adoption", "PROJECT_ADOPTION_GATE.md", "pre-implementation", "React + custom/native CSS", "client-interruption continuity contract", "delivery"],
    )
    require_markers(
        "AGENTS.md",
        ["Project Adoption Gate", "skills/project-adoption/SKILL.md", ".app-factory.json", "React + CSS próprio", "pre-implementation", "delivery", "Continuidade após perda do cliente"],
    )
    require_markers(
        "templates/project/AGENTS.md",
        ["PROJECT_ADOPTION_GATE.md", ".app-factory.json", "React + CSS/custom/native UI", "pre-implementation", "delivery", "core/SYSTEM_ENGINEERING.md"],
    )
    require_markers(
        "starters/web-admin/template/AGENTS.md",
        ["PROJECT_ADOPTION_GATE.md", ".app-factory.json", "React + CSS/custom/native UI", "pre-implementation", "delivery", "core/SYSTEM_ENGINEERING.md"],
    )
    require_markers(
        "profiles/web-admin/PROFILE.md",
        ["Project Adoption Gate antes do código", "React + CSS próprio", "ui.deviation", "pre-implementation", "delivery", "Continuidade após perda do cliente"],
    )
    require_markers(".github/workflows/validate-python-evidence.yml", ["tests/project_adoption", "scripts/project_adoption_gate.py"])


def validate_system_engineering_continuity() -> None:
    require_markers(
        "core/SYSTEM_ENGINEERING.md",
        [
            "Continuidade de operações após perda do cliente",
            "foi executada? até onde chegou? o que ainda falta?",
            "não repita cegamente",
            "navegador/cliente",
            "sobrevivência e determinismo",
        ],
    )
    require_markers(
        "templates/project/ARCHITECTURE.md",
        [
            "Continuidade de operações críticas",
            "estado/checkpoint durável fora do navegador",
            "foi executada? até onde chegou? o que ainda falta?",
            "retomada/reconciliação/compensação",
        ],
    )
    require_markers("templates/project/PRODUCT.md", ["Continuidade operacional, quando aplicável", "core/SYSTEM_ENGINEERING.md"])


def validate_professional_ui() -> None:
    require_markers(
        "ui/PROFESSIONAL_UI_PROFILE.md",
        ["professional-default", "shadcn/ui", "ReUI", "HeroUI", "quality bar", "não armazena nem reproduz código", "Visual QA", "prefers-reduced-motion"],
    )
    require_markers(
        "ui/UI_POLICY.md",
        ["professional-default", "ui/PROFESSIONAL_UI_PROFILE.md", "Base preferencial: **shadcn/ui**", "ReUI seletivamente", "HeroUI", "Motion Profile universal", "Nenhum efeito ambiental específico"],
    )
    require_markers(
        "ui/MOTION_POLICY.md",
        ["Motion Profile", "ambient", "prefers-reduced-motion", "prefers-reduced-transparency", "nenhum padrão ambiental específico"],
    )
    require_markers(
        "ui/heroui/README.md",
        ["HeroUI como linguagem principal", "Professional UI Profile", "Motion Profile", "Nenhum efeito ambiental específico"],
    )
    require_markers(
        "skills/ui-builder/SKILL.md",
        ["professional-default", "ui/PROFESSIONAL_UI_PROFILE.md", "shadcn/ui como base", "ReUI seletivamente", "HeroUI", "Inventário antes da implementação", "não ativa automaticamente"],
    )
    require_markers("templates/project/PRODUCT.md", ["Professional UI Profile", "professional-default", "density", "Motion Profile"])
    require_markers("templates/project/ARCHITECTURE.md", ["Professional UI Profile", "professional-default", "UI profissional, quando aplicável", "Motion Profile"])
    require_markers("templates/project/AGENTS.md", ["ui/PROFESSIONAL_UI_PROFILE.md", "HeroUI", "mandatory environmental effect"])
    require_markers("profiles/web-admin/PROFILE.md", ["shadcn/ui como base do design system", "ReUI", "HeroUI é perfil visual alternativo"])
    require_markers("starters/web-admin/template/.factory-template.json", ['"professionalUiProfile": "professional-default"', '"motionProfile": "ambient"'])
    require_markers("starters/web-admin/template/AGENTS.md", ["Preserve shadcn/ui as the visual foundation", "ReUI", "professional-default", "ui/PROFESSIONAL_UI_PROFILE.md"])
    require_markers("starters/web-admin/template/PRODUCT.md", ["visual system: shadcn/ui baseline", "ReUI only when", "Professional UI Profile: `professional-default`"])
    require_markers("starters/web-admin/template/ARCHITECTURE.md", ["Tailwind CSS + shadcn/ui", "ReUI only when", "Professional UI Profile: `professional-default`", "HeroUI"])
    require_markers("starters/web-admin/template/PROJECT_STATE.md", ["design system: shadcn/ui foundation", "advanced UI/ReUI: not activated", "Professional UI Profile: `professional-default`"])
    require_markers("scripts/create-web-admin.mjs", ["professionalUiProfile", '"professionalUiProfile"', "Professional UI Profile:"])
    require_markers("scripts/create-web-admin.test.mjs", ["baseManifest.professionalUiProfile", "professional-default", "design system: shadcn\\/ui foundation"])
    require_markers("research/SOURCES.md", ["HeroUI Pro", "INSPIRAR", "ui/PROFESSIONAL_UI_PROFILE.md"])


def validate_evaluation_evidence() -> None:
    require_markers(
        "research/EVALUATION_EVIDENCE_RESEARCH.md",
        ["Agent Conformance Corpus", "SWE-bench", "Inspect AI", "coverage.py", "diff-cover", "Skill Routing Telemetry", "OpenTelemetry"],
    )
    require_markers(
        "scripts/agent_conformance.py",
        ["ACTION_KINDS", "BEHAVIORAL_ASSERTIONS", "safe_relative_path", "run_reference_case", "score_workspace", "shell=False"],
    )
    require_markers(".coveragerc", ["branch = True", "source = engine"])
    require_markers(
        ".github/workflows/validate-python-evidence.yml",
        ["fetch-depth: 0", "coverage run --parallel-mode", "diff-cover coverage.xml", "--fail-under=100", "Upload evidence artifacts"],
    )
    require_markers(
        "core/LEARNING_ENGINE.md",
        ["Skill Routing Telemetry", ".factory/skill-routing.json", "não afirma saber se um modelo leu", "nunca remove ou desativa Skill automaticamente"],
    )
    require_markers("skills/factory-router/SKILL.md", ["scripts/skill_routing.py", "advisory aggregate telemetry", "never include prompt/task text"])


def validate_change_hygiene() -> None:
    require_markers(
        "core/CHANGE_HYGIENE.md",
        ["preservar comportamento estável não significa preservar implementação obsoleta", "Substituir, não sombrear", "Consolidação após repair loop", "projetos externos", "scripts/change_hygiene.py"],
    )
    require_markers("skills/maintenance/SKILL.md", ["core/CHANGE_HYGIENE.md", "Consolidação obrigatória", "net code health da área tocada"])
    require_markers("core/PRINCIPLES.md", ["Preservar comportamento, não implementação obsoleta", "A árvore final não é o histórico de tentativas"])
    require_markers("core/DEFINITION_OF_DONE.md", ["Change Hygiene em sistemas existentes", "shadow implementations", "Manutenção não termina apenas porque o bug sumiu"])
    require_markers("research/CHANGE_HYGIENE_RESEARCH.md", ["Google Engineering Practices", "Chromium", "Microsoft Engineering Fundamentals Playbook", "Knip", "Stylelint", "jscpd"])


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

    validate_project_adoption()
    validate_system_engineering_continuity()
    validate_professional_ui()
    validate_evaluation_evidence()
    validate_change_hygiene()

    print(
        f"OK: {len(REQUIRED)} arquivos obrigatórios, {len(skill_files)} Skills, Project Adoption Gate, System Engineering/Client Interruption Resilience, Professional UI, Evaluation Evidence e Change Hygiene validados."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
