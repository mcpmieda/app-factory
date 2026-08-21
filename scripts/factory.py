#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.autonomy_engine import (  # noqa: E402
    EVENTS,
    HUMAN_CATEGORIES,
    init_project,
    next_action,
    read_state,
    record_event,
    resume_project,
)
from engine.context_engine import scan_repository  # noqa: E402


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="App Factory V1.1 autonomous context/runtime CLI")
    root.add_argument("--root", default=".", help="Project root (default: current directory)")
    sub = root.add_subparsers(dest="command", required=True)

    context = sub.add_parser("context", help="Refresh incremental repository context")
    context.add_argument("--max-bytes", type=int, default=512 * 1024)

    init = sub.add_parser("init", help="Initialize autonomous project state")
    init.add_argument("--goal", help="User outcome; inferred from PROJECT_STATE/README when omitted")
    init.add_argument("--max-repairs", type=int, default=3)

    sub.add_parser("status", help="Show compact autonomous state")
    sub.add_parser("next", help="Refresh context and choose the next action")

    resume = sub.add_parser("resume", help="Recover state in a fresh session and choose the next action")
    resume.add_argument("--goal", help="Used only when no state exists and no clear goal can be inferred")
    resume.add_argument("--max-repairs", type=int, default=3)

    record = sub.add_parser("record", help="Record one agent/workflow event")
    record.add_argument("event", choices=sorted(EVENTS))
    record.add_argument("--summary")
    record.add_argument("--category", choices=sorted(HUMAN_CATEGORIES))
    return root


def main() -> int:
    args = parser().parse_args()
    project_root = Path(args.root).resolve()

    if args.command == "context":
        result = scan_repository(project_root, max_bytes=args.max_bytes)
        emit({
            "fingerprint": result.repo_map["fingerprint"],
            "delta": result.repo_map["delta"],
            "stats": result.repo_map["stats"],
            "stack": result.repo_map["stack"],
            "output_dir": str(result.output_dir.relative_to(project_root)) if result.output_dir.is_relative_to(project_root) else str(result.output_dir),
        })
        return 0
    if args.command == "init":
        emit(init_project(project_root, goal=args.goal, max_repairs=args.max_repairs))
        return 0
    if args.command == "status":
        state = read_state(project_root)
        emit(state or {"status": "uninitialized", "next": "resume"})
        return 0
    if args.command == "next":
        action, state = next_action(project_root)
        emit({"action": action, "state": state})
        return 0
    if args.command == "resume":
        result = resume_project(project_root, goal=args.goal, max_repairs=args.max_repairs)
        emit({
            "action": result.action,
            "state": result.state,
            "context": {
                "fingerprint": result.context.repo_map["fingerprint"],
                "delta": result.context.repo_map["delta"],
                "stats": result.context.repo_map["stats"],
            },
        })
        return 0
    if args.command == "record":
        state = record_event(project_root, args.event, summary=args.summary, category=args.category)
        emit({"state": state, "next": next_action(project_root, auto_refresh=False)[0]})
        return 0
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
