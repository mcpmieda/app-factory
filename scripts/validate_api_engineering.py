#!/usr/bin/env python3
"""Valida a integração do API Engineering Contract sem dependências externas."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def read(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        fail(f"Arquivo obrigatório ausente: {path}")
    return target.read_text(encoding="utf-8")


def require_markers(path: str, markers: list[str]) -> None:
    text = read(path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{path} sem marcadores obrigatórios: {missing}")


def main() -> int:
    require_markers(
        "core/API_ENGINEERING.md",
        [
            "`none`",
            "`lightweight`",
            "`contract`",
            "`governed`",
            "OpenAPI",
            "GraphQL",
            "gRPC",
            "AsyncAPI",
            "Arazzo",
            "RFC 9457",
            "RFC 9110",
            "OWASP API Security",
            "Redocly CLI",
            "oasdiff",
            "Schemathesis",
            "Pact",
            "idempot",
            "Webhooks",
            "breaking",
            "timeout",
            "retry",
            "contract-first",
            "não cria uma API onde o produto não precisa",
        ],
    )

    require_markers(
        "skills/api-engineering/SKILL.md",
        [
            "name: api-engineering",
            "core/API_ENGINEERING.md",
            "none`, `lightweight`, `contract` ou `governed",
            "Redocly",
            "oasdiff",
            "Schemathesis",
            "Pact",
            "semantic-verification",
            "security-review",
        ],
    )

    integration_files = [
        "README.md",
        "AGENTS.md",
        "PROJECT_STATE.md",
        "PORTABILITY.md",
        "core/ENTRYPOINT.md",
        "core/SYSTEM_ENGINEERING.md",
        "core/SEMANTIC_VERIFICATION.md",
        "core/WORKFLOW.md",
        "core/DEFINITION_OF_DONE.md",
        "skills/factory-router/SKILL.md",
        "skills/app-planner/SKILL.md",
        "skills/architecture/SKILL.md",
        "skills/security-review/SKILL.md",
        "profiles/web-admin/PROFILE.md",
        "profiles/web-app/PROFILE.md",
        "profiles/automation/PROFILE.md",
        "templates/project/AGENTS.md",
        "templates/project/ARCHITECTURE.md",
        "templates/project/PROJECT_STATE.md",
    ]
    for path in integration_files:
        text = read(path)
        if "API_ENGINEERING" not in text and "api-engineering" not in text and "API Engineering" not in text:
            fail(f"{path} não referencia a fonte comum de API Engineering")

    require_markers(
        "PROJECT_STATE.md",
        [
            "governance hardening",
            "API Engineering Contract",
            "17",
            "Validate API Engineering Contract",
        ],
    )
    require_markers(
        "templates/project/API.md",
        [
            "modo de governanca",
            "fonte de verdade",
            "compatibilidade",
            "timeout",
            "retry",
            "Webhooks/eventos",
            "Gates",
            "Arazzo",
            "Nao copie `core/API_ENGINEERING.md`",
        ],
    )
    require_markers(
        "templates/api/redocly.yaml",
        ["recommended-strict", "version the Redocly CLI"],
    )
    require_markers(
        "templates/api/README.md",
        ["@redocly/cli", "oasdiff breaking", "schemathesis", "nao dependencias universais"],
    )

    # Regression guards: API governance must extend, not replace, the proven engines/recipes.
    preserved = [
        "core/SYSTEM_ENGINEERING.md",
        "core/CONTEXT_ENGINE.md",
        "core/AUTONOMY_ENGINE.md",
        "core/EXECUTION_FABRIC.md",
        "core/LEARNING_ENGINE.md",
        "core/SEMANTIC_VERIFICATION.md",
        "engine/context_engine.py",
        "engine/autonomy_engine.py",
        "engine/execution_engine.py",
        "engine/learning_engine.py",
        "engine/semantic_verification.py",
        "starters/web-admin/recipes/auth-better-auth/recipe.json",
        "starters/web-admin/recipes/database-drizzle-postgres/recipe.json",
    ]
    missing = [path for path in preserved if not (ROOT / path).is_file()]
    if missing:
        fail("Regressão: capacidades/recipes preservados ausentes: " + ", ".join(missing))

    readme = read("README.md")
    if "17 Skills" not in readme:
        fail("README deve refletir a nova Skill sem alterar a baseline dos engines")

    print(
        "OK: API Engineering integrado de forma condicional a arquitetura, semântica, "
        "segurança, perfis, templates e regressão dos engines/recipes existentes."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
