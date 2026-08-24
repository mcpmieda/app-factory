"""Durable App Factory project-adoption gate.

The gate prevents a project from claiming App Factory governance while skipping
routing, UI, semantic, or verification decisions until after implementation.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

AGENTS_START = "<!-- APP-FACTORY:ADOPTION:START -->"
AGENTS_END = "<!-- APP-FACTORY:ADOPTION:END -->"
STATE_START = "<!-- APP-FACTORY:ADOPTION:START -->"
STATE_END = "<!-- APP-FACTORY:ADOPTION:END -->"

SYSTEM_LEVELS = [
    "website",
    "local-app",
    "persistent-app",
    "multi-user-system",
    "production-system",
    "critical-system",
]
SCALES = {"S", "M", "L", "XL"}
RISKS = {"low", "medium", "high", "critical"}
API_MODES = {"none", "lightweight", "contract", "governed"}
SEMANTIC_MODES = {"required", "not-required"}
SEMANTIC_DEPTHS = {"none", "scenario", "domain", "formal"}
INDEPENDENT_MODES = {"baseline", "independent", "adversarial", "release"}
AD_HOC_DESIGN_SYSTEMS = {
    "custom",
    "native",
    "plain css",
    "css",
    "css/html",
    "html/css",
    "hand-rolled",
    "hand rolled",
    "react + css",
    "react+css",
}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _replace_managed_block(text: str, block: str) -> str:
    if AGENTS_START in text and AGENTS_END in text:
        before, remainder = text.split(AGENTS_START, 1)
        _, after = remainder.split(AGENTS_END, 1)
        return f"{before.rstrip()}\n\n{block}\n{after.lstrip()}".rstrip() + "\n"
    return f"{text.rstrip()}\n\n{block}\n" if text.strip() else f"{block}\n"


def _agents_block() -> str:
    return "\n".join(
        [
            AGENTS_START,
            "## App Factory adoption gate",
            "",
            "This repository is governed by **App Factory** (`mcpmieda/app-factory`).",
            "Use `factory-router` for software-development work and read `core/PROJECT_ADOPTION_GATE.md` before material implementation.",
            "Run the `pre-implementation` adoption gate before the first functional/visual code change in a new material block.",
            "Do not retrofit routing, design-system choice, semantic contracts, or verification strategy only after implementation.",
            AGENTS_END,
        ]
    )


def _state_block(config: dict[str, Any]) -> str:
    routing = config["routing"]
    ui = config["ui"]
    lines = [
        STATE_START,
        "## App Factory Adoption",
        "",
        f"- governance: `app-factory`;",
        f"- factory baseline: `{config['factoryBaseline']}`;",
        f"- adoption mode: `{config['adoption']['mode']}`;",
        f"- scale: `{routing['scale']}`;",
        f"- risk: `{routing['risk']}`;",
        f"- system level: `{routing['systemLevel']}`;",
        f"- profile: `{routing['profile']}`;",
        f"- API mode: `{routing['apiMode']}`;",
        f"- Semantic Verification: `{routing['semanticVerification']}` / depth `{routing['semanticDepth']}`;",
        f"- Independent Verification: `{routing['independentVerification']}`;",
    ]
    if routing.get("authoritativeData"):
        lines.append(f"- authoritative data: {routing['authoritativeData']};")
    if routing.get("identity"):
        lines.append(f"- identity: {routing['identity']};")
    if routing.get("authorization"):
        lines.append(f"- authorization: {routing['authorization']};")
    if routing.get("recovery"):
        lines.append(f"- recovery: {routing['recovery']};")
    if ui.get("enabled"):
        lines.extend(
            [
                f"- design system: `{ui['designSystem']}`;",
                f"- Professional UI Profile: `{ui['professionalUiProfile']}`;",
                f"- Motion Profile: `{ui['motionProfile']}`;",
            ]
        )
        if ui.get("ambientSurfaceProfile"):
            lines.append(f"- Ambient Surface Profile: `{ui['ambientSurfaceProfile']}`;")
        if ui.get("constellationIntensity"):
            lines.append(f"- Constellation Intensity: `{ui['constellationIntensity']}`;")
        if ui.get("deviation"):
            lines.append(f"- UI deviation: {ui['deviation']};")
    lines.extend(
        [
            "",
            "Implementation must not start until `project_adoption_gate.py check --phase pre-implementation` is green (or the equivalent checklist is proven when the script cannot run).",
            STATE_END,
        ]
    )
    return "\n".join(lines)


def normalize_config(config: dict[str, Any]) -> dict[str, Any]:
    routing = dict(config.get("routing") or {})
    ui = dict(config.get("ui") or {})
    adoption = dict(config.get("adoption") or {})

    profile = str(routing.get("profile") or "none")
    ui_enabled = bool(ui.get("enabled", profile == "web-admin"))
    design_system = str(ui.get("designSystem") or ("shadcn/ui" if profile == "web-admin" else "none"))
    hero = "heroui" in design_system.lower()

    normalized = {
        "schemaVersion": 2,
        "governance": "app-factory",
        "factoryBaseline": str(config.get("factoryBaseline") or "unknown"),
        "adoption": {
            "status": "routed",
            "mode": str(adoption.get("mode") or "existing"),
            "adoptedAt": str(adoption.get("adoptedAt") or _now()),
        },
        "routing": {
            "scale": str(routing.get("scale") or "M"),
            "risk": str(routing.get("risk") or "medium"),
            "systemLevel": str(routing.get("systemLevel") or "persistent-app"),
            "profile": profile,
            "apiMode": str(routing.get("apiMode") or "none"),
            "semanticVerification": str(routing.get("semanticVerification") or "required"),
            "semanticDepth": str(routing.get("semanticDepth") or "scenario"),
            "independentVerification": str(routing.get("independentVerification") or "independent"),
            "authoritativeData": str(routing.get("authoritativeData") or ""),
            "identity": str(routing.get("identity") or ""),
            "authorization": str(routing.get("authorization") or ""),
            "recovery": str(routing.get("recovery") or ""),
        },
        "ui": {
            "enabled": ui_enabled,
            "designSystem": design_system,
            "professionalUiProfile": str(ui.get("professionalUiProfile") or ("professional-default" if ui_enabled else "none")),
            "motionProfile": str(ui.get("motionProfile") or ("ambient" if ui_enabled else "none")),
            "ambientSurfaceProfile": str(ui.get("ambientSurfaceProfile") or ("ambient-constellation" if hero else "")) or None,
            "constellationIntensity": str(ui.get("constellationIntensity") or ("strong" if hero else "")) or None,
            "deviation": str(ui.get("deviation") or "") or None,
        },
    }
    return normalized


def initialize_project(project: Path, factory_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    project = project.resolve()
    factory_root = factory_root.resolve()
    project.mkdir(parents=True, exist_ok=True)

    normalized = normalize_config(config)
    manifest_path = project / ".app-factory.json"
    existing_manifest = _read_json(manifest_path)
    merged = dict(existing_manifest)
    merged.update(normalized)
    # Preserve starter provenance/recipes and other non-governance keys by updating rather than replacing.
    _write_json(manifest_path, merged)

    agents_path = project / "AGENTS.md"
    if agents_path.is_file():
        agents_text = agents_path.read_text(encoding="utf-8")
    else:
        template = factory_root / "templates" / "project" / "AGENTS.md"
        agents_text = template.read_text(encoding="utf-8") if template.is_file() else "# AGENTS.md — Project\n"
    agents_path.write_text(_replace_managed_block(agents_text, _agents_block()), encoding="utf-8")

    state_path = project / "PROJECT_STATE.md"
    state_text = state_path.read_text(encoding="utf-8") if state_path.is_file() else "# PROJECT_STATE\n"
    state_path.write_text(_replace_managed_block(state_text, _state_block(normalized)), encoding="utf-8")
    return merged


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _level_at_least(level: str, minimum: str) -> bool:
    try:
        return SYSTEM_LEVELS.index(level) >= SYSTEM_LEVELS.index(minimum)
    except ValueError:
        return False


def audit_project(project: Path, phase: str = "pre-implementation") -> list[str]:
    project = project.resolve()
    issues: list[str] = []

    if phase not in {"pre-implementation", "delivery"}:
        return [f"unsupported phase: {phase}"]

    manifest_path = project / ".app-factory.json"
    if not manifest_path.is_file():
        return ["missing .app-factory.json for an App Factory-governed project"]

    try:
        manifest = _read_json(manifest_path)
    except (ValueError, json.JSONDecodeError) as exc:
        return [f"invalid .app-factory.json: {exc}"]

    if manifest.get("schemaVersion") != 2:
        issues.append(".app-factory.json schemaVersion must be 2; run adoption init to upgrade legacy starter metadata")
    if manifest.get("governance") != "app-factory":
        issues.append(".app-factory.json must declare governance=app-factory")

    adoption = manifest.get("adoption") if isinstance(manifest.get("adoption"), dict) else {}
    routing = manifest.get("routing") if isinstance(manifest.get("routing"), dict) else {}
    ui = manifest.get("ui") if isinstance(manifest.get("ui"), dict) else {}

    if adoption.get("status") != "routed":
        issues.append("adoption.status must be routed before implementation")
    if adoption.get("mode") not in {"new", "existing"}:
        issues.append("adoption.mode must be new or existing")

    scale = str(routing.get("scale") or "")
    risk = str(routing.get("risk") or "")
    system_level = str(routing.get("systemLevel") or "")
    profile = str(routing.get("profile") or "")
    api_mode = str(routing.get("apiMode") or "")
    semantic_mode = str(routing.get("semanticVerification") or "")
    semantic_depth = str(routing.get("semanticDepth") or "")
    independent_mode = str(routing.get("independentVerification") or "")

    if scale not in SCALES:
        issues.append(f"invalid or missing routing.scale: {scale or '<empty>'}")
    if risk not in RISKS:
        issues.append(f"invalid or missing routing.risk: {risk or '<empty>'}")
    if system_level not in SYSTEM_LEVELS:
        issues.append(f"invalid or missing routing.systemLevel: {system_level or '<empty>'}")
    if not profile:
        issues.append("routing.profile must be recorded (use none when no validated profile applies)")
    if api_mode not in API_MODES:
        issues.append(f"invalid or missing routing.apiMode: {api_mode or '<empty>'}")
    if semantic_mode not in SEMANTIC_MODES:
        issues.append(f"invalid or missing routing.semanticVerification: {semantic_mode or '<empty>'}")
    if semantic_depth not in SEMANTIC_DEPTHS:
        issues.append(f"invalid or missing routing.semanticDepth: {semantic_depth or '<empty>'}")
    if independent_mode not in INDEPENDENT_MODES:
        issues.append(f"invalid or missing routing.independentVerification: {independent_mode or '<empty>'}")

    if system_level in SYSTEM_LEVELS and _level_at_least(system_level, "persistent-app"):
        if not _nonempty(routing.get("authoritativeData")):
            issues.append(f"{system_level} requires routing.authoritativeData")
    if system_level in SYSTEM_LEVELS and _level_at_least(system_level, "multi-user-system"):
        for field in ("identity", "authorization", "recovery"):
            if not _nonempty(routing.get(field)):
                issues.append(f"{system_level} requires routing.{field}")

    if semantic_mode == "not-required" and semantic_depth != "none":
        issues.append("semanticDepth must be none when Semantic Verification is not-required")
    if semantic_mode == "required" and semantic_depth == "none":
        issues.append("Semantic Verification required needs scenario, domain, or formal depth")
    if semantic_mode == "required":
        for relative in ("specs/semantic-contract.json", "specs/verification-plan.json"):
            if not (project / relative).is_file():
                issues.append(f"Semantic Verification required before code: missing {relative}")
        if semantic_depth in {"domain", "formal"} and not (project / "specs/semantic-assurance.json").is_file():
            issues.append(f"semantic depth {semantic_depth} requires specs/semantic-assurance.json before code")

    ui_enabled = ui.get("enabled") is True
    if ui_enabled:
        design_system = str(ui.get("designSystem") or "")
        design_lower = design_system.strip().lower()
        if not design_system or design_lower == "none":
            issues.append("UI-enabled project requires ui.designSystem before implementation")
        if not _nonempty(ui.get("professionalUiProfile")) or ui.get("professionalUiProfile") == "none":
            issues.append("UI-enabled project requires ui.professionalUiProfile")
        if not _nonempty(ui.get("motionProfile")) or ui.get("motionProfile") == "none":
            issues.append("UI-enabled project requires ui.motionProfile")
        if profile == "web-admin" and design_lower in AD_HOC_DESIGN_SYSTEMS and not _nonempty(ui.get("deviation")):
            issues.append("web-admin cannot use ad-hoc/native CSS as its visual foundation without an explicit ui.deviation; default is shadcn/ui or an explicit HeroUI override")
        if "heroui" in design_lower:
            if ui.get("ambientSurfaceProfile") != "ambient-constellation":
                issues.append("HeroUI primary design system requires ui.ambientSurfaceProfile=ambient-constellation by default")
            if ui.get("constellationIntensity") != "strong":
                issues.append("HeroUI primary design system requires ui.constellationIntensity=strong by default")

    agents_path = project / "AGENTS.md"
    if not agents_path.is_file():
        issues.append("missing AGENTS.md durable App Factory link")
    else:
        agents = agents_path.read_text(encoding="utf-8")
        for marker in ("App Factory", "factory-router", "PROJECT_ADOPTION_GATE.md"):
            if marker not in agents:
                issues.append(f"AGENTS.md missing adoption marker: {marker}")

    state_path = project / "PROJECT_STATE.md"
    if not state_path.is_file():
        issues.append("missing PROJECT_STATE.md")
    else:
        state = state_path.read_text(encoding="utf-8")
        if STATE_START not in state or "## App Factory Adoption" not in state:
            issues.append("PROJECT_STATE.md missing managed App Factory Adoption block")

    if phase == "delivery":
        if semantic_mode == "required" and risk in {"medium", "high", "critical"}:
            if not (project / "specs/review-evidence.json").is_file():
                issues.append(f"delivery at {risk} risk requires current specs/review-evidence.json")
        if independent_mode in {"independent", "adversarial", "release"} and not (project / "VERIFICATION.md").is_file():
            issues.append(f"Independent Verification mode {independent_mode} requires recoverable VERIFICATION.md before delivery")

    return issues
