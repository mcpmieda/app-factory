#!/usr/bin/env python3
"""Valida o adaptador Codex Plugin da App Factory usando apenas a stdlib."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def stop(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        stop(f"arquivo ausente: {path.relative_to(ROOT)}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        stop(f"JSON inválido em {path.relative_to(ROOT)}: {error}")
    if not isinstance(payload, dict):
        stop(f"objeto JSON esperado em {path.relative_to(ROOT)}")
    return payload


def non_empty_string(payload: dict[str, Any], field: str, location: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        stop(f"{location}.{field} deve ser string não vazia")
    return value


def validate_manifest() -> dict[str, Any]:
    manifest = read_json(MANIFEST_PATH)
    name = non_empty_string(manifest, "name", "plugin.json")
    if not NAME_RE.fullmatch(name):
        stop("plugin.json.name deve usar kebab-case")

    version = non_empty_string(manifest, "version", "plugin.json")
    if not SEMVER_RE.fullmatch(version):
        stop("plugin.json.version deve usar SemVer estrito")

    non_empty_string(manifest, "description", "plugin.json")
    author = manifest.get("author")
    if not isinstance(author, dict):
        stop("plugin.json.author deve ser objeto")
    non_empty_string(author, "name", "plugin.json.author")

    skills_path = non_empty_string(manifest, "skills", "plugin.json")
    if skills_path != "./skills/" or not (ROOT / "skills").is_dir():
        stop("plugin.json.skills deve apontar para ./skills/ na raiz")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        stop("plugin.json.interface deve ser objeto")
    for field in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
    ):
        non_empty_string(interface, field, "plugin.json.interface")

    capabilities = interface.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities or not all(
        isinstance(item, str) and item.strip() for item in capabilities
    ):
        stop("plugin.json.interface.capabilities deve ser lista não vazia de strings")

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        stop("plugin.json.interface.defaultPrompt deve conter de 1 a 3 prompts")
    if not all(isinstance(item, str) and 0 < len(item) <= 128 for item in prompts):
        stop("cada defaultPrompt deve ser string não vazia de até 128 caracteres")

    return manifest


def validate_marketplace(plugin_name: str) -> None:
    marketplace = read_json(MARKETPLACE_PATH)
    non_empty_string(marketplace, "name", "marketplace.json")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list):
        stop("marketplace.json.plugins deve ser lista")

    matches = [entry for entry in entries if isinstance(entry, dict) and entry.get("name") == plugin_name]
    if len(matches) != 1:
        stop(f"marketplace deve conter exatamente uma entrada para {plugin_name}")
    entry = matches[0]
    source = entry.get("source")
    if not isinstance(source, dict) or source.get("source") != "local":
        stop("marketplace deve usar source local")
    if source.get("path") != "./":
        stop("marketplace deve apontar para ./ e reutilizar a raiz sem cópia")

    policy = entry.get("policy")
    if not isinstance(policy, dict):
        stop("marketplace policy deve ser objeto")
    if policy.get("installation") not in {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}:
        stop("marketplace policy.installation inválida")
    if policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
        stop("marketplace policy.authentication inválida")
    non_empty_string(entry, "category", "marketplace.plugins[app-factory]")


def main() -> int:
    manifest = validate_manifest()
    validate_marketplace(manifest["name"])
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    print(
        "OK: manifest, marketplace local e "
        f"{len(skills)} Skills validados sem duplicação."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
