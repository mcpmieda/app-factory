#!/usr/bin/env python3
"""Valida regras essenciais de skills/*/SKILL.md sem dependências externas."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def stop(message: str) -> None:
    print("ERROR:", message)
    raise SystemExit(1)


def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return {}


def validate(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    fields = frontmatter(text)
    name = fields.get("name", "")
    description = fields.get("description", "")
    compatibility = fields.get("compatibility", "")

    if not name:
        stop(f"name ausente em {path.relative_to(ROOT)}")
    if len(name) > 64 or not NAME_RE.fullmatch(name):
        stop(f"name inválido em {path.relative_to(ROOT)}: {name!r}")
    if name != path.parent.name:
        stop(f"name deve ser igual ao diretório em {path.relative_to(ROOT)}")
    if not description or len(description) > 1024:
        stop(f"description ausente ou longa demais em {path.relative_to(ROOT)}")
    if compatibility and len(compatibility) > 500:
        stop(f"compatibility longa demais em {path.relative_to(ROOT)}")
    if len(text.splitlines()) > 500:
        print(f"WARN: {path.relative_to(ROOT)} excede 500 linhas; mova detalhes para references/.")


def main() -> int:
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skills:
        stop("nenhuma Skill encontrada")
    for skill in skills:
        validate(skill)
    print(f"OK: {len(skills)} Skills seguem as restrições essenciais do Agent Skills spec.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
