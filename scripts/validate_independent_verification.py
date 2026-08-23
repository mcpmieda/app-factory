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
    ".github/workflows/validate-independent-verification.yml",
]

WIRING_MARKERS = {
    "AGENTS.md": ["INDEPENDENT_VERIFICATION.md", "independent-verification", "free"],
    "core/ENTRYPOINT.md": ["Verificação independente", "baseline", "adversarial"],
    "core/WORKFLOW.md": ["INDEPENDENT_VERIFICATION.md", "required/advisory"],
    "core/DEFINITION_OF_DONE.md": ["Independent Verification", "mutation testing", "OWASP ZAP"],
    "core/EXECUTION_FABRIC.md": ["Independent Verification", "github_ci"],
    "core/SEMANTIC_VERIFICATION.md": ["Independent Verification", "não substitui"],
    "skills/api-engineering/SKILL.md": ["independent-verification", "Schemathesis/DAST"],
    "skills/security-review/SKILL.md": ["Independent Verification", "threat model"],
    "skills/app-planner/SKILL.md": ["Independent Verification", "free"],
    "skills/factory-router/SKILL.md": ["independent-verification", "adversarial"],
    "skills/verification/SKILL.md": ["independent-verification", "mutation"],
    "templates/project/AGENTS.md": ["INDEPENDENT_VERIFICATION.md", "VERIFICATION.md"],
    "templates/project/ARCHITECTURE.md": ["Independent Verification", "VERIFICATION.md"],
    "templates/project/PROJECT_STATE.md": ["Independent Verification", "checks independentes obrigatórios"],
    "profiles/web-admin/PROFILE.md": ["Independent Verification", "adversarial"],
    "profiles/web-app/PROFILE.md": ["Independent Verification", "adversarial"],
    "profiles/automation/PROFILE.md": ["Independent Verification", "mutmut"],
    "profiles/website/PROFILE.md": ["Independent Verification", "Lighthouse CI"],
    "profiles/chrome-extension/PROFILE.md": ["Independent Verification", "StrykerJS"],
    "PORTABILITY.md": ["Independent Verification portátil", "free-only"],
    "APP_FACTORY_PLAN.md": ["Independent Verification", "free-only"],
    "PROJECT_STATE.md": ["Independent Verification", "18"],
    "README.md": ["Independent Verification", "18 Skills"],
    "docs/CODEX_PLUGIN.md": ["Independent Verification", "18 Skills"],
    "docs/DECISIONS.md": ["D-045", "D-052", "Independent Verification"],
    ".codex-plugin/plugin.json": ["independent verification", "free/open-source"],
}

PRESERVE = [
    "engine/context_engine.py",
    "engine/autonomy_engine.py",
    "engine/execution_engine.py",
    "engine/ci_executor.py",
    "engine/learning_engine.py",
    "engine/semantic_verification.py",
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


def write_package(root: Path, *, react: bool = False, playwright: bool = False, tests: bool = True) -> None:
    dependencies: dict[str, str] = {}
    dev_dependencies: dict[str, str] = {}
    if react:
        dependencies.update({"react": "0.0.0", "react-dom": "0.0.0"})
    if playwright:
        dev_dependencies["@playwright/test"] = "0.0.0"
    scripts = {"test": "echo test"} if tests else {}
    (root / "package.json").write_text(
        json.dumps({"scripts": scripts, "dependencies": dependencies, "devDependencies": dev_dependencies}),
        encoding="utf-8",
    )
    if tests:
        (root / "tests").mkdir(exist_ok=True)


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

    # A robust web + API system must gain adversarial evidence independently from hand-written tests.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        write_package(root, react=True, playwright=True, tests=True)
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
        for check_id in ("supply-chain", "sast", "accessibility", "api-property-testing", "dast-baseline", "mutation-js"):
            assert_plan(check_id in ids, f"robust web/API plan missing {check_id}")
        assert_plan(ids["dast-baseline"]["status"] == "required", "DAST baseline must block adversarial web plan")
        assert_plan(plan["preferred_executor"] == "github_ci", "GitHub CI must be preferred deterministic executor")
        assert_plan(plan["free_only"] is True, "independent layer must remain free-only")

    # Production release increases depth but does not invent arbitrary universal scores.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        write_package(root, react=True, playwright=True, tests=True)
        plan = build_independent_verification_plan(
            root,
            risk="high",
            system_level="production-system",
            api_mode="none",
            release=True,
        )
        ids = {item["id"]: item for item in plan["checks"]}
        assert_plan(plan["mode"] == "release", "production release must use release mode")
        for check_id in ("dast-active", "web-quality", "mutation-js"):
            assert_plan(check_id in ids, f"release plan missing {check_id}")
        assert_plan(ids["dast-active"]["status"] == "required", "high-risk release active DAST must be required")
        assert_plan(ids["mutation-js"]["status"] == "required", "high-risk release mutation must be required")
        assert_plan(plan["rules"]["no_active_scan_against_production_by_default"] is True, "active scan safety guard missing")

    # Python receives its own mature mutation default instead of JS tooling.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        (root / "requirements.txt").write_text("pytest==0\n", encoding="utf-8")
        (root / "tests").mkdir()
        plan = build_independent_verification_plan(
            root,
            risk="critical",
            system_level="critical-system",
            api_mode="none",
            release=True,
        )
        ids = {item["id"] for item in plan["checks"]}
        assert_plan("mutation-python" in ids, "critical Python release must select Python mutation tooling")
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
        "OWASP ZAP",
        "Semgrep Community Edition",
        "Trivy",
        "axe-core",
        "Lighthouse CI",
        "não entendem sozinhos a intenção",
        "não exigir segunda API/modelo de IA pago",
        "active/full scan",
    ):
        if marker.lower() not in core.lower():
            fail(f"Independent Verification contract missing marker: {marker}")

    workflow = (ROOT / ".github/workflows/validate-independent-verification.yml").read_text(encoding="utf-8")
    for marker in ("permissions:", "contents: read", "timeout-minutes", "validate_independent_verification.py"):
        if marker not in workflow:
            fail(f"Independent Verification CI safety marker missing: {marker}")

    plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    if plugin.get("version") != "1.4.0":
        fail("Independent Verification is governance hardening and must not invent a V1.5 plugin version")


def main() -> int:
    validate_planner()
    validate_wiring()
    print("OK: Independent Verification planning, free-only adversarial tooling, safety and Factory-wide wiring validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
