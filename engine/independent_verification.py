from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

RISK_LEVELS = ("low", "medium", "high", "critical")
SYSTEM_LEVELS = (
    "website",
    "local-app",
    "persistent-app",
    "multi-user-system",
    "production-system",
    "critical-system",
)
API_MODES = ("none", "lightweight", "contract", "governed")
VERIFICATION_MODES = ("baseline", "independent", "adversarial", "release")

RISK_RANK = {value: index for index, value in enumerate(RISK_LEVELS)}
SYSTEM_RANK = {value: index for index, value in enumerate(SYSTEM_LEVELS)}
API_RANK = {value: index for index, value in enumerate(API_MODES)}


@dataclass(frozen=True)
class ProjectSignals:
    javascript: bool
    python: bool
    tests: bool
    web_ui: bool
    playwright: bool
    openapi: bool
    graphql: bool
    api_contract: bool

    def to_dict(self) -> dict[str, bool]:
        return {
            "javascript": self.javascript,
            "python": self.python,
            "tests": self.tests,
            "web_ui": self.web_ui,
            "playwright": self.playwright,
            "openapi": self.openapi,
            "graphql": self.graphql,
            "api_contract": self.api_contract,
        }


@dataclass(frozen=True)
class VerificationCheck:
    check_id: str
    tool: str
    category: str
    status: str
    trigger: str
    reason: str
    safety: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return {
            "id": self.check_id,
            "tool": self.tool,
            "category": self.category,
            "status": self.status,
            "trigger": self.trigger,
            "reason": self.reason,
            "safety": self.safety,
        }


def _package(root: Path) -> dict[str, Any]:
    path = root / "package.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def detect_project_signals(root: Path | str) -> ProjectSignals:
    root = Path(root).resolve()
    package = _package(root)
    dependencies: dict[str, Any] = {}
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        value = package.get(key)
        if isinstance(value, dict):
            dependencies.update(value)

    dep_names = {str(name).lower() for name in dependencies}
    script_names = {str(name).lower() for name in (package.get("scripts") or {})} if isinstance(package.get("scripts"), dict) else set()

    javascript = (root / "package.json").is_file()
    python = any((root / name).is_file() for name in ("pyproject.toml", "requirements.txt", "requirements-dev.txt", "setup.py"))
    tests = any((root / name).exists() for name in ("tests", "test", "__tests__")) or any(
        name.startswith("test") for name in script_names
    )
    playwright = any((root / name).is_file() for name in ("playwright.config.ts", "playwright.config.js", "playwright.config.mjs")) or "@playwright/test" in dep_names
    web_frameworks = {
        "next",
        "react",
        "react-dom",
        "astro",
        "vue",
        "nuxt",
        "svelte",
        "@sveltejs/kit",
        "vite",
    }
    web_ui = bool(dep_names & web_frameworks) or playwright

    openapi = any((root / path).is_file() for path in (
        "api/openapi.yaml",
        "api/openapi.yml",
        "api/openapi.json",
        "openapi.yaml",
        "openapi.yml",
        "openapi.json",
    ))
    graphql = any((root / path).is_file() for path in (
        "api/schema.graphql",
        "schema.graphql",
        "schema.graphqls",
    ))
    api_contract = openapi or graphql or (root / "api/asyncapi.yaml").is_file() or (root / "api/proto").is_dir()

    return ProjectSignals(
        javascript=javascript,
        python=python,
        tests=tests,
        web_ui=web_ui,
        playwright=playwright,
        openapi=openapi,
        graphql=graphql,
        api_contract=api_contract,
    )


def _validate(value: str, allowed: tuple[str, ...], label: str) -> str:
    value = str(value).strip().lower()
    if value not in allowed:
        raise ValueError(f"Unknown {label}: {value}. Expected one of: {', '.join(allowed)}")
    return value


def choose_verification_mode(
    *,
    risk: str = "medium",
    system_level: str = "persistent-app",
    api_mode: str = "none",
    release: bool = False,
) -> str:
    risk = _validate(risk, RISK_LEVELS, "risk")
    system_level = _validate(system_level, SYSTEM_LEVELS, "system level")
    api_mode = _validate(api_mode, API_MODES, "API mode")

    if release and SYSTEM_RANK[system_level] >= SYSTEM_RANK["production-system"]:
        return "release"
    if (
        RISK_RANK[risk] >= RISK_RANK["high"]
        or SYSTEM_RANK[system_level] >= SYSTEM_RANK["multi-user-system"]
        or API_RANK[api_mode] >= API_RANK["governed"]
    ):
        return "adversarial"
    if (
        RISK_RANK[risk] >= RISK_RANK["medium"]
        or SYSTEM_RANK[system_level] >= SYSTEM_RANK["persistent-app"]
        or API_RANK[api_mode] >= API_RANK["contract"]
    ):
        return "independent"
    return "baseline"


