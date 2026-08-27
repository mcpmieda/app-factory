#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.work_orchestrator import (  # noqa: E402
    MAX_AUTOMATIC_PARALLEL,
    build_execution_plan,
    default_worker_providers,
    factory_run_template,
    load_factory_run,
)


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def csv_values(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="App Factory provider-neutral multiagent Factory Run planner")
    sub = root.add_subparsers(dest="command", required=True)

    sub.add_parser("template", help="Emit a portable Factory Run JSON template")

    validate = sub.add_parser("validate", help="Validate a Factory Run JSON file")
    validate.add_argument("spec", type=Path)

    plan = sub.add_parser("plan", help="Build safe parallel execution waves")
    plan.add_argument("spec", type=Path)
    plan.add_argument(
        "--providers",
        default="jules,antigravity",
        help="Comma-separated providers currently available to this machine/control plane",
    )
    plan.add_argument("--max-parallel", type=int, default=MAX_AUTOMATIC_PARALLEL)
    plan.add_argument(
        "--allow-metered",
        action="store_true",
        help="Allow metered providers if explicitly made automatic in a custom registry. Codex remains manual by default.",
    )

    sub.add_parser("providers", help="Show the built-in worker provider registry without credentials")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "template":
            emit(factory_run_template())
            return 0
        if args.command == "providers":
            emit({
                key: {
                    "cost_class": value.cost_class,
                    "execution_mode": value.execution_mode,
                    "capabilities": sorted(value.capabilities),
                    "max_parallel": value.max_parallel,
                    "automatic": value.automatic,
                    "requires_local_machine": value.requires_local_machine,
                    "description": value.description,
                }
                for key, value in default_worker_providers().items()
            })
            return 0
        if args.command == "validate":
            run_id, goal, tasks = load_factory_run(args.spec)
            emit({"valid": True, "run_id": run_id, "goal": goal, "task_count": len(tasks)})
            return 0
        if args.command == "plan":
            plan = build_execution_plan(
                args.spec,
                available_provider_ids=csv_values(args.providers),
                max_parallel=args.max_parallel,
                allow_metered=args.allow_metered,
            )
            emit(plan.to_dict())
            return 0 if not plan.blocked else 2
    except (OSError, json.JSONDecodeError, ValueError) as error:
        emit({"valid": False, "error": str(error)})
        return 1
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
