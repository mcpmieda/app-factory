#!/usr/bin/env python3
"""Validate Independent Verification policy, deterministic planning and Factory wiring."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.independent_verification import build_independent_verification_plan  # noqa: E402


REQUIRED_FILES = [
    "core/INDEPENDENT_VERIFICATION.md",
    "engine/independent_verification.py",
    "scripts/independent_verification.py",
    "skills/independent-verification/SKILL.md",
    "templates/project/VERIFICATION.md",
    "templates/verification/README.md",
    "research/VERIFICATION_ENRICHMENT_RESEARCH.md",
    ".github/workflows/validate-independent-verification.yml",
]

WIRING_MARKERS = {
    "AGENTS.md": ["INDEPENDENT_VERIFICATION.md", "independent-verification", "gratuitas/open source"],
    "core/ENTRYPOINT.md": ["Verificação independente", "baseline", "adversarial"],
    "core/WORKFLOW.md": ["INDEPENDENT_VERIFICATION.md", "required/advisory"],
    "core/DEFINITION_OF_DONE.md": ["Independent Verification", "mutation testing", "OWASP ZAP"],
    "core/EXECUTION_FABRIC.md": ["Independent Verification", "github_ci"],
    "core/SEMANTIC_VERIFICATION.md": ["Independent Verification", "não substitui"],
    "core/SEMANTIC_ASSURANCE.md": ["property-based", "NIST ACTS"],
    "core/TASK_ROUTER.md": ["actionlint", "Toxiproxy", "k6"],
    "skills/api-engineering/SKILL.md": ["independent-verification", "Schemathesis/DAST"],
    "skills/security-review/SKILL.md": ["Independent Verification", "threat model"],
    "skills/app-planner/SKILL.md": ["Independent Verification", "gratuitos/open source", "carga", "resiliência"],
    "skills/factory-router/SKILL.md": ["independent-verification", "adversarial"],
    "skills/verification/SKILL.md": ["independent-verification", "mutation"],
    "skills/semantic-assurance/SKILL.md": ["NIST ACTS", "fast-check", "Hypothesis"],
    "templates/project/AGENTS.md": ["INDEPENDENT_VERIFICATION.md", "VERIFICATION.md"],
    "templates/project/ARCHITECTURE.md": ["Independent Verification", "VERIFICATION.md"],
    "templates/project/PROJECT_STATE.md": ["Independent Verification", "checks independentes obrigatórios"],
    "templates/project/VERIFICATION.md": ["actionlint", "Squawk", "Toxiproxy", "NIST ACTS"],
    "profiles/web-admin/PROFILE.md": ["Independent Verification", "adversarial"],
    "profiles/web-app/PROFILE.md": ["Independent Verification", "adversarial"],
    "profiles/automation/PROFILE.md": ["Independent Verification", "mutmut"],
    "profiles/website/PROFILE.md": ["Independent Verification", "Lighthouse CI"],
    "profiles/chrome-extension/PROFILE.md": ["Independent Verification", "StrykerJS"],
    "PORTABILITY.md": ["Independent Verification portátil", "free-only"],
    "APP_FACTORY_PLAN.md": ["Independent Verification", "free-only"],
    "PROJECT_STATE.md": ["Independent Verification", "19", "actionlint", "NIST ACTS"],
    "README.md": ["Independent Verification", "19 Skills"],
    "docs/CODEX_PLUGIN.md": ["Independent Verification", "19 Skills"],
    "docs/DECISIONS.md": ["D-045", "D-052", "Independent Verification", "actionlint", "NIST ACTS"],
    ".codex-plugin/plugin.json": ["independent verification", "free/open-source"],
}

PRESERVE = [
    "engine/context_engine.py",
    "engine/autonomy_engine.py",
    "engine/execution_engine.py",
    "engine/ci_executor.py",
    "engine/learning_engine.py",
    "engine/semantic_verification.py",
    "engine/semantic_assurance.py",
    "engine/review_packet.py",
    "skills/api-engineering/SKILL.md",
    "starters/web-admin/recipes/auth-better-auth",
    "starters/web-admin/recipes/database-drizzle-postgres",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def assert_plan(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def write_package(
    root: Path,
    *,
    react: bool = False,
    playwright: bool = False,
    tests: bool = True,
    postgres: bool = False,
    architecture_rules: bool = False,
) -> None:
    dependencies: dict[str, str] = {}
    dev_dependencies: dict[str, str] = {}
    if react:
        dependencies.update({"react": "0.0.0", "react-dom": "0.0.0"})
    if playwright:
        dev_dependencies["@playwright/test"] = "0.0.0"
    if postgres:
        dependencies["pg"] = "0.0.0"
    if architecture_rules:
        dev_dependencies["dependency-cruiser"] = "0.0.0"
    scripts = {"test": "echo test"} if tests else {}
    (root / "package.json").write_text(
        json.dumps({"scripts": scripts, "dependencies": dependencies, "devDependencies": dev_dependencies}),
        encoding="utf-8",
    )
    if tests:
        (root / "tests").mkdir(exist_ok=True)
    if playwright:
        (root / "playwright.config.ts").write_text("export default {};\n", encoding="utf-8")


def write_workflow(root: Path) -> None:
    target = root / ".github/workflows"
    target.mkdir(parents=True, exist_ok=True)
    (target / "ci.yml").write_text("name: CI\non: [push]\njobs: {}\n", encoding="utf-8")


def write_semantics(root: Path, *, combinatorial_model: bool = False) -> None:
    specs = root / "specs"
    specs.mkdir(parents=True, exist_ok=True)
    (specs / "semantic-contract.json").write_text(
        json.dumps({"invariants": [{"id": "INV-001", "text": "state remains valid"}]}),
        encoding="utf-8",
    )
    constraints = [
        {"id": "CON-001", "kind": "enum", "allowed": ["a", "b"], "forbidden": []},
        {"id": "CON-002", "kind": "enum", "allowed": ["x", "y"], "forbidden": []},
        {"id": "CON-003", "kind": "enum", "allowed": ["on", "off"], "forbidden": []},
    ]
    (specs / "semantic-assurance.json").write_text(
        json.dumps({"depth": "domain", "constraints": constraints, "states": [], "transitions": []}),
        encoding="utf-8",
    )
    if combinatorial_model:
        (specs / "combinatorial-model.json").write_text("{}\n", encoding="utf-8")


def validate_planner() -> None:
    # A simple legitimate local app must stay light.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        write_package(root, tests=False)
        plan = build_independent_verification_plan(
            root,
            risk="low",
            system_level="local-app",
            api_mode="none",
        )
        assert_plan(plan["mode"] == "baseline", "low-risk local app must remain baseline")
        assert_plan(plan["checks"] == [], "baseline app must not receive heavyweight scanners by default")

    # A robust web + API system must gain adversarial evidence and verify its own CI.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        write_package(root, react=True, playwright=True, tests=True)
        write_workflow(root)
        (root / "api").mkdir()
        (root / "api/openapi.yaml").write_text("openapi: 3.1.0\ninfo:\n  title: test\n  version: 1\npaths: {}\n", encoding="utf-8")
        plan = build_independent_verification_plan(
            root,
            risk="high",
            system_level="multi-user-system",
            api_mode="contract",
        )
        ids = {item["id"]: item for item in plan["checks"]}
        assert_plan(plan["mode"] == "adversarial", "high-risk multi-user app must be adversarial")
        for check_id in (
            "supply-chain",
            "sast",
            "ci-workflow-lint",
            "ci-workflow-security",
            "accessibility",
            "cross-browser-e2e",
            "api-property-testing",
            "dast-baseline",
            "mutation-js",
            "architecture-boundaries",
        ):
            assert_plan(check_id in ids, f"robust web/API plan missing {check_id}")
        assert_plan(ids["ci-workflow-lint"]["status"] == "required", "actionlint must protect selected CI")
        assert_plan(ids["dast-baseline"]["status"] == "required", "DAST baseline must block adversarial web plan")
        assert_plan(plan["preferred_executor"] == "github_ci", "GitHub CI must be preferred deterministic executor")
        assert_plan(plan["free_only"] is True, "independent layer must remain free-only")

    # Domain semantics should generate property/combinatorial testing without making them universal.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        write_package(root, tests=True)
        write_semantics(root, combinatorial_model=True)
        plan = build_independent_verification_plan(
            root,
            risk="high",
            system_level="multi-user-system",
            api_mode="none",
        )
        ids = {item["id"]: item for item in plan["checks"]}
        assert_plan("property-js" in ids, "domain JS system with invariants must select fast-check")
        assert_plan("combinatorial-testing" in ids, "finite semantic dimensions must select combinatorial testing")
        assert_plan(ids["combinatorial-testing"]["status"] == "required", "materialized combinatorial model must become executable evidence")

    # PostgreSQL migrations and architecture rules gain focused checks instead of generic extra scanners.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        write_package(root, tests=True, postgres=True, architecture_rules=True)
        migrations = root / "migrations"
        migrations.mkdir()
        (migrations / "001.sql").write_text("ALTER TABLE users ADD COLUMN active boolean;\n", encoding="utf-8")
        plan = build_independent_verification_plan(
            root,
            risk="high",
            system_level="multi-user-system",
            api_mode="none",
        )
        ids = {item["id"]: item for item in plan["checks"]}
        assert_plan(ids["postgres-migration-safety"]["tool"] == "Squawk", "PostgreSQL migration safety must use Squawk by default")
        assert_plan(ids["postgres-migration-safety"]["status"] == "required", "high-risk PostgreSQL migrations must block on safety lint")
        assert_plan(ids["architecture-boundaries"]["status"] == "required", "declared architecture boundaries must be enforced")

    # Production release can add load, fault-injection and cross-browser checks without inventing thresholds.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        write_package(root, react=True, playwright=True, tests=True)
        (root / "tests/load").mkdir(parents=True)
        (root / "tests/load/smoke.js").write_text("export default function () {}\n", encoding="utf-8")
        plan = build_independent_verification_plan(
            root,
            risk="high",
            system_level="production-system",
            api_mode="none",
            release=True,
            external_integrations=True,
        )
        ids = {item["id"]: item for item in plan["checks"]}
        for check_id in ("dast-active", "web-quality", "mutation-js", "cross-browser-e2e", "load-performance", "network-resilience"):
            assert_plan(check_id in ids, f"release plan missing {check_id}")
        assert_plan(ids["load-performance"]["status"] == "required", "declared high-risk release load tests must block")
        assert_plan(ids["network-resilience"]["status"] == "required", "material external integrations need release resilience evidence")
        assert_plan(plan["rules"]["no_load_against_unapproved_targets"] is True, "load safety guard missing")

    # RESTler is escalation for governed REST APIs, not a Schemathesis replacement.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        write_package(root, tests=True)
        (root / "api").mkdir()
        (root / "api/openapi.yaml").write_text("openapi: 3.1.0\ninfo:\n  title: test\n  version: 1\npaths: {}\n", encoding="utf-8")
        (root / "tests/restler").mkdir(parents=True)
        plan = build_independent_verification_plan(
            root,
            risk="high",
            system_level="production-system",
            api_mode="governed",
            release=True,
        )
        ids = {item["id"]: item for item in plan["checks"]}
        assert_plan("api-property-testing" in ids, "Schemathesis remains the primary contract fuzz gate")
        assert_plan("api-stateful-deep" in ids, "governed REST release may escalate to RESTler")
        assert_plan(ids["api-stateful-deep"]["status"] == "required", "materialized RESTler config must make deep fuzz executable")

    # Python receives Hypothesis and mutmut when semantics/risk justify them.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        (root / "requirements.txt").write_text("pytest==0\n", encoding="utf-8")
        (root / "tests").mkdir()
        write_semantics(root)
        plan = build_independent_verification_plan(
            root,
            risk="critical",
            system_level="critical-system",
            api_mode="none",
            release=True,
        )
        ids = {item["id"] for item in plan["checks"]}
        assert_plan("mutation-python" in ids, "critical Python release must select Python mutation tooling")
        assert_plan("property-python" in ids, "semantic Python domain must select Hypothesis")
        assert_plan("mutation-js" not in ids, "Python-only project must not receive JS mutation tooling")


def validate_wiring() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("Independent Verification files missing: " + ", ".join(missing))

    for path, markers in WIRING_MARKERS.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        lowered = text.lower()
        missing_markers = [marker for marker in markers if marker.lower() not in lowered]
        if missing_markers:
            fail(f"{path} missing Independent Verification markers: {missing_markers}")

    for path in PRESERVE:
        if not (ROOT / path).exists():
            fail(f"regression guard: existing capability missing: {path}")

    core = (ROOT / "core/INDEPENDENT_VERIFICATION.md").read_text(encoding="utf-8")
    for marker in (
        "free-only",
        "StrykerJS",
        "mutmut",
        "Schemathesis",
        "RESTler",
        "OWASP ZAP",
        "Semgrep Community Edition",
        "Opengrep",
        "Trivy",
        "axe-core",
        "Lighthouse CI",
        "actionlint",
        "zizmor",
        "Hypothesis",
        "fast-check",
        "NIST ACTS",
        "Squawk",
        "k6",
        "Toxiproxy",
        "dependency-cruiser",
        "não entendem sozinhos a intenção",
        "não exigir segunda API/modelo de IA pago",
        "active/full scan",
        "não rodar ferramentas redundantes",
    ):
        if marker.lower() not in core.lower():
            fail(f"Independent Verification contract missing marker: {marker}")

    workflow = (ROOT / ".github/workflows/validate-independent-verification.yml").read_text(encoding="utf-8")
    for marker in ("permissions:", "contents: read", "timeout-minutes", "validate_independent_verification.py"):
        if marker not in workflow:
            fail(f"Independent Verification CI safety marker missing: {marker}")

    plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if plugin.get("version") != "1.4.0":
        fail("Independent Verification enrichment is governance hardening and must not invent a V1.5 plugin version")


def main() -> int:
    validate_planner()
    validate_wiring()
    print("OK: enriched Independent Verification planning, free-only diverse tooling, safety and Factory-wide wiring validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
