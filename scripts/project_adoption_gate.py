#!/usr/bin/env python3
"""Initialize or check durable App Factory adoption for a project."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.project_adoption import audit_project, initialize_project  # noqa: E402


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="App Factory Project Adoption Gate")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Materialize durable App Factory adoption metadata")
    init.add_argument("--project", required=True)
    init.add_argument("--mode", choices=["new", "existing"], default="existing")
    init.add_argument("--factory-baseline", default="unknown")
    init.add_argument("--scale", choices=["S", "M", "L", "XL"], required=True)
    init.add_argument("--risk", choices=["low", "medium", "high", "critical"], required=True)
    init.add_argument(
        "--system-level",
        choices=["website", "local-app", "persistent-app", "multi-user-system", "production-system", "critical-system"],
        required=True,
    )
    init.add_argument("--profile", default="none")
    init.add_argument("--api-mode", choices=["none", "lightweight", "contract", "governed"], required=True)
    init.add_argument("--semantic", choices=["required", "not-required"], required=True)
    init.add_argument("--semantic-depth", choices=["none", "scenario", "domain", "formal"], required=True)
    init.add_argument(
        "--independent",
        choices=["baseline", "independent", "adversarial", "release"],
        required=True,
    )
    init.add_argument("--authoritative-data", default="")
    init.add_argument("--identity", default="")
    init.add_argument("--authorization", default="")
    init.add_argument("--recovery", default="")
    init.add_argument("--ui", choices=["true", "false"], default=None)
    init.add_argument("--design-system", default="")
    init.add_argument("--professional-ui-profile", default="")
    init.add_argument("--motion-profile", default="")
    init.add_argument("--ambient-surface-profile", default="")
    init.add_argument("--constellation-intensity", default="")
    init.add_argument("--deviation", default="")

    check = subparsers.add_parser("check", help="Read-only conformance check")
    check.add_argument("--project", required=True)
    check.add_argument("--phase", choices=["pre-implementation", "delivery"], default="pre-implementation")
    check.add_argument("--json", action="store_true")
    return parser


def _init(args: argparse.Namespace) -> int:
    ui_enabled = None if args.ui is None else args.ui == "true"
    config = {
        "factoryBaseline": args.factory_baseline,
        "adoption": {"mode": args.mode},
        "routing": {
            "scale": args.scale,
            "risk": args.risk,
            "systemLevel": args.system_level,
            "profile": args.profile,
            "apiMode": args.api_mode,
            "semanticVerification": args.semantic,
            "semanticDepth": args.semantic_depth,
            "independentVerification": args.independent,
            "authoritativeData": args.authoritative_data,
            "identity": args.identity,
            "authorization": args.authorization,
            "recovery": args.recovery,
        },
        "ui": {
            **({"enabled": ui_enabled} if ui_enabled is not None else {}),
            "designSystem": args.design_system,
            "professionalUiProfile": args.professional_ui_profile,
            "motionProfile": args.motion_profile,
            "ambientSurfaceProfile": args.ambient_surface_profile,
            "constellationIntensity": args.constellation_intensity,
            "deviation": args.deviation,
        },
    }
    manifest = initialize_project(Path(args.project), ROOT, config)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def _check(args: argparse.Namespace) -> int:
    issues = audit_project(Path(args.project), phase=args.phase)
    if args.json:
        print(json.dumps({"phase": args.phase, "ok": not issues, "issues": issues}, ensure_ascii=False, indent=2))
    elif issues:
        print(f"FAIL: App Factory adoption gate ({args.phase})")
        for issue in issues:
            print(f"- {issue}")
    else:
        print(f"OK: App Factory adoption gate ({args.phase})")
    return 1 if issues else 0


def main() -> int:
    args = _parser().parse_args()
    return _init(args) if args.command == "init" else _check(args)


if __name__ == "__main__":
    raise SystemExit(main())
