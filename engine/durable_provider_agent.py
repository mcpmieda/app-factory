from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Mapping

from engine.provider_runtime import (
    REPOSITORY_PATTERN,
    RUNTIME_SCHEMA_VERSION,
    SHA_PATTERN,
    DurableEvidence,
    ProviderExecutionResult,
    ProviderTaskRequest,
    redact_text,
    sanitize_value,
    validate_branch_name,
    validate_changed_paths,
)

DURABLE_AGENT_SCHEMA_VERSION = 1
TRUSTED_CONTROL_ACTOR = "github-actions[bot]"
AUTOMATIC_DURABLE_PROVIDERS = frozenset({"antigravity", "opencode_ollama"})
LEASE_TTL_MIN_SECONDS = 60
LEASE_TTL_MAX_SECONDS = 21_600
HEARTBEAT_PHASES = frozenset({"claimed", "preparing", "running", "publishing", "completed", "failed"})
TERMINAL_RESULT_STATES = frozenset({"success", "failed", "canceled", "interrupted"})
FINGERPRINT_PATTERN = re.compile(r"^[0-9a-f]{64}$")
IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9._:@/-]{1,160}$")
MARKER_KIND_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]{0,31}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_timestamp(value: str, *, label: str) -> datetime:
    raw = str(value or "").strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError as error:
        raise ValueError(f"invalid {label}: {value}") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def sha256_fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def validate_fingerprint(value: str, *, label: str) -> str:
    fingerprint = str(value or "").strip().lower()
    if not FINGERPRINT_PATTERN.fullmatch(fingerprint):
        raise ValueError(f"invalid {label}")
    return fingerprint


def validate_identifier(value: str, *, label: str) -> str:
    identifier = str(value or "").strip()
    if not IDENTIFIER_PATTERN.fullmatch(identifier):
        raise ValueError(f"invalid {label}: {value}")
    return identifier


def portable_request_payload(request: ProviderTaskRequest) -> dict[str, Any]:
    request.validate()
    return {
        "schema_version": RUNTIME_SCHEMA_VERSION,
        "run_id": request.run_id,
        "task_id": request.task_id,
        "repository": request.repository,
        "integration_branch": request.integration_branch,
        "target_branch": request.target_branch,
        "working_branch": request.working_branch,
        "paths": list(request.normalized_paths),
        "instruction": request.instruction,
        "allowed_commands": list(request.normalized_commands),
        "timeout_seconds": request.timeout_seconds,
        "remote": request.remote,
    }


def request_fingerprint(request: ProviderTaskRequest) -> str:
    return sha256_fingerprint(portable_request_payload(request))


def manifest_fingerprint(manifest: Mapping[str, Any]) -> str:
    if not isinstance(manifest, Mapping):
        raise ValueError("Factory Run manifest must be a JSON object")
    return sha256_fingerprint(dict(manifest))


