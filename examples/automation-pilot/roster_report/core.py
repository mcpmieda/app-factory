from __future__ import annotations

import csv
import json
import os
import tempfile
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS = {"id", "name", "department", "hours", "training_required"}
TRUTHY = {"1", "true", "yes", "sim"}
FALSY = {"0", "false", "no", "não", "nao"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")
        return [dict(row) for row in reader]


def _normalize(row: dict[str, str], row_number: int) -> tuple[dict[str, Any] | None, str | None]:
    record_id = row.get("id", "").strip().upper()
    name = " ".join(row.get("name", "").split()).title()
    department = " ".join(row.get("department", "").split()).upper()
    if not record_id or not name or not department:
        return None, f"row {row_number}: id, name and department are required"
    try:
        hours = int(row.get("hours", ""))
        if hours < 0:
            raise ValueError
    except ValueError:
        return None, f"row {row_number} ({record_id}): hours must be a non-negative integer"
    raw_required = row.get("training_required", "").strip().lower()
    if raw_required not in TRUTHY | FALSY:
        return None, f"row {row_number} ({record_id}): training_required must be yes/no"
    required = raw_required in TRUTHY
    priority = "urgent" if required and hours < 4 else "follow-up" if required else "complete"
    return {
        "department": department,
        "hours": hours,
        "id": record_id,
        "name": name,
        "priority": priority,
        "training_required": required,
    }, None


def build_report(rows: list[dict[str, str]]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for row_number, row in enumerate(rows, start=2):
        record, error = _normalize(row, row_number)
        if error:
            errors.append(error)
        elif record:
            records.append(record)
    records.sort(key=lambda item: item["id"])
    errors.sort()
    return {
        "errors": errors,
        "records": records,
        "summary": {
            "accepted": len(records),
            "rejected": len(errors),
            "urgent": sum(record["priority"] == "urgent" for record in records),
        },
    }


def serialize_report(report: dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as target:
            target.write(serialize_report(report))
            target.flush()
            os.fsync(target.fileno())
        os.replace(temp_name, path)
    except BaseException:
        Path(temp_name).unlink(missing_ok=True)
        raise
