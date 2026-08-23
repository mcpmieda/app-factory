#!/usr/bin/env python3
"""Validate Change Hygiene policy, scanner behavior and Factory wiring."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "core/CHANGE_HYGIENE.md",
    "scripts/change_hygiene.py",
    "scripts/validate_change_hygiene.py",
    "tests/change_hygiene/test_change_hygiene.py",
    "research/CHANGE_HYGIENE_RESEARCH.md",
    "skills/maintenance/SKILL.md",
    "core/PRINCIPLES.md",
    "core/DEFINITION_OF_DONE.md",
    ".github/workflows/validate-change-hygiene.yml",
]

MARKERS = {
    "core/CHANGE_HYGIENE.md": [
        "preservar comportamento estável não significa preservar implementação obsoleta",
        "Um caminho ativo por responsabilidade",
        "Substituir, não sombrear",
        "Consolidação após repair loop",
        "Compatibilidade é exceção explícita",
        "CSS: corrigir a causa antes da cascata",
        "Knip",
        "Vulture",
        "jscpd",
        "projetos externos",
    ],
    "skills/maintenance/SKILL.md": [
        "core/CHANGE_HYGIENE.md",
        "Preserve **comportamento**, não implementação obsoleta",
        "Consolidação obrigatória",
        "scripts/change_hygiene.py",
        "net code health da área tocada",
    ],
    "core/PRINCIPLES.md": [
        "Preservar comportamento, não implementação obsoleta",
        "A árvore final não é o histórico de tentativas",
    ],
    "core/DEFINITION_OF_DONE.md": [
        "Change Hygiene em sistemas existentes",
        "shadow implementations",
        "scripts/change_hygiene.py",
        "Manutenção não termina apenas porque o bug sumiu",
    ],
    "scripts/change_hygiene.py": [
        "tracked-temporary-artifact",
        "possible-shadow-copy",
        "new-suppression",
        "css-important-added",
        "temporary-debt-marker",
        "heuristics_are_advisory",
        "shell=False",
    ],
    "research/CHANGE_HYGIENE_RESEARCH.md": [
        "Google Engineering Practices",
        "Chromium",
        "Microsoft Engineering Fundamentals Playbook",
        "ESLint",
        "Knip",
        "Stylelint",
        "Ruff / Vulture",
        "jscpd",
        "net code health",
    ],
}


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def validate_files_and_markers() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail("Change Hygiene files missing: " + ", ".join(missing))
    for path, markers in MARKERS.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        missing_markers = [marker for marker in markers if marker not in text]
        if missing_markers:
            fail(f"{path} missing Change Hygiene markers: {missing_markers}")


def run_tests() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests/change_hygiene",
            "-p",
            "test_*.py",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
        shell=False,
    )
    if completed.returncode != 0:
        fail((completed.stdout + "\n" + completed.stderr).strip())


def main() -> int:
    validate_files_and_markers()
    run_tests()
    print("OK: Change Hygiene contract, deterministic scanner and consolidation rules validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