@dataclass(frozen=True)
class FactoryLease:
    lease_id: str
    run_id: str
    task_id: str
    issue_number: int
    provider_id: str
    worker_id: str
    repository: str
    working_branch: str
    integration_branch: str
    target_branch: str
    request_sha256: str
    manifest_sha256: str
    issued_at: str
    expires_at: str
    actor: str
    schema_version: int = DURABLE_AGENT_SCHEMA_VERSION

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "FactoryLease":
        if not isinstance(raw, Mapping):
            raise ValueError("lease must be a JSON object")
        lease = cls(
            lease_id=str(raw.get("lease_id") or ""),
            run_id=str(raw.get("run_id") or ""),
            task_id=str(raw.get("task_id") or ""),
            issue_number=int(raw.get("issue_number") or 0),
            provider_id=str(raw.get("provider_id") or ""),
            worker_id=str(raw.get("worker_id") or ""),
            repository=str(raw.get("repository") or ""),
            working_branch=str(raw.get("working_branch") or ""),
            integration_branch=str(raw.get("integration_branch") or ""),
            target_branch=str(raw.get("target_branch") or ""),
            request_sha256=str(raw.get("request_sha256") or ""),
            manifest_sha256=str(raw.get("manifest_sha256") or ""),
            issued_at=str(raw.get("issued_at") or ""),
            expires_at=str(raw.get("expires_at") or ""),
            actor=str(raw.get("actor") or ""),
            schema_version=int(raw.get("schema_version") or 0),
        )
        lease.validate()
        return lease

    @property
    def trusted(self) -> bool:
        return self.actor == TRUSTED_CONTROL_ACTOR

    @property
    def issued_time(self) -> datetime:
        return parse_timestamp(self.issued_at, label="lease issued_at")

    @property
    def expiry_time(self) -> datetime:
        return parse_timestamp(self.expires_at, label="lease expires_at")

    def active_at(self, when: datetime) -> bool:
        point = when.astimezone(timezone.utc)
        return self.trusted and self.issued_time <= point < self.expiry_time

    def validate(self) -> None:
        if self.schema_version != DURABLE_AGENT_SCHEMA_VERSION:
            raise ValueError(f"unsupported durable agent schema_version: {self.schema_version}")
        validate_identifier(self.lease_id, label="lease_id")
        validate_identifier(self.run_id, label="run_id")
        validate_identifier(self.task_id, label="task_id")
        validate_identifier(self.worker_id, label="worker_id")
        if self.issue_number <= 0:
            raise ValueError("issue_number must be positive")
        if self.provider_id not in AUTOMATIC_DURABLE_PROVIDERS:
            raise ValueError(f"provider is not eligible for durable automatic execution: {self.provider_id}")
        if not REPOSITORY_PATTERN.fullmatch(self.repository):
            raise ValueError("repository must use owner/name form")
        worker = validate_branch_name(self.working_branch, label="worker branch")
        integration = validate_branch_name(self.integration_branch, label="integration branch")
        target = validate_branch_name(self.target_branch, label="target branch")
        if len({worker, integration, target}) != 3:
            raise ValueError("worker, integration, and target branches must be distinct")
        validate_fingerprint(self.request_sha256, label="request_sha256")
        validate_fingerprint(self.manifest_sha256, label="manifest_sha256")
        issued = self.issued_time
        expires = self.expiry_time
        ttl = (expires - issued).total_seconds()
        if not LEASE_TTL_MIN_SECONDS <= ttl <= LEASE_TTL_MAX_SECONDS:
            raise ValueError(
                f"lease TTL must be between {LEASE_TTL_MIN_SECONDS} and {LEASE_TTL_MAX_SECONDS} seconds"
            )
        if not self.actor:
            raise ValueError("lease actor is required")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema_version": self.schema_version,
            "lease_id": self.lease_id,
            "run_id": self.run_id,
            "task_id": self.task_id,
            "issue_number": self.issue_number,
            "provider_id": self.provider_id,
            "worker_id": self.worker_id,
            "repository": self.repository,
            "working_branch": self.working_branch,
            "integration_branch": self.integration_branch,
            "target_branch": self.target_branch,
            "request_sha256": self.request_sha256,
            "manifest_sha256": self.manifest_sha256,
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "actor": self.actor,
        }


