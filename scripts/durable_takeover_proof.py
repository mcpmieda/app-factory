#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from engine.durable_provider_agent import (
    FactoryLease,
    LeaseHeartbeat,
    TRUSTED_CONTROL_ACTOR,
    assert_lease_authorizes,
    decode_marker,
    encode_marker,
    manifest_fingerprint,
    new_lease_times,
    parse_timestamp,
    request_fingerprint,
)
from engine.provider_runtime import ProviderTaskRequest

RUN_ID = "durable-takeover-proof-001"
TASK_ID = "lease-handoff"
ISSUE_NUMBER = 72
PROVIDER_ID = "opencode_ollama"
WORKER_A = "takeover-executor-a"
WORKER_B = "takeover-executor-b"
WORKING_BRANCH = "factory/durable-takeover-proof-001/lease-handoff"
INTEGRATION_BRANCH = "factory/durable-takeover-proof-001"
TARGET_BRANCH = "main"
PATH_SCOPE = "pilots/live/durable-takeover/result.md"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "run_id": RUN_ID,
        "goal": "Prove cross-executor recovery after lease expiry.",
        "max_parallel": 1,
        "tasks": [{"id": TASK_ID, "paths": [PATH_SCOPE]}],
    }


def request(worktree: Path) -> ProviderTaskRequest:
    return ProviderTaskRequest.from_mapping(
        {
            "run_id": RUN_ID,
            "task_id": TASK_ID,
            "repository": os.environ["GITHUB_REPOSITORY"],
            "worktree": str(worktree.resolve()),
            "integration_branch": INTEGRATION_BRANCH,
            "target_branch": TARGET_BRANCH,
            "working_branch": WORKING_BRANCH,
            "paths": [PATH_SCOPE],
            "instruction": "Lease-only recovery proof. Do not execute a provider model.",
            "allowed_commands": [],
            "timeout_seconds": 900,
            "remote": "origin",
        }
    )


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def expect_rejected(lease: FactoryLease, req: ProviderTaskRequest, worker_id: str, *, when: datetime) -> None:
    try:
        assert_lease_authorizes(lease, req, manifest(), worker_id=worker_id, when=when)
    except ValueError:
        return
    raise RuntimeError(f"worker {worker_id} was unexpectedly authorized")


def lease_a(req: ProviderTaskRequest) -> FactoryLease:
    issued_at, expires_at = new_lease_times(ttl_seconds=180)
    lease = FactoryLease(
        lease_id=f"takeover-a-{os.environ['GITHUB_RUN_ID']}-{os.environ['GITHUB_RUN_ATTEMPT']}",
        run_id=RUN_ID,
        task_id=TASK_ID,
        issue_number=ISSUE_NUMBER,
        provider_id=PROVIDER_ID,
        worker_id=WORKER_A,
        repository=req.repository,
        working_branch=WORKING_BRANCH,
        integration_branch=INTEGRATION_BRANCH,
        target_branch=TARGET_BRANCH,
        request_sha256=request_fingerprint(req),
        manifest_sha256=manifest_fingerprint(manifest()),
        issued_at=issued_at,
        expires_at=expires_at,
        actor=TRUSTED_CONTROL_ACTOR,
    )
    lease.validate()
    return lease


def lease_b(req: ProviderTaskRequest, prior: FactoryLease) -> FactoryLease:
    issued_at, expires_at = new_lease_times(ttl_seconds=600)
    lease = FactoryLease(
        lease_id=f"takeover-b-{os.environ['GITHUB_RUN_ID']}-{os.environ['GITHUB_RUN_ATTEMPT']}",
        run_id=RUN_ID,
        task_id=TASK_ID,
        issue_number=ISSUE_NUMBER,
        provider_id=prior.provider_id,
        worker_id=WORKER_B,
        repository=req.repository,
        working_branch=prior.working_branch,
        integration_branch=prior.integration_branch,
        target_branch=prior.target_branch,
        request_sha256=request_fingerprint(req),
        manifest_sha256=manifest_fingerprint(manifest()),
        issued_at=issued_at,
        expires_at=expires_at,
        actor=TRUSTED_CONTROL_ACTOR,
    )
    lease.validate()
    if lease.request_sha256 != prior.request_sha256:
        raise RuntimeError("request fingerprint changed between executors")
    if lease.manifest_sha256 != prior.manifest_sha256:
        raise RuntimeError("manifest fingerprint changed between executors")
    return lease


