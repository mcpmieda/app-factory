#!/usr/bin/env python3
"""Minimal structural validation for the opt-in App Factory core."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "AGENTS.md",
    "core/ENTRYPOINT.md",
    "skills/factory-router/SKILL.md",
]

SKILL_HEADER = re.compile(
    r"^---\s*\n(?:(?!^---$).)*?^name:\s*.+$.*?^description:\s*.+$.*?^---$",
    re.MULTILINE | re.DOTALL,
)


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        fail("Required core files missing: " + ", ".join(missing))

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    entrypoint = (ROOT / "core/ENTRYPOINT.md").read_text(encoding="utf-8")
    router = (ROOT / "skills/factory-router/SKILL.md").read_text(encoding="utf-8")

    if "opcional" not in agents.lower() and "opt-in" not in agents.lower():
        fail("AGENTS.md must state that App Factory governance is optional")
    if "explicit" not in entrypoint.lower() or "opt" not in entrypoint.lower():
        fail("core/ENTRYPOINT.md must preserve explicit opt-in activation")
    if not SKILL_HEADER.search(router):
        fail("factory-router SKILL.md is missing valid frontmatter")

    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        if not SKILL_HEADER.search(text):
            fail(f"Invalid skill frontmatter: {skill.relative_to(ROOT)}")

    print("OK: App Factory opt-in core structure is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