@dataclass(frozen=True)
class LeaseHeartbeat:
    lease_id: str
    run_id: str
    task_id: str
    provider_id: str
    worker_id: str
    phase: str
    observed_at: str = field(default_factory=utc_now)
    head_sha: str | None = None
    detail: str = ""
    metrics: Mapping[str, int | float] = field(default_factory=dict)
    schema_version: int = DURABLE_AGENT_SCHEMA_VERSION

    @classmethod
    def from_lease(
        cls,
        lease: FactoryLease,
        *,
        phase: str,
        head_sha: str | None = None,
        detail: str = "",
        metrics: Mapping[str, int | float] | None = None,
        observed_at: str | None = None,
    ) -> "LeaseHeartbeat":
        lease.validate()
        heartbeat = cls(
            lease_id=lease.lease_id,
            run_id=lease.run_id,
            task_id=lease.task_id,
            provider_id=lease.provider_id,
            worker_id=lease.worker_id,
            phase=phase,
            observed_at=observed_at or utc_now(),
            head_sha=head_sha,
            detail=detail,
            metrics=dict(metrics or {}),
        )
        heartbeat.validate()
        return heartbeat

    def validate(self) -> None:
        if self.schema_version != DURABLE_AGENT_SCHEMA_VERSION:
            raise ValueError("unsupported heartbeat schema_version")
        validate_identifier(self.lease_id, label="lease_id")
        validate_identifier(self.run_id, label="run_id")
        validate_identifier(self.task_id, label="task_id")
        validate_identifier(self.worker_id, label="worker_id")
        if self.provider_id not in AUTOMATIC_DURABLE_PROVIDERS:
            raise ValueError("invalid heartbeat provider")
        if self.phase not in HEARTBEAT_PHASES:
            raise ValueError(f"invalid heartbeat phase: {self.phase}")
        parse_timestamp(self.observed_at, label="heartbeat observed_at")
        if self.head_sha is not None and not SHA_PATTERN.fullmatch(self.head_sha):
            raise ValueError("heartbeat head_sha is invalid")
        if any(not isinstance(value, (int, float)) for value in self.metrics.values()):
            raise ValueError("heartbeat metrics must be numeric")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema_version": self.schema_version,
            "lease_id": self.lease_id,
            "run_id": self.run_id,
            "task_id": self.task_id,
            "provider_id": self.provider_id,
            "worker_id": self.worker_id,
            "phase": self.phase,
            "observed_at": self.observed_at,
            "head_sha": self.head_sha,
            "detail": redact_text(self.detail),
            "metrics": dict(self.metrics),
        }


@dataclass(frozen=True)
class DurableProviderResult:
    lease_id: str
    run_id: str
    task_id: str
    issue_number: int
    provider_id: str
    worker_id: str
    status: str
    branch: str
    commit_sha: str
    remote_sha: str
    changed_paths: tuple[str, ...]
    pushed: bool
    request_sha256: str
    manifest_sha256: str
    observed_at: str = field(default_factory=utc_now)
    session_id: str | None = None
    error: str | None = None
    schema_version: int = DURABLE_AGENT_SCHEMA_VERSION

    @classmethod
    def from_execution(
        cls,
        lease: FactoryLease,
        execution: ProviderExecutionResult,
        *,
        observed_at: str | None = None,
    ) -> "DurableProviderResult":
        lease.validate()
        evidence: DurableEvidence | None = execution.evidence
        result = cls(
            lease_id=lease.lease_id,
            run_id=lease.run_id,
            task_id=lease.task_id,
            issue_number=lease.issue_number,
            provider_id=lease.provider_id,
            worker_id=lease.worker_id,
            status=execution.output.status,
            branch=evidence.branch if evidence else "",
            commit_sha=evidence.commit_sha if evidence else "",
            remote_sha=evidence.commit_sha if evidence and evidence.complete else "",
            changed_paths=evidence.changed_paths if evidence else (),
            pushed=bool(evidence and evidence.pushed),
            request_sha256=lease.request_sha256,
            manifest_sha256=lease.manifest_sha256,
            observed_at=observed_at or utc_now(),
            session_id=execution.output.session_id,
            error=execution.output.error,
        )
        result.validate()
        return result

    def validate(self) -> None:
        if self.schema_version != DURABLE_AGENT_SCHEMA_VERSION:
            raise ValueError("unsupported provider result schema_version")
        validate_identifier(self.lease_id, label="lease_id")
        validate_identifier(self.run_id, label="run_id")
        validate_identifier(self.task_id, label="task_id")
        validate_identifier(self.worker_id, label="worker_id")
        if self.issue_number <= 0:
            raise ValueError("provider result issue_number must be positive")
        if self.provider_id not in AUTOMATIC_DURABLE_PROVIDERS:
            raise ValueError("invalid provider result provider")
        if self.status not in TERMINAL_RESULT_STATES:
            raise ValueError(f"invalid provider result status: {self.status}")
        validate_fingerprint(self.request_sha256, label="request_sha256")
        validate_fingerprint(self.manifest_sha256, label="manifest_sha256")
        parse_timestamp(self.observed_at, label="provider result observed_at")
        if self.status == "success":
            validate_branch_name(self.branch, label="provider result branch")
            if not SHA_PATTERN.fullmatch(self.commit_sha):
                raise ValueError("provider result commit_sha is invalid")
            if not SHA_PATTERN.fullmatch(self.remote_sha):
                raise ValueError("provider result remote_sha is invalid")
            if not self.changed_paths:
                raise ValueError("successful provider result requires changed_paths")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema_version": self.schema_version,
            "lease_id": self.lease_id,
            "run_id": self.run_id,
            "task_id": self.task_id,
            "issue_number": self.issue_number,
            "provider_id": self.provider_id,
            "worker_id": self.worker_id,
            "status": self.status,
            "branch": self.branch,
            "commit_sha": self.commit_sha,
            "remote_sha": self.remote_sha,
            "changed_paths": list(self.changed_paths),
            "pushed": self.pushed,
            "request_sha256": self.request_sha256,
            "manifest_sha256": self.manifest_sha256,
            "observed_at": self.observed_at,
            "session_id": redact_text(self.session_id) if self.session_id else None,
            "error": redact_text(self.error) if self.error else None,
        }


