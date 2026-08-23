#!/usr/bin/env python3
"""Record/report privacy-safe aggregate Skill routing telemetry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.learning_engine import record_skill_routing, skill_routing_report  # noqa: E402


def installed_skills() -> list[str]:
    return sorted(path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md"))


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="App Factory local aggregate Skill routing telemetry")
    root.add_argument("--root", default=".", help="Project root that owns .factory/ telemetry")
    sub = root.add_subparsers(dest="command", required=True)

    record = sub.add_parser("record")
    record.add_argument("--skill", action="append", required=True, help="Installed Skill slug; repeatable")
    record.add_argument("--source", choices=["factory-router", "app-planner", "manual"], default="factory-router")

    sub.add_parser("report")
    return root


def main() -> int:
    args = parser().parse_args()
    project_root = Path(args.root).resolve()
    catalog = installed_skills()
    if args.command == "record":
        unknown = sorted(set(args.skill) - set(catalog))
        if unknown:
            emit({"recorded": False, "error": "unknown installed Skill(s): " + ", ".join(unknown)})
            return 1
        try:
            state = record_skill_routing(project_root, skills=args.skill, source=args.source)
        except ValueError as error:
            emit({"recorded": False, "error": str(error)})
            return 1
        emit({"recorded": True, "state": state})
        return 0
    if args.command == "report":
        emit(skill_routing_report(project_root, installed_skills=catalog))
        return 0
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
