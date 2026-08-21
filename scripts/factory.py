#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
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
from engine.ci_executor import build_ci_plan, run_declared_gates  # noqa: E402
from engine.context_engine import scan_repository  # noqa: E402
from engine.execution_engine import (  # noqa: E402
    default_backends,
    read_execution_state,
    record_execution_attempt,
    route_action,
)


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def csv_values(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def available_backends(args: argparse.Namespace) -> list[str]:
    raw = getattr(args, "backends", None) or os.environ.get("APP_FACTORY_BACKENDS") or "current_agent,github_ci"
    return csv_values(raw)


def current_task_key(project_root: Path) -> str | None:
    state = read_state(project_root)
    if not isinstance(state, dict):
        return None
    created_at = state.get("created_at")
    return str(created_at) if created_at else None


def execution_for_action(project_root: Path, action: dict[str, object], backends: list[str]) -> dict[str, object]:
    action_name = str(action.get("action") or "inspect_state")
    if action_name == "request_human":
        return {"backend": "human", "action": action_name, "reason": "A decisão foi explicitamente classificada como humana."}
    if action_name == "done":
        return {"backend": None, "action": action_name, "reason": "Nenhuma execução adicional é necessária."}
    return route_action(
        project_root,
        action_name,
        available_backends=backends,
        task_key=current_task_key(project_root),
    ).to_dict()


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="App Factory V1.2 autonomous context/execution CLI")
    root.add_argument("--root", default=".", help="Project root (default: current directory)")
    root.add_argument(
        "--backends",
        help="Comma-separated available execution backends. Default: current_agent,github_ci or APP_FACTORY_BACKENDS.",
    )
    sub = root.add_subparsers(dest="command", required=True)

    context = sub.add_parser("context", help="Refresh incremental repository context")
    context.add_argument("--max-bytes", type=int, default=512 * 1024)

    init = sub.add_parser("init", help="Initialize autonomous project state")
    init.add_argument("--goal", help="User outcome; inferred from PROJECT_STATE/README when omitted")
    init.add_argument("--max-repairs", type=int, default=3)

    sub.add_parser("status", help="Show compact autonomous state")
    sub.add_parser("next", help="Refresh context and choose the next action plus execution backend")

    resume = sub.add_parser("resume", help="Recover state in a fresh session and choose action/backend")
    resume.add_argument("--goal", help="Used only when no state exists and no clear goal can be inferred")
    resume.add_argument("--max-repairs", type=int, default=3)

    record = sub.add_parser("record", help="Record one agent/workflow event")
    record.add_argument("event", choices=sorted(EVENTS))
    record.add_argument("--summary")
    record.add_argument("--category", choices=sorted(HUMAN_CATEGORIES))

    route = sub.add_parser("route", help="Choose the lightest capable execution backend")
    route.add_argument("action")
    route.add_argument("--need", action="append", default=[], help="Additional required capability; repeatable")
    route.add_argument("--headless-browser", action="store_true")
    route.add_argument("--interactive-shell", action="store_true")
    route.add_argument("--interactive-browser", action="store_true")
    route.add_argument("--live-migration", action="store_true")
    route.add_argument("--task-key", help="Optional task scope; defaults to current Autonomy state creation id")

    sub.add_parser("execution-status", help="Show bounded execution attempt history")

    attempt = sub.add_parser("record-execution", help="Record one execution backend outcome")
    attempt.add_argument("action")
    attempt.add_argument("backend", choices=sorted(default_backends()))
    attempt.add_argument("outcome", choices=["success", "failure", "blocked", "cancelled"])
    attempt.add_argument("--need", action="append", default=[])
    attempt.add_argument("--summary")
    attempt.add_argument("--duration-ms", type=int)
    attempt.add_argument("--task-key", help="Optional task scope; defaults to current Autonomy state creation id")

    sub.add_parser("gates", help="Discover repository-owned allowlisted deterministic CI gates")
    run_gates = sub.add_parser("run-gates", help="Run discovered allowlisted gates without shell evaluation")
    run_gates.add_argument("--gate", action="append", default=[], help="Gate id to run; repeatable. Default: all discovered")
    run_gates.add_argument("--timeout", type=int, default=900)
    return root


def main() -> int:
    args = parser().parse_args()
    project_root = Path(args.root).resolve()
    backends = available_backends(args)

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
        emit({"action": action, "execution": execution_for_action(project_root, action, backends), "state": state})
        return 0
    if args.command == "resume":
        result = resume_project(project_root, goal=args.goal, max_repairs=args.max_repairs)
        emit({
            "action": result.action,
            "execution": execution_for_action(project_root, result.action, backends),
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
        action = next_action(project_root, auto_refresh=False)[0]
        emit({"state": state, "next": action, "execution": execution_for_action(project_root, action, backends)})
        return 0
    if args.command == "route":
        decision = route_action(
            project_root,
            args.action,
            available_backends=backends,
            task_key=args.task_key or current_task_key(project_root),
            headless_browser=args.headless_browser,
            interactive_shell=args.interactive_shell,
            interactive_browser=args.interactive_browser,
            live_migration=args.live_migration,
            extra_capabilities=args.need,
        )
        emit(decision.to_dict())
        return 0 if decision.backend_id else 2
    if args.command == "execution-status":
        emit(read_execution_state(project_root))
        return 0
    if args.command == "record-execution":
        state = record_execution_attempt(
            project_root,
            action=args.action,
            backend_id=args.backend,
            required_capabilities=args.need,
            outcome=args.outcome,
            summary=args.summary,
            duration_ms=args.duration_ms,
            task_key=args.task_key or current_task_key(project_root),
        )
        emit(state)
        return 0
    if args.command == "gates":
        emit(build_ci_plan(project_root))
        return 0
    if args.command == "run-gates":
        results = run_declared_gates(project_root, gate_ids=args.gate, timeout_seconds=args.timeout)
        payload = [result.to_dict() for result in results]
        emit({"results": payload, "success": bool(results) and all(result.success for result in results)})
        return 0 if payload and all(item["success"] for item in payload) else 1
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