@dataclass(frozen=True)
class ResultDecision:
    accepted: bool
    completed: bool
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "accepted": self.accepted,
            "completed": self.completed,
            "reasons": list(self.reasons),
        }


def lease_binding_reasons(
    lease: FactoryLease,
    request: ProviderTaskRequest,
    manifest: Mapping[str, Any],
    *,
    worker_id: str,
    when: datetime,
    require_active: bool = True,
) -> tuple[str, ...]:
    reasons: list[str] = []
    try:
        lease.validate()
        request.validate()
    except ValueError as error:
        return (str(error),)
    if not lease.trusted:
        reasons.append("lease was not issued by github-actions[bot]")
    if require_active and not lease.active_at(when):
        reasons.append("lease is not active")
    expected = {
        "run_id": request.run_id,
        "task_id": request.task_id,
        "repository": request.repository,
        "working_branch": request.working_branch,
        "integration_branch": request.integration_branch,
        "target_branch": request.target_branch,
        "worker_id": worker_id,
        "request_sha256": request_fingerprint(request),
        "manifest_sha256": manifest_fingerprint(manifest),
    }
    for field_name, expected_value in expected.items():
        if getattr(lease, field_name) != expected_value:
            reasons.append(f"lease {field_name} does not match the durable task contract")
    return tuple(reasons)


def assert_lease_authorizes(
    lease: FactoryLease,
    request: ProviderTaskRequest,
    manifest: Mapping[str, Any],
    *,
    worker_id: str,
    when: datetime | None = None,
) -> FactoryLease:
    reasons = lease_binding_reasons(
        lease,
        request,
        manifest,
        worker_id=worker_id,
        when=when or datetime.now(timezone.utc),
        require_active=True,
    )
    if reasons:
        raise ValueError("; ".join(reasons))
    return lease


