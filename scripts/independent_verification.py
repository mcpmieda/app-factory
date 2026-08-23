#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.independent_verification import (  # noqa: E402
    API_MODES,
    RISK_LEVELS,
    SYSTEM_LEVELS,
    build_independent_verification_plan,
)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description="Build a free-only deterministic Independent Verification plan")
    command.add_argument("--root", default=".", help="Project root")
    command.add_argument("--risk", choices=RISK_LEVELS, default="medium")
    command.add_argument("--system-level", choices=SYSTEM_LEVELS, default="persistent-app")
    command.add_argument("--api-mode", choices=API_MODES, default="none")
    command.add_argument("--release", action="store_true")
    command.add_argument(
        "--external-integrations",
        action="store_true",
        help="Project has material network integrations whose resilience must be exercised through controlled test proxies/stubs",
    )
    return command


def main() -> int:
    args = parser().parse_args()
    plan = build_independent_verification_plan(
        Path(args.root),
        risk=args.risk,
        system_level=args.system_level,
        api_mode=args.api_mode,
        release=args.release,
        external_integrations=args.external_integrations,
    )
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
