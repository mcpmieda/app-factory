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

SUPPORTED_AUTOMATIC_PROVIDERS = frozenset({"jules", "opencode_ollama"})


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def csv_values(raw: str) -> list[str]:
    values = [item.strip() for item in raw.split(",") if item.strip()]
    unsupported = [item for item in values if item not in SUPPORTED_AUTOMATIC_PROVIDERS]
    if unsupported:
        raise ValueError(
            "Unsupported automatic provider in finalized scope: " + ", ".join(unsupported)
        )
    return values


def finalized_template() -> dict[str, object]:
    template = factory_run_template()
    for task in template.get("tasks", []):
        if not isinstance(task, dict):
            continue
        preferred = task.get("preferred_providers")
        if isinstance(preferred, list):
            task["preferred_providers"] = [
                item for item in preferred if item in SUPPORTED_AUTOMATIC_PROVIDERS
            ]
    return template


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="App Factory finalized multiagent Factory Run planner")
    sub = root.add_subparsers(dest="command", required=True)

    sub.add_parser("template", help="Emit a portable Factory Run JSON template")

    validate = sub.add_parser("validate", help="Validate a Factory Run JSON file")
    validate.add_argument("spec", type=Path)

    plan = sub.add_parser("plan", help="Build safe parallel execution waves")
    plan.add_argument("spec", type=Path)
    plan.add_argument(
        "--providers",
        default="jules,opencode_ollama",
        help="Comma-separated supported providers currently available to this control plane",
    )
    plan.add_argument("--max-parallel", type=int, default=MAX_AUTOMATIC_PARALLEL)
    plan.add_argument(
        "--allow-metered",
        action="store_true",
        help="Reserved compatibility flag. Codex remains manual and is never selected automatically.",
    )

    sub.add_parser("providers", help="Show the finalized automatic provider registry")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "template":
            emit(finalized_template())
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
                if key in SUPPORTED_AUTOMATIC_PROVIDERS
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