def evaluate_result(
    lease: FactoryLease,
    result: DurableProviderResult,
    request: ProviderTaskRequest,
    manifest: Mapping[str, Any],
) -> ResultDecision:
    reasons = list(
        lease_binding_reasons(
            lease,
            request,
            manifest,
            worker_id=result.worker_id,
            when=parse_timestamp(result.observed_at, label="provider result observed_at"),
            require_active=True,
        )
    )
    try:
        result.validate()
    except ValueError as error:
        reasons.append(str(error))
        return ResultDecision(False, False, tuple(dict.fromkeys(reasons)))
    comparisons = {
        "lease_id": lease.lease_id,
        "run_id": lease.run_id,
        "task_id": lease.task_id,
        "issue_number": lease.issue_number,
        "provider_id": lease.provider_id,
        "request_sha256": lease.request_sha256,
        "manifest_sha256": lease.manifest_sha256,
    }
    for field_name, expected in comparisons.items():
        if getattr(result, field_name) != expected:
            reasons.append(f"provider result {field_name} does not match the lease")
    if result.status == "success":
        if result.branch != lease.working_branch:
            reasons.append("provider result branch does not match the leased worker branch")
        if not result.pushed:
            reasons.append("successful provider result was not pushed")
        if result.commit_sha != result.remote_sha:
            reasons.append("provider result remote SHA does not match the validated commit")
        try:
            validate_changed_paths(result.changed_paths, request.normalized_paths)
        except ValueError as error:
            reasons.append(str(error))
    accepted = not reasons
    completed = accepted and result.status == "success"
    default_reason = (
        "durable provider result is complete and ready for control-plane CI reconciliation"
        if completed
        else "terminal provider failure is bound to the trusted lease"
    )
    return ResultDecision(accepted, completed, tuple(reasons) or (default_reason,))


def select_recoverable_lease(
    leases: Iterable[FactoryLease],
    request: ProviderTaskRequest,
    manifest: Mapping[str, Any],
    *,
    worker_id: str,
    when: datetime | None = None,
) -> FactoryLease | None:
    point = when or datetime.now(timezone.utc)
    active: list[FactoryLease] = []
    for lease in leases:
        if not lease_binding_reasons(
            lease,
            request,
            manifest,
            worker_id=worker_id,
            when=point,
            require_active=True,
        ):
            active.append(lease)
    if len(active) > 1:
        raise ValueError("multiple active trusted leases match the same durable task")
    return active[0] if active else None


def encode_marker(kind: str, payload: Mapping[str, Any]) -> str:
    marker_kind = str(kind or "").strip().upper()
    if not MARKER_KIND_PATTERN.fullmatch(marker_kind):
        raise ValueError(f"invalid marker kind: {kind}")
    rendered = canonical_json(sanitize_value(dict(payload)))
    if "-->" in rendered:
        raise ValueError("marker payload contains an unsafe terminator")
    return f"<!-- FACTORY_PROVIDER_{marker_kind} {rendered} -->"


def decode_marker(body: str, kind: str) -> dict[str, Any] | None:
    marker_kind = str(kind or "").strip().upper()
    if not MARKER_KIND_PATTERN.fullmatch(marker_kind):
        raise ValueError(f"invalid marker kind: {kind}")
    pattern = re.compile(
        rf"<!--\s*FACTORY_PROVIDER_{re.escape(marker_kind)}\s+(\{{.*?\}})\s*-->",
        re.DOTALL,
    )
    match = pattern.search(str(body or ""))
    if not match:
        return None
    try:
        value = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        raise ValueError("invalid durable provider marker JSON") from error
    if not isinstance(value, dict):
        raise ValueError("durable provider marker payload must be an object")
    return value


def new_lease_times(*, issued_at: datetime | None = None, ttl_seconds: int = 1800) -> tuple[str, str]:
    if not LEASE_TTL_MIN_SECONDS <= int(ttl_seconds) <= LEASE_TTL_MAX_SECONDS:
        raise ValueError("lease ttl_seconds is outside the allowed range")
    issued = (issued_at or datetime.now(timezone.utc)).astimezone(timezone.utc).replace(microsecond=0)
    expires = issued + timedelta(seconds=int(ttl_seconds))
    return issued.isoformat(), expires.isoformat()
