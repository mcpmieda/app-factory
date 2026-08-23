#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.semantic_assurance import (  # noqa: E402
    analyze_assurance,
    load_json,
    new_assurance,
    read_assurance,
    semantic_diff,
    write_assurance,
)
from engine.semantic_verification import read_spec  # noqa: E402


def command_init(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    spec = read_spec(root)
    if spec is None:
        raise SystemExit("semantic-contract.json is required before semantic assurance init")
    assurance = new_assurance(spec, depth=args.depth)
    write_assurance(root, assurance)
    print(f"created {root / 'specs/semantic-assurance.json'}")
    return 0


def command_analyze(args: argparse.Namespace) -> int:
    report = analyze_assurance(args.root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ready"] else 1


def command_diff(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    current = read_assurance(root)
    if current is None:
        raise SystemExit("current semantic-assurance.json is missing")
    baseline = load_json(args.baseline)
    plan_path = root / "specs/verification-plan.json"
    plan = load_json(plan_path) if plan_path.is_file() else None
    report = semantic_diff(baseline, current, verification_plan=plan)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="App Factory Semantic Assurance")
    parser.add_argument("--root", default=".", help="project root")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create semantic-assurance.json from current semantic contract")
    init.add_argument("--depth", choices=["scenario", "domain", "formal"], default="domain")
    init.set_defaults(func=command_init)

    analyze = sub.add_parser("analyze", help="validate consistency, traceability and coverage")
    analyze.set_defaults(func=command_analyze)

    diff = sub.add_parser("diff", help="compare a baseline semantic-assurance.json to current")
    diff.add_argument("--baseline", required=True)
    diff.set_defaults(func=command_diff)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