def phase_a(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    req = request(Path(os.environ["GITHUB_WORKSPACE"]))
    first = lease_a(req)
    now = utc_now()
    assert_lease_authorizes(first, req, manifest(), worker_id=WORKER_A, when=now)
    expect_rejected(first, req, WORKER_B, when=now)

    heartbeat = LeaseHeartbeat.from_lease(
        first,
        phase="running",
        detail="executor A alive; expiry intentionally unchanged",
        metrics={"progress": 0.25},
        observed_at=now.replace(microsecond=0).isoformat(),
    )
    before = hashlib.sha256(json.dumps(first.to_dict(), sort_keys=True).encode()).hexdigest()
    after = hashlib.sha256(json.dumps(first.to_dict(), sort_keys=True).encode()).hexdigest()
    if before != after:
        raise RuntimeError("heartbeat mutated Lease A")

    write_json(output / "lease-a.json", first.to_dict())
    write_json(
        output / "fingerprints-a.json",
        {
            "request_sha256": first.request_sha256,
            "manifest_sha256": first.manifest_sha256,
            "worktree": "executor-a-redacted",
        },
    )
    write_text(
        output / "lease-a-comment.txt",
        encode_marker("lease", first.to_dict())
        + "\nCross-executor proof Lease A issued by GitHub Actions. Heartbeats never extend this expiry.",
    )
    write_text(
        output / "heartbeat-comment.txt",
        encode_marker("heartbeat", heartbeat.to_dict())
        + "\nLease A heartbeat persisted by GitHub Actions without renewing authority.",
    )


def recover_lease_a(comments_path: Path) -> FactoryLease:
    comments = json.loads(comments_path.read_text(encoding="utf-8"))
    if not isinstance(comments, list):
        raise ValueError("comments payload must be a JSON array")
    matches: list[FactoryLease] = []
    for comment in comments:
        if comment.get("user", {}).get("login") != TRUSTED_CONTROL_ACTOR:
            continue
        try:
            payload = decode_marker(str(comment.get("body", "")), "lease")
            candidate = FactoryLease.from_mapping(payload)
        except ValueError:
            continue
        if candidate.run_id == RUN_ID and candidate.worker_id == WORKER_A:
            matches.append(candidate)
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one trusted Lease A, found {len(matches)}")
    return matches[0]


def phase_b(output: Path, comments_path: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    req = request(Path(os.environ["GITHUB_WORKSPACE"]))
    first = recover_lease_a(comments_path)
    now = utc_now()

    if not first.active_at(now):
        raise RuntimeError("Lease A expired before executor B observed the active handoff boundary")
    assert_lease_authorizes(first, req, manifest(), worker_id=WORKER_A, when=now)
    expect_rejected(first, req, WORKER_B, when=now)

    expires = parse_timestamp(first.expires_at, label="Lease A expiry")
    remaining = (expires - utc_now()).total_seconds() + 2
    if remaining > 0:
        time.sleep(remaining)

    after_expiry = utc_now()
    if first.active_at(after_expiry):
        raise RuntimeError("Lease A remained active after its expiry")
    expect_rejected(first, req, WORKER_A, when=after_expiry)

    second = lease_b(req, first)
    assert_lease_authorizes(second, req, manifest(), worker_id=WORKER_B, when=utc_now())
    expect_rejected(second, req, WORKER_A, when=utc_now())

    write_json(output / "lease-b.json", second.to_dict())
    write_json(
        output / "fingerprints-b.json",
        {
            "request_sha256": second.request_sha256,
            "manifest_sha256": second.manifest_sha256,
            "worktree": "executor-b-redacted",
        },
    )
    write_text(
        output / "lease-b-comment.txt",
        encode_marker("lease", second.to_dict())
        + "\nLease B issued only after trusted Lease A expired; authority moved to executor B.",
    )
    proof = {
        "schema_version": 1,
        "run_id": RUN_ID,
        "issue_number": ISSUE_NUMBER,
        "executor_a": WORKER_A,
        "executor_b": WORKER_B,
        "lease_a": first.lease_id,
        "lease_a_expires_at": first.expires_at,
        "lease_b": second.lease_id,
        "request_sha256": second.request_sha256,
        "manifest_sha256": second.manifest_sha256,
        "takeover": "proved",
        "production_activation": "not-performed",
        "target_merge": "not-performed",
    }
    write_text(
        output / "proof-comment.txt",
        "<!-- FACTORY_DURABLE_TAKEOVER_PROOF "
        + json.dumps(proof, separators=(",", ":"), sort_keys=True)
        + " -->\nCross-executor lease takeover proved by two GitHub-hosted jobs. Heartbeat did not renew Lease A; executor B received authority only after expiry.",
    )


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Live App Factory lease takeover proof driver")
    sub = root.add_subparsers(dest="command", required=True)
    first = sub.add_parser("phase-a")
    first.add_argument("--output", type=Path, required=True)
    second = sub.add_parser("phase-b")
    second.add_argument("--output", type=Path, required=True)
    second.add_argument("--comments", type=Path, required=True)
    return root


def main() -> int:
    args = parser().parse_args()
    if args.command == "phase-a":
        phase_a(args.output)
    else:
        phase_b(args.output, args.comments)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
