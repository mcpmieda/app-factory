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
SEMANTIC_DEPTHS = ("none", "scenario", "domain", "formal")

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
    browser_extension: bool
    openapi: bool
    graphql: bool
    api_contract: bool
    github_workflows: bool
    postgres: bool
    postgres_migrations: bool
    architecture_rules: bool
    load_tests: bool
    restler_config: bool
    semantic_assurance: bool
    semantic_depth: str
    property_candidate: bool
    combinatorial_candidate: bool
    combinatorial_model: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "javascript": self.javascript,
            "python": self.python,
            "tests": self.tests,
            "web_ui": self.web_ui,
            "playwright": self.playwright,
            "browser_extension": self.browser_extension,
            "openapi": self.openapi,
            "graphql": self.graphql,
            "api_contract": self.api_contract,
            "github_workflows": self.github_workflows,
            "postgres": self.postgres,
            "postgres_migrations": self.postgres_migrations,
            "architecture_rules": self.architecture_rules,
            "load_tests": self.load_tests,
            "restler_config": self.restler_config,
            "semantic_assurance": self.semantic_assurance,
            "semantic_depth": self.semantic_depth,
            "property_candidate": self.property_candidate,
            "combinatorial_candidate": self.combinatorial_candidate,
            "combinatorial_model": self.combinatorial_model,
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


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _package(root: Path) -> dict[str, Any]:
    return _read_json(root / "package.json")


def _has_files(root: Path, patterns: tuple[str, ...]) -> bool:
    return any(any(path.is_file() for path in root.glob(pattern)) for pattern in patterns)


def _has_dir(root: Path, paths: tuple[str, ...]) -> bool:
    return any((root / path).is_dir() for path in paths)


def _semantic_signals(root: Path) -> tuple[bool, str, bool, bool, bool]:
    assurance = _read_json(root / "specs/semantic-assurance.json")
    contract = _read_json(root / "specs/semantic-contract.json")
    if not assurance:
        return False, "none", bool(contract.get("invariants")), False, False

    depth = str(assurance.get("depth", "none")).strip().lower()
    if depth not in SEMANTIC_DEPTHS:
        depth = "none"

    constraints = [item for item in assurance.get("constraints", []) if isinstance(item, dict)]
    transitions = [item for item in assurance.get("transitions", []) if isinstance(item, dict)]
    states = [item for item in assurance.get("states", []) if isinstance(item, dict)]
    invariants = [item for item in contract.get("invariants", []) if isinstance(item, dict)]

    property_candidate = depth in {"domain", "formal"} and bool(constraints or transitions or invariants)
    finite_dimensions = 0
    for item in constraints:
        if item.get("kind") == "enum":
            allowed = item.get("allowed", [])
            if isinstance(allowed, list) and len(allowed) >= 2:
                finite_dimensions += 1
    if len(states) >= 3:
        finite_dimensions += 1

    combinatorial_model = (root / "specs/combinatorial-model.json").is_file() or _has_dir(
        root, ("tests/combinatorial", "test/combinatorial")
    )
    combinatorial_candidate = depth in {"domain", "formal"} and (finite_dimensions >= 3 or combinatorial_model)
    return True, depth, property_candidate, combinatorial_candidate, combinatorial_model


