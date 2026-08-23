#!/usr/bin/env python3
"""Deterministic corpus/scorer for App Factory agent conformance.

The scorer evaluates observable worktree state only. It never asks for or
scores private chain-of-thought. Reference actions are intentionally allowlisted
and never execute arbitrary shell supplied by a case.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.ci_executor import run_declared_gates  # noqa: E402
from engine.semantic_verification import (  # noqa: E402
    read_spec,
    semantic_status,
    validate_spec,
    validate_verification_plan,
)

SCHEMA_VERSION = 1
CASES_DIR = ROOT / "evals" / "agent-conformance" / "cases"
FACTORY_CLI = ROOT / "scripts" / "factory.py"
CASE_ID_CHARS = frozenset("abcdefghijklmnopqrstuvwxyz0123456789-")
ACTION_KINDS = {"write_text", "write_json", "factory_cli", "attach_evidence"}
ASSERTION_KINDS = {
    "file_exists",
    "file_absent",
    "text_contains",
    "json_equals",
    "semantic_spec_valid",
    "verification_plan_valid",
    "semantic_ready",
    "declared_gate_passes",
}
BEHAVIORAL_ASSERTIONS = ASSERTION_KINDS - {"file_exists", "file_absent"}
MAX_CASE_TEXT = 256_000


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def safe_relative_path(root: Path, raw: str) -> Path:
    relative = Path(str(raw))
    if relative.is_absolute() or not relative.parts or ".." in relative.parts or relative.parts[0] == ".git":
        raise ValueError(f"unsafe relative path: {raw}")
    target = (root / relative).resolve()
    root = root.resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"path escapes workspace: {raw}")
    return target


def valid_case_id(value: Any) -> bool:
    if not isinstance(value, str) or not 3 <= len(value) <= 80:
        return False
    return value[0].isalnum() and value[-1].isalnum() and all(char in CASE_ID_CHARS for char in value)


def validate_case(case: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(case, dict):
        return ["case must be a JSON object"]
    if case.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if not valid_case_id(case.get("id")):
        errors.append("id must be a stable lowercase slug")
    prompt = case.get("prompt")
    if not isinstance(prompt, str) or len(prompt.strip()) < 20 or len(prompt) > MAX_CASE_TEXT:
        errors.append("prompt must be a bounded meaningful string")

    actions = case.get("reference_actions")
    if not isinstance(actions, list) or not actions:
        errors.append("reference_actions must be a non-empty array")
        actions = []
    for index, action in enumerate(actions):
        if not isinstance(action, dict) or action.get("kind") not in ACTION_KINDS:
            errors.append(f"reference_actions[{index}] uses unsupported kind")
            continue
        path = action.get("path")
        if path is not None:
            try:
                safe_relative_path(Path("/tmp/conformance-audit"), str(path))
            except ValueError as error:
                errors.append(f"reference_actions[{index}]: {error}")
        if action.get("kind") == "factory_cli":
            args = action.get("args")
            if not isinstance(args, list) or not args or not all(isinstance(item, str) and item for item in args):
                errors.append(f"reference_actions[{index}].args must be non-empty strings")
            if type(action.get("expect_exit", 0)) is not int:
                errors.append(f"reference_actions[{index}].expect_exit must be an integer")
        if action.get("kind") == "attach_evidence":
            if not isinstance(action.get("criterion"), str) or not isinstance(action.get("evidence"), list):
                errors.append(f"reference_actions[{index}] requires criterion + evidence")

    assertions = case.get("assertions")
    if not isinstance(assertions, list) or not assertions:
        errors.append("assertions must be a non-empty array")
        assertions = []
    assertion_kinds: set[str] = set()
    for index, assertion in enumerate(assertions):
        if not isinstance(assertion, dict) or assertion.get("kind") not in ASSERTION_KINDS:
            errors.append(f"assertions[{index}] uses unsupported kind")
            continue
        kind = str(assertion["kind"])
        assertion_kinds.add(kind)
        path = assertion.get("path")
        if path is not None:
            try:
                safe_relative_path(Path("/tmp/conformance-audit"), str(path))
            except ValueError as error:
                errors.append(f"assertions[{index}]: {error}")
    if assertions and not (assertion_kinds & BEHAVIORAL_ASSERTIONS):
        errors.append("case must assert behavior/contract, not only file presence")
    return errors


def load_cases(case_id: str | None = None) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in sorted(CASES_DIR.glob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"invalid case file {path.name}: {error}") from error
        errors = validate_case(value)
        if errors:
            raise ValueError(f"invalid case {path.name}: {'; '.join(errors)}")
        assert isinstance(value, dict)
        current_id = str(value["id"])
        if current_id in seen:
            raise ValueError(f"duplicate case id: {current_id}")
        seen.add(current_id)
        if case_id is None or current_id == case_id:
            cases.append(value)
    if case_id is not None and not cases:
        raise ValueError(f"unknown case id: {case_id}")
    if not cases:
        raise ValueError("agent conformance corpus is empty")
    return cases


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_factory_cli(workspace: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(FACTORY_CLI), "--root", str(workspace), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        shell=False,
        timeout=60,
    )


def execute_reference_action(workspace: Path, action: dict[str, Any]) -> None:
    kind = action["kind"]
    if kind == "write_text":
        path = safe_relative_path(workspace, str(action["path"]))
        content = action.get("content")
        if not isinstance(content, str) or len(content) > MAX_CASE_TEXT:
            raise ValueError("write_text content must be a bounded string")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return
    if kind == "write_json":
        path = safe_relative_path(workspace, str(action["path"]))
        write_json(path, action.get("value"))
        return
    if kind == "factory_cli":
        completed = run_factory_cli(workspace, list(action["args"]))
        expected = int(action.get("expect_exit", 0))
        if completed.returncode != expected:
            raise RuntimeError(
                f"factory_cli expected {expected}, got {completed.returncode}: "
                f"{completed.stderr or completed.stdout}"
            )
        return
    if kind == "attach_evidence":
        plan_path = safe_relative_path(workspace, "specs/verification-plan.json")
        try:
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError("verification plan missing before attach_evidence") from error
        criterion = str(action["criterion"])
        rows = plan.get("criteria", []) if isinstance(plan, dict) else []
        for row in rows:
            if isinstance(row, dict) and row.get("id") == criterion:
                row["evidence"] = action["evidence"]
                write_json(plan_path, plan)
                return
        raise ValueError(f"criterion not found in verification plan: {criterion}")
    raise ValueError(f"unsupported reference action: {kind}")


def json_pointer_get(value: Any, pointer: str) -> Any:
    if pointer == "":
        return value
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("JSON pointer must start with /")
    current = value
    for raw in pointer[1:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(token)]
        elif isinstance(current, dict):
            current = current[token]
        else:
            raise KeyError(token)
    return current


def score_assertion(workspace: Path, assertion: dict[str, Any]) -> tuple[bool, str]:
    kind = assertion["kind"]
    if kind in {"file_exists", "file_absent"}:
        path = safe_relative_path(workspace, str(assertion["path"]))
        exists = path.is_file()
        expected = kind == "file_exists"
        return exists == expected, f"{kind}: {assertion['path']}"
    if kind == "text_contains":
        path = safe_relative_path(workspace, str(assertion["path"]))
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return False, f"text file missing: {assertion['path']}"
        needle = str(assertion.get("text", ""))
        return bool(needle) and needle in text, f"text_contains: {assertion['path']}"
    if kind == "json_equals":
        path = safe_relative_path(workspace, str(assertion["path"]))
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            actual = json_pointer_get(value, str(assertion.get("pointer", "")))
        except (OSError, json.JSONDecodeError, KeyError, IndexError, ValueError, TypeError):
            return False, f"json_equals unreadable: {assertion['path']}"
        return actual == assertion.get("value"), f"json_equals: {assertion['path']}#{assertion.get('pointer', '')}"
    if kind == "semantic_spec_valid":
        errors = validate_spec(read_spec(workspace))
        return not errors, "semantic_spec_valid" if not errors else "semantic_spec_valid: " + "; ".join(errors)
    if kind == "verification_plan_valid":
        errors = validate_verification_plan(workspace)
        return not errors, "verification_plan_valid" if not errors else "verification_plan_valid: " + "; ".join(errors)
    if kind == "semantic_ready":
        status = semantic_status(workspace)
        expected = bool(assertion.get("value", True))
        return status.ready_for_delivery == expected, f"semantic_ready expected={expected} actual={status.ready_for_delivery}"
    if kind == "declared_gate_passes":
        gate = str(assertion.get("gate", ""))
        try:
            results = run_declared_gates(workspace, gate_ids=[gate], timeout_seconds=60)
        except (ValueError, subprocess.SubprocessError) as error:
            return False, f"declared_gate_passes {gate}: {error}"
        passed = len(results) == 1 and results[0].success
        detail = results[0].stderr_tail or results[0].stdout_tail if results else "gate not executed"
        return passed, f"declared_gate_passes {gate}: {detail[-500:]}"
    return False, f"unsupported assertion: {kind}"


def score_workspace(case: dict[str, Any], workspace: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    for assertion in case["assertions"]:
        passed, detail = score_assertion(workspace.resolve(), assertion)
        checks.append({"kind": assertion["kind"], "pass": passed, "detail": detail})
    failures = [check for check in checks if not check["pass"]]
    return {
        "schema_version": SCHEMA_VERSION,
        "case": case["id"],
        "pass": not failures,
        "checks": checks,
        "blocking_failures": failures,
    }


def run_reference_case(case: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix=f"app-factory-{case['id']}-") as temp:
        workspace = Path(temp)
        try:
            for action in case["reference_actions"]:
                execute_reference_action(workspace, action)
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            return {
                "schema_version": SCHEMA_VERSION,
                "case": case["id"],
                "pass": False,
                "checks": [],
                "blocking_failures": [{"kind": "reference_execution", "pass": False, "detail": str(error)}],
            }
        return score_workspace(case, workspace)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="App Factory deterministic agent-conformance corpus/scorer")
    sub = root.add_subparsers(dest="command", required=True)
    sub.add_parser("validate-corpus")
    reference = sub.add_parser("run-reference")
    reference.add_argument("--case")
    score = sub.add_parser("score")
    score.add_argument("--case", required=True)
    score.add_argument("--workspace", required=True)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        cases = load_cases(getattr(args, "case", None))
    except ValueError as error:
        emit({"pass": False, "error": str(error)})
        return 1
    if args.command == "validate-corpus":
        emit({"pass": True, "schema_version": SCHEMA_VERSION, "cases": [case["id"] for case in cases]})
        return 0
    if args.command == "run-reference":
        results = [run_reference_case(case) for case in cases]
        emit({"pass": all(result["pass"] for result in results), "results": results})
        return 0 if all(result["pass"] for result in results) else 1
    if args.command == "score":
        result = score_workspace(cases[0], Path(args.workspace))
        emit(result)
        return 0 if result["pass"] else 1
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
