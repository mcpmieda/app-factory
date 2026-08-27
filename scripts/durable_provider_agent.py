#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.durable_provider_agent import (  # noqa: E402
    DurableProviderResult,
    FactoryLease,
    LeaseHeartbeat,
    assert_lease_authorizes,
    evaluate_result,
    manifest_fingerprint,
    parse_timestamp,
    request_fingerprint,
)
from engine.provider_runtime import (  # noqa: E402
    ProviderExecutionResult,
    SubprocessRunner,
    execute_provider_task,
    redact_text,
)
from scripts.provider_worker import build_adapter, load_request  # noqa: E402


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def load_object(path: Path, *, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def load_manifest(path: Path) -> Mapping[str, Any]:
    return load_object(path, label="Factory Run manifest")


def load_lease(path: Path) -> FactoryLease:
    return FactoryLease.from_mapping(load_object(path, label="lease"))


def parse_metrics(values: list[str]) -> dict[str, int | float]:
    metrics: dict[str, int | float] = {}
    for raw in values:
        key, separator, value = raw.partition("=")
        key = key.strip()
        value = value.strip()
        if not separator or not key or key in metrics:
            raise ValueError(f"invalid or duplicate metric: {raw}")
        try:
            numeric: int | float = int(value)
        except ValueError:
            try:
                numeric = float(value)
            except ValueError as error:
                raise ValueError(f"metric must be numeric: {raw}") from error
        metrics[key] = numeric
    return metrics


def add_provider_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--binary")
    parser.add_argument("--model")
    parser.add_argument("--agent")
    parser.add_argument("--effort", choices=("low", "medium", "high"))
    parser.add_argument("--ollama-binary")
    parser.add_argument("--ollama-base-url")
    parser.add_argument(
        "--profile-home",
        type=Path,
        help="Dedicated isolated provider profile outside the worktree",
    )


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description=(
            "GitHub-backed durable executor for App Factory local/headless providers. "
            "The GitHub Control Plane remains the final authority."
        )
    )
    sub = root.add_subparsers(dest="command", required=True)

    fingerprint = sub.add_parser(
        "fingerprint",
        help="Calculate portable request and immutable manifest fingerprints",
    )
    fingerprint.add_argument("spec", type=Path)
    fingerprint.add_argument("manifest", type=Path)

    validate = sub.add_parser(
        "validate",
        help="Validate that a trusted active lease exactly authorizes this executor",
    )
    validate.add_argument("spec", type=Path)
    validate.add_argument("manifest", type=Path)
    validate.add_argument("lease", type=Path)
    validate.add_argument("--worker-id", required=True)
    validate.add_argument("--at", help="ISO-8601 validation time; defaults to now")

    heartbeat = sub.add_parser(
        "heartbeat",
        help="Emit a sanitized heartbeat candidate for GitHub Control Plane validation",
    )
    heartbeat.add_argument("lease", type=Path)
    heartbeat.add_argument("--phase", required=True)
    heartbeat.add_argument("--head-sha")
    heartbeat.add_argument("--detail", default="")
    heartbeat.add_argument("--metric", action="append", default=[])
    heartbeat.add_argument("--at", help="ISO-8601 observation time; defaults to now")

    run = sub.add_parser(
        "run",
        help="Execute, validate, commit, and publish the exact leased worker task",
    )
    run.add_argument("spec", type=Path)
    run.add_argument("manifest", type=Path)
    run.add_argument("lease", type=Path)
    run.add_argument("--worker-id", required=True)
    run.add_argument(
        "--publish",
        action="store_true",
        help="Required: completion without a confirmed remote worker SHA is forbidden",
    )
    add_provider_options(run)
    return root


def validation_time(raw: str | None) -> datetime:
    if raw:
        return parse_timestamp(raw, label="validation time")
    return datetime.now(timezone.utc)


def fingerprint_payload(spec: Path, manifest_path: Path) -> dict[str, Any]:
    request = load_request(spec)
    manifest = load_manifest(manifest_path)
    return {
        "schema_version": 1,
        "run_id": request.run_id,
        "task_id": request.task_id,
        "repository": request.repository,
        "request_sha256": request_fingerprint(request),
        "manifest_sha256": manifest_fingerprint(manifest),
    }


def validate_command(args: argparse.Namespace) -> int:
    request = load_request(args.spec)
    manifest = load_manifest(args.manifest)
    lease = load_lease(args.lease)
    assert_lease_authorizes(
        lease,
        request,
        manifest,
        worker_id=args.worker_id,
        when=validation_time(args.at),
    )
    emit({
        "authorized": True,
        "lease_id": lease.lease_id,
        "issue_number": lease.issue_number,
        "provider_id": lease.provider_id,
        "worker_id": lease.worker_id,
        "working_branch": lease.working_branch,
        "expires_at": lease.expires_at,
        "request_sha256": lease.request_sha256,
        "manifest_sha256": lease.manifest_sha256,
        "authority": "github-control-plane",
    })
    return 0


def heartbeat_command(args: argparse.Namespace) -> int:
    lease = load_lease(args.lease)
    observed = validation_time(args.at)
    if not lease.active_at(observed):
        raise ValueError("heartbeat requires an active trusted lease")
    heartbeat = LeaseHeartbeat.from_lease(
        lease,
        phase=args.phase,
        head_sha=args.head_sha,
        detail=args.detail,
        metrics=parse_metrics(args.metric),
        observed_at=observed.astimezone(timezone.utc).replace(microsecond=0).isoformat(),
    )
    emit({
        "candidate": "heartbeat",
        "heartbeat": heartbeat.to_dict(),
        "authority": "pending-github-control-plane-validation",
    })
    return 0


def run_command(args: argparse.Namespace) -> int:
    if not args.publish:
        raise ValueError("run requires --publish; local-only completion is forbidden")
    request = load_request(args.spec)
    manifest = load_manifest(args.manifest)
    lease = load_lease(args.lease)
    assert_lease_authorizes(
        lease,
        request,
        manifest,
        worker_id=args.worker_id,
    )

    args.provider = lease.provider_id
    adapter = build_adapter(args)
    if adapter.provider_id != lease.provider_id:
        raise ValueError("configured adapter does not match the trusted lease provider")

    execution: ProviderExecutionResult = execute_provider_task(
        adapter,
        request,
        runner=SubprocessRunner(),
        publish=True,
    )
    result = DurableProviderResult.from_execution(lease, execution)
    decision = evaluate_result(lease, result, request, manifest)
    emit({
        "candidate": "provider-result",
        "result": result.to_dict(),
        "decision": decision.to_dict(),
        "authority": "pending-github-control-plane-validation",
    })
    if not decision.accepted:
        return 1
    return 0 if decision.completed else 2


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "fingerprint":
            emit(fingerprint_payload(args.spec, args.manifest))
            return 0
        if args.command == "validate":
            return validate_command(args)
        if args.command == "heartbeat":
            return heartbeat_command(args)
        if args.command == "run":
            return run_command(args)
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        emit({"valid": False, "error": redact_text(error)})
        return 1
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