def detect_project_signals(root: Path | str) -> ProjectSignals:
    root = Path(root).resolve()
    package = _package(root)
    dependencies: dict[str, Any] = {}
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        value = package.get(key)
        if isinstance(value, dict):
            dependencies.update(value)

    dep_names = {str(name).lower() for name in dependencies}
    scripts = package.get("scripts") if isinstance(package.get("scripts"), dict) else {}
    script_names = {str(name).lower() for name in scripts}

    javascript = (root / "package.json").is_file()
    python = any((root / name).is_file() for name in ("pyproject.toml", "requirements.txt", "requirements-dev.txt", "setup.py"))
    tests = any((root / name).exists() for name in ("tests", "test", "__tests__")) or any(
        name.startswith("test") for name in script_names
    )
    playwright = any((root / name).is_file() for name in ("playwright.config.ts", "playwright.config.js", "playwright.config.mjs")) or "@playwright/test" in dep_names
    browser_extension = False
    manifest = _read_json(root / "manifest.json")
    if manifest.get("manifest_version") in {2, 3}:
        browser_extension = True

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
    web_ui = bool(dep_names & web_frameworks) or playwright or browser_extension

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

    github_workflows = _has_files(root, (".github/workflows/*.yml", ".github/workflows/*.yaml"))
    postgres_deps = {"pg", "postgres", "drizzle-orm", "prisma", "@prisma/client", "@supabase/supabase-js"}
    postgres = bool(dep_names & postgres_deps) or _has_dir(root, ("supabase", "drizzle", "prisma"))
    postgres_migrations = _has_files(
        root,
        (
            "migrations/**/*.sql",
            "drizzle/**/*.sql",
            "supabase/migrations/**/*.sql",
            "prisma/migrations/**/*.sql",
        ),
    )
    architecture_rules = "dependency-cruiser" in dep_names or _has_files(
        root,
        (
            ".dependency-cruiser.js",
            ".dependency-cruiser.cjs",
            ".dependency-cruiser.mjs",
            ".dependency-cruiser.ts",
            "dependency-cruiser.config.js",
            "dependency-cruiser.config.cjs",
            "dependency-cruiser.config.mjs",
            "dependency-cruiser.config.ts",
        ),
    )
    load_tests = _has_dir(root, ("tests/load", "tests/performance", "test/load", "performance", "k6")) or any(
        marker in name for name in script_names for marker in ("load", "perf", "k6")
    )
    restler_config = _has_dir(root, ("tests/restler", "restler", "restlerConfig")) or _has_files(
        root, ("**/restler*.json", "**/restler*.py")
    )

    semantic_assurance, semantic_depth, property_candidate, combinatorial_candidate, combinatorial_model = _semantic_signals(root)

    return ProjectSignals(
        javascript=javascript,
        python=python,
        tests=tests,
        web_ui=web_ui,
        playwright=playwright,
        browser_extension=browser_extension,
        openapi=openapi,
        graphql=graphql,
        api_contract=api_contract,
        github_workflows=github_workflows,
        postgres=postgres,
        postgres_migrations=postgres_migrations,
        architecture_rules=architecture_rules,
        load_tests=load_tests,
        restler_config=restler_config,
        semantic_assurance=semantic_assurance,
        semantic_depth=semantic_depth,
        property_candidate=property_candidate,
        combinatorial_candidate=combinatorial_candidate,
        combinatorial_model=combinatorial_model,
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
    external_integrations: bool = False,
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

    if signals.github_workflows and mode != "baseline":
        checks.append(_check(
            "ci-workflow-lint",
            "actionlint",
            "ci-correctness",
            required=True,
            trigger="pull_request",
            reason="Validate GitHub Actions syntax, expressions and workflow references before trusting CI as an executor.",
        ))
        checks.append(_check(
            "ci-workflow-security",
            "zizmor",
            "ci-security",
            required=mode in {"adversarial", "release"},
            trigger="pull_request",
            reason="Analyze GitHub Actions for injection, credential, permission and ref-security risks.",
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

    if signals.web_ui and signals.playwright and not signals.browser_extension and mode in {"adversarial", "release"}:
        checks.append(_check(
            "cross-browser-e2e",
            "Playwright Chromium + Firefox + WebKit",
            "browser-compatibility",
            required=mode == "release",
            trigger="release" if mode == "release" else "pull_request-selective",
            reason="Exercise critical browser flows across independent browser engines instead of validating Chromium only.",
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

    if api_mode == "governed" and signals.openapi and mode == "release":
        checks.append(_check(
            "api-stateful-deep",
            "Microsoft RESTler",
            "api-stateful-deep-fuzzing",
            required=signals.restler_config and RISK_RANK[risk] >= RISK_RANK["high"],
            trigger="release/nightly",
            reason="Escalate only complex governed REST APIs to deeper producer-consumer state exploration beyond the default API fuzzing layer.",
            safety="Use a disposable authorized environment; RESTler fuzz mode can be disruptive and is never aimed at production by inference.",
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

    if signals.property_candidate and mode != "baseline":
        property_required = signals.semantic_depth == "formal" or (
            mode == "release" and RISK_RANK[risk] >= RISK_RANK["high"]
        )
        if signals.javascript:
            checks.append(_check(
                "property-js",
                "fast-check",
                "domain-property-testing",
                required=property_required,
                trigger="pull_request-selective" if mode != "release" else "release",
                reason="Generate domain values and shrink counterexamples from semantic invariants, ranges or state rules.",
            ))
        if signals.python:
            checks.append(_check(
                "property-python",
                "Hypothesis",
                "domain-property-testing",
                required=property_required,
                trigger="pull_request-selective" if mode != "release" else "release",
                reason="Generate domain values/state sequences and shrink counterexamples from semantic invariants and constraints.",
            ))

    if signals.combinatorial_candidate and mode != "baseline":
        checks.append(_check(
            "combinatorial-testing",
            "NIST ACTS or equivalent covering-array generator",
            "combinatorial-testing",
            required=signals.combinatorial_model and mode in {"adversarial", "release"},
            trigger="pull_request-selective" if mode != "release" else "release",
            reason="Cover interactions among multiple finite configuration/domain dimensions without exhaustive test explosion.",
        ))

    if signals.postgres and signals.postgres_migrations and mode != "baseline":
        checks.append(_check(
            "postgres-migration-safety",
            "Squawk",
            "database-migration-safety",
            required=mode in {"adversarial", "release"},
            trigger="pull_request",
            reason="Detect PostgreSQL migration patterns that can create unsafe locks, availability regressions or incompatible schema changes.",
        ))

    if signals.javascript and mode != "baseline" and (
        signals.architecture_rules or SYSTEM_RANK[system_level] >= SYSTEM_RANK["multi-user-system"]
    ):
        checks.append(_check(
            "architecture-boundaries",
            "dependency-cruiser or equivalent architecture test",
            "architecture-conformance",
            required=signals.architecture_rules and mode in {"adversarial", "release"},
            trigger="pull_request",
            reason="Continuously enforce declared module/layer boundaries instead of relying on architecture documentation alone.",
        ))

    performance_candidate = SYSTEM_RANK[system_level] >= SYSTEM_RANK["production-system"] and (
        signals.web_ui or signals.api_contract
    )
    if (signals.load_tests and mode in {"adversarial", "release"}) or (performance_candidate and mode == "release"):
        checks.append(_check(
            "load-performance",
            "k6",
            "load-performance-reliability",
            required=signals.load_tests and mode == "release" and RISK_RANK[risk] >= RISK_RANK["high"],
            trigger="release" if mode == "release" else "pull_request-selective",
            reason="Exercise realistic concurrent workload and enforce only project-specific thresholds derived from SLOs or stable baselines.",
            safety="Use controlled test/preview infrastructure; do not generate load against third-party or production targets without explicit authorization.",
        ))

    if external_integrations and mode in {"adversarial", "release"}:
        checks.append(_check(
            "network-resilience",
            "Toxiproxy or equivalent fault proxy",
            "network-fault-resilience",
            required=mode == "release" and RISK_RANK[risk] >= RISK_RANK["high"],
            trigger="release" if mode == "release" else "pull_request-selective",
            reason="Verify timeout, retry, idempotency and degraded behavior under latency, disconnects and constrained network conditions.",
            safety="Inject faults only between the test system and controlled stubs/proxies; never degrade an external provider itself.",
        ))

    return {
        "schema_version": 2,
        "mode": mode,
        "free_only": True,
        "preferred_executor": "github_ci",
        "fallback_executor": "local_full/self-hosted-runner when GitHub-hosted capacity is unavailable",
        "risk": risk,
        "system_level": system_level,
        "api_mode": api_mode,
        "release": bool(release),
        "external_integrations": bool(external_integrations),
        "signals": signals.to_dict(),
        "checks": [check.to_dict() for check in checks],
        "required_check_ids": [check.check_id for check in checks if check.status == "required"],
        "advisory_check_ids": [check.check_id for check in checks if check.status == "advisory"],
        "rules": {
            "no_paid_ai_required": True,
            "no_active_scan_against_production_by_default": True,
            "no_load_against_unapproved_targets": True,
            "fault_injection_targets_controlled_dependencies_only": True,
            "tool_unavailable_is_not_pass": True,
            "semantic_review_remains_separate": True,
            "pin_versions_in_real_ci": True,
            "avoid_redundant_scanners": True,
            "ci_executor_must_be_verified_when_workflows_exist": True,
        },
    }
