from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .core import build_report, read_csv, serialize_report, write_report


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description="Normalize a fictitious roster CSV.")
    command.add_argument("input", type=Path)
    command.add_argument("output", type=Path)
    command.add_argument(
        "--dry-run", action="store_true", help="Print output without writing a file."
    )
    return command


def main() -> int:
    args = parser().parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        report = build_report(read_csv(args.input))
    except (OSError, ValueError) as error:
        logging.error("input rejected: %s", error)
        return 2
    summary = report["summary"]
    logging.info(
        "processed accepted=%s rejected=%s urgent=%s",
        summary["accepted"],
        summary["rejected"],
        summary["urgent"],
    )
    if args.dry_run:
        print(serialize_report(report), end="")
        logging.info("dry-run complete; no file written")
    else:
        write_report(args.output, report)
        logging.info("report written atomically to %s", args.output)
    return 0


raise SystemExit(main())