def _check(
    check_id: str,
    tool: str,
    category: str,
    *,
    required: bool,
    trigger: str,
    reason: str,
    safety: str | None = None,
) -> VerificationCheck:
    return VerificationCheck(
        check_id=check_id,
        tool=tool,
        category=category,
        status="required" if required else "advisory",
        trigger=trigger,
        reason=reason,
        safety=safety,
    )


def build_independent_verification_plan(
    root: Path | str,
    *,
    risk: str = "medium",
    system_level: str = "persistent-app",
    api_mode: str = "none",
    release: bool = False,
) -> dict[str, Any]:
    root = Path(root).resolve()
    risk = _validate(risk, RISK_LEVELS, "risk")
    system_level = _validate(system_level, SYSTEM_LEVELS, "system level")
    api_mode = _validate(api_mode, API_MODES, "API mode")
    mode = choose_verification_mode(
        risk=risk,
        system_level=system_level,
        api_mode=api_mode,
        release=release,
    )
    signals = detect_project_signals(root)
    checks: list[VerificationCheck] = []

    if mode != "baseline":
        checks.append(_check(
            "supply-chain",
            "Trivy",
            "dependencies-secrets-misconfiguration",
            required=True,
            trigger="pull_request",
            reason="Independent scan for vulnerable dependencies, secrets and repository misconfiguration.",
        ))
        checks.append(_check(
            "sast",
            "Semgrep Community Edition",
            "static-security",
            required=mode in {"adversarial", "release"},
            trigger="pull_request",
            reason="Static security rules provide evidence independent from implementation-authored tests.",
        ))

    if signals.web_ui and mode != "baseline":
        checks.append(_check(
            "accessibility",
            "axe-core + Playwright",
            "accessibility",
            required=mode in {"adversarial", "release"},
            trigger="pull_request",
            reason="Automated accessibility checks cover important rendered states outside normal functional assertions.",
        ))

    if signals.web_ui and mode == "release":
        checks.append(_check(
            "web-quality",
            "Lighthouse CI",
            "performance-quality",
            required=False,
            trigger="release",
            reason="Release quality/performance budgets should become blocking only after a stable project baseline exists.",
        ))

    if api_mode in {"contract", "governed"} and signals.api_contract:
        checks.append(_check(
            "api-property-testing",
            "Schemathesis",
            "api-fuzz-property-stateful",
            required=mode in {"adversarial", "release"},
            trigger="pull_request",
            reason="Generate API cases and stateful sequences independently from hand-written examples.",
            safety="Use isolated test data and never run destructive fuzzing against production by default.",
        ))

    if signals.web_ui and mode in {"adversarial", "release"}:
        checks.append(_check(
            "dast-baseline",
            "OWASP ZAP",
            "dynamic-security",
            required=True,
            trigger="pull_request",
            reason="Observe the running web application externally in an ephemeral environment.",
            safety="Target only an ephemeral/local authorized environment; never infer a production target.",
        ))

    if signals.web_ui and mode == "release":
        checks.append(_check(
            "dast-active",
            "OWASP ZAP active scan",
            "dynamic-security-active",
            required=RISK_RANK[risk] >= RISK_RANK["high"],
            trigger="release",
            reason="Active DAST adds stronger adversarial coverage for high-risk production releases.",
            safety="Active scan is allowed only against disposable or explicitly authorized targets.",
        ))

    if signals.tests and mode in {"adversarial", "release"}:
        if signals.javascript:
            checks.append(_check(
                "mutation-js",
                "StrykerJS",
                "mutation-testing",
                required=mode == "release" and RISK_RANK[risk] >= RISK_RANK["high"],
                trigger="release" if mode == "release" else "pull_request-selective",
                reason="Mutate JavaScript/TypeScript production logic to prove tests detect deliberate defects.",
            ))
        if signals.python:
            checks.append(_check(
                "mutation-python",
                "mutmut",
                "mutation-testing",
                required=mode == "release" and RISK_RANK[risk] >= RISK_RANK["high"],
                trigger="release" if mode == "release" else "pull_request-selective",
                reason="Mutate Python production logic to prove tests detect deliberate defects.",
            ))

    return {
        "schema_version": 1,
        "mode": mode,
        "free_only": True,
        "preferred_executor": "github_ci",
        "fallback_executor": "local_full/self-hosted-runner when GitHub-hosted capacity is unavailable",
        "risk": risk,
        "system_level": system_level,
        "api_mode": api_mode,
        "release": bool(release),
        "signals": signals.to_dict(),
        "checks": [check.to_dict() for check in checks],
        "required_check_ids": [check.check_id for check in checks if check.status == "required"],
        "advisory_check_ids": [check.check_id for check in checks if check.status == "advisory"],
        "rules": {
            "no_paid_ai_required": True,
            "no_active_scan_against_production_by_default": True,
            "tool_unavailable_is_not_pass": True,
            "semantic_review_remains_separate": True,
            "pin_versions_in_real_ci": True,
        },
    }
