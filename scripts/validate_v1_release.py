#!/usr/bin/env python3
"""Small V1 release preflight composed with the existing executable gates."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MAX_TRACKED_BYTES = 5 * 1024 * 1024
FORBIDDEN_PARTS = {
    "node_modules",
    ".next",
    "coverage",
    "playwright-report",
    "test-results",
}
SECRET_PATTERNS = {
    "AWS access key": re.compile(rb"AKIA[0-9A-Z]{16}"),
    "GitHub classic token": re.compile(rb"ghp_[A-Za-z0-9]{36}"),
    "private key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def stop(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def candidate_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / raw.decode("utf-8") for raw in result.stdout.split(b"\0") if raw]


def validate_repository_hygiene() -> None:
    for path in candidate_files():
        relative = path.relative_to(ROOT)
        if any(part in FORBIDDEN_PARTS for part in relative.parts):
            stop(f"generated artifact is tracked or pending: {relative}")
        if path.suffix.lower() in {".db", ".sqlite", ".sqlite3"}:
            stop(f"database artifact is tracked or pending: {relative}")
        if not path.is_file():
            continue
        size = path.stat().st_size
        if size > MAX_TRACKED_BYTES:
            stop(f"file exceeds 5 MiB release limit: {relative} ({size} bytes)")
        if size > 1_000_000:
            continue
        contents = path.read_bytes()
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(contents):
                stop(f"possible {label} in {relative}")


def validate_version_coherence() -> None:
    manifest = json.loads(
        (ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    version = manifest.get("version")
    if not isinstance(version, str) or not version.startswith("1.0.0"):
        stop("plugin manifest must identify the V1.0 release line")

    expected_baseline = f"v{version}"
    template = ROOT / "starters/web-admin/template"
    template_metadata = json.loads(
        (template / ".factory-template.json").read_text(encoding="utf-8")
    )
    if template_metadata.get("factoryBaseline") != expected_baseline:
        stop(
            "web-admin template baseline diverges from plugin version: "
            f"{template_metadata.get('factoryBaseline')} != {expected_baseline}"
        )

    required_markers = {
        template / "PROJECT_STATE.md": f"Factory baseline: `{expected_baseline}`",
        template / "src/config/project.ts": f'factoryBaseline: "{expected_baseline}"',
        template / "src/config/project.test.ts": f'factoryBaseline: "{expected_baseline}"',
        ROOT / "README.md": version,
        ROOT / "PROJECT_STATE.md": "V1.0 release candidate",
    }
    for path, marker in required_markers.items():
        if marker not in path.read_text(encoding="utf-8"):
            stop(f"version marker {marker!r} missing from {path.relative_to(ROOT)}")


def validate_composed_gates() -> None:
    required_workflows = {
        ".github/workflows/validate-factory.yml": "validate_plugin.py",
        ".github/workflows/validate-web-admin-starter.yml": "generated-postgres-auth",
        ".github/workflows/validate-living-ui.yml": "End-to-end desktop, mobile and reduced motion",
        ".github/workflows/validate-universal-pilots.yml": "chrome-extension",
        ".github/workflows/validate-web-admin-pilot.yml": "npm run e2e",
        ".github/workflows/validate-v1-release.yml": "validate_v1_bootstrap.py",
    }
    for raw_path, marker in required_workflows.items():
        path = ROOT / raw_path
        if not path.is_file() or marker not in path.read_text(encoding="utf-8"):
            stop(f"release gate missing {marker!r} in {raw_path}")

    project = ROOT / "audits/v1-final/equipment-loans"
    required_project_files = [
        "README.md",
        "PROJECT_STATE.md",
        "ARCHITECTURE.md",
        "src/features/loans/domain.ts",
        "src/features/loans/repository.ts",
        "tests/e2e/equipment-loans.spec.ts",
    ]
    for relative in required_project_files:
        if not (project / relative).is_file():
            stop(f"final audit project is missing {relative}")

    package = json.loads((project / "package.json").read_text(encoding="utf-8"))
    scripts = package.get("scripts", {})
    for script in ("format:check", "lint", "typecheck", "test:coverage", "build", "e2e"):
        if script not in scripts:
            stop(f"final audit project is missing npm script {script}")
    dependencies = {**package.get("dependencies", {}), **package.get("devDependencies", {})}
    if "better-auth" in dependencies:
        stop("final audit project must not invent authentication")


def main() -> int:
    validate_repository_hygiene()
    validate_version_coherence()
    validate_composed_gates()
    print("OK: V1 version coherence, gate composition, final project contract, secrets and artifacts validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
