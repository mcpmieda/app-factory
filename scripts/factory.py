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
    request_for_action,
    route_action,
)
from engine.learning_engine import learning_status, record_learning_event  # noqa: E402
from engine.review_packet import build_clean_review_packet  # noqa: E402
from engine.semantic_verification import (  # noqa: E402
    CHANGE_TYPES,
    REVIEW_MODES,
    RISK_LEVELS,
    VERDICTS,
    create_verification_plan,
    new_spec,
    read_spec,
    semantic_status,
    validate_spec,
    write_review_evidence,
    write_verification_plan,
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


def add_capability_flags(command: argparse.ArgumentParser) -> None:
    command.add_argument("--need", action="append", default=[], help="Additional required capability; repeatable")
    command.add_argument("--headless-browser", action="store_true")
    command.add_argument("--interactive-shell", action="store_true")
    command.add_argument("--interactive-browser", action="store_true")
    command.add_argument("--live-migration", action="store_true")


def capability_request(args: argparse.Namespace):
    return request_for_action(
        args.action,
        headless_browser=getattr(args, "headless_browser", False),
        interactive_shell=getattr(args, "interactive_shell", False),
        interactive_browser=getattr(args, "interactive_browser", False),
        live_migration=getattr(args, "live_migration", False),
        extra_capabilities=getattr(args, "need", []),
    )


def parse_criterion_results(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in values:
        criterion_id, separator, status = raw.partition("=")
        criterion_id = criterion_id.strip()
        status = status.strip()
        if not separator or not criterion_id or status not in {"pass", "fail"}:
            raise ValueError("--criterion must use AC-001=pass or AC-001=fail")
        result[criterion_id] = status
    return result


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="App Factory V1.4 autonomous context/execution/learning/semantic CLI")
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
    init.add_argument("--require-spec", action="store_true", help="Route planning through semantic specification before implementation")

    sub.add_parser("status", help="Show compact autonomous state")
    sub.add_parser("next", help="Refresh context and choose the next action plus execution backend")

    resume = sub.add_parser("resume", help="Recover state in a fresh session and choose action/backend")
    resume.add_argument("--goal", help="Used only when no state exists and no clear goal can be inferred")
    resume.add_argument("--max-repairs", type=int, default=3)
    resume.add_argument("--require-spec", action="store_true", help="Used only when creating missing state")

    record = sub.add_parser("record", help="Record one agent/workflow event")
    record.add_argument("event", choices=sorted(EVENTS))
    record.add_argument("--summary")
    record.add_argument("--category", choices=sorted(HUMAN_CATEGORIES))

    spec_template = sub.add_parser("spec-template", help="Emit a structured semantic-spec template; the agent fills criteria before spec-ready")
    spec_template.add_argument("--goal", required=True)
    spec_template.add_argument("--change-type", choices=sorted(CHANGE_TYPES), default="functional")
    spec_template.add_argument("--risk", choices=sorted(RISK_LEVELS), default="medium")

    sub.add_parser("spec-validate", help="Validate specs/semantic-contract.json")
    sub.add_parser("verification-plan-init", help="Generate verification-plan rows from the current semantic spec")
    sub.add_parser("semantic-status", help="Validate semantic spec, traceability and review freshness")
    review_packet = sub.add_parser("review-packet", help="Emit a clean-context spec + diff review packet without implementation reasoning")
    review_packet.add_argument("--base", default="main", help="Git base ref used to build the review diff (default: main)")

    review = sub.add_parser("record-semantic-review", help="Record decoupled semantic review evidence")
    review.add_argument("--mode", required=True, choices=sorted(REVIEW_MODES))
    review.add_argument("--verdict", required=True, choices=sorted(VERDICTS))
    review.add_argument("--criterion", action="append", default=[], help="Criterion result AC-001=pass; repeatable")
    review.add_argument("--finding", action="append", default=[], help="Review finding; repeatable")

    route = sub.add_parser("route", help="Choose a capable backend, using local learning only when evidence is sufficient")
    route.add_argument("action")
    add_capability_flags(route)
    route.add_argument("--task-key", help="Optional task scope; defaults to current Autonomy state creation id")
    route.add_argument("--no-learning", action="store_true", help="Show the pure V1.2 baseline route")

    sub.add_parser("execution-status", help="Show bounded execution attempt history")

    attempt = sub.add_parser("record-execution", help="Record execution outcome and update privacy-safe local learning")
    attempt.add_argument("action")
    attempt.add_argument("backend", choices=sorted(default_backends()))
    attempt.add_argument("outcome", choices=["success", "failure", "blocked", "cancelled"])
    add_capability_flags(attempt)
    attempt.add_argument("--summary")
    attempt.add_argument("--duration-ms", type=int)
    attempt.add_argument("--task-key", help="Optional task scope; defaults to current Autonomy state creation id")

    sub.add_parser("learning-status", help="Show aggregate local learning metadata; never raw prompts/code/logs")
    learn = sub.add_parser("learning-recommend", help="Explain the learned/baseline backend recommendation")
    learn.add_argument("action")
    add_capability_flags(learn)
    learn.add_argument("--task-key", help="Optional task scope for current execution fallback")

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
        emit(init_project(
            project_root,
            goal=args.goal,
            max_repairs=args.max_repairs,
            require_spec=args.require_spec,
        ))
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
        result = resume_project(
            project_root,
            goal=args.goal,
            max_repairs=args.max_repairs,
            require_spec=args.require_spec,
        )
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
    if args.command == "spec-template":
        emit(new_spec(args.goal, change_type=args.change_type, risk=args.risk))
        return 0
    if args.command == "spec-validate":
        spec = read_spec(project_root)
        errors = validate_spec(spec)
        emit({"valid": not errors, "errors": errors})
        return 0 if not errors else 1
    if args.command == "verification-plan-init":
        spec = read_spec(project_root)
        errors = validate_spec(spec)
        if errors:
            emit({"written": False, "errors": errors})
            return 1
        assert spec is not None
        plan = create_verification_plan(spec)
        write_verification_plan(project_root, plan)
        emit({"written": True, "path": "specs/verification-plan.json", "plan": plan})
        return 0
    if args.command == "semantic-status":
        status = semantic_status(project_root)
        emit(status.to_dict())
        return 0 if status.ready_for_delivery else 1
    if args.command == "review-packet":
        emit(build_clean_review_packet(project_root, base_ref=args.base))
        return 0
    if args.command == "record-semantic-review":
        try:
            criteria = parse_criterion_results(args.criterion)
            review_value = write_review_evidence(
                project_root,
                mode=args.mode,
                verdict=args.verdict,
                criterion_results=criteria,
                findings=args.finding,
            )
        except ValueError as error:
            emit({"written": False, "error": str(error)})
            return 1
        emit({"written": True, "path": "specs/review-evidence.json", "review": review_value})
        return 0
    if args.command in {"route", "learning-recommend"}:
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
            use_learning=not getattr(args, "no_learning", False),
        )
        if args.command == "learning-recommend":
            emit({"route": decision.to_dict(), "learning": decision.learning})
        else:
            emit(decision.to_dict())
        return 0 if decision.backend_id else 2
    if args.command == "execution-status":
        emit(read_execution_state(project_root))
        return 0
    if args.command == "record-execution":
        request = capability_request(args)
        capabilities = sorted(request.required_capabilities)
        state = record_execution_attempt(
            project_root,
            action=args.action,
            backend_id=args.backend,
            required_capabilities=capabilities,
            outcome=args.outcome,
            summary=args.summary,
            duration_ms=args.duration_ms,
            task_key=args.task_key or current_task_key(project_root),
        )
        record_learning_event(
            project_root,
            action=args.action,
            capabilities=capabilities,
            backend=args.backend,
            outcome=args.outcome,
            duration_ms=args.duration_ms,
        )
        emit({"execution": state, "learning": learning_status(project_root)})
        return 0
    if args.command == "learning-status":
        emit(learning_status(project_root))
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
