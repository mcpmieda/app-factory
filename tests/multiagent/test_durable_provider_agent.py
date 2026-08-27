from __future__ import annotations

import tempfile
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

from engine.durable_provider_agent import (
    AUTOMATIC_DURABLE_PROVIDERS,
    DURABLE_AGENT_SCHEMA_VERSION,
    TRUSTED_CONTROL_ACTOR,
    DurableProviderResult,
    FactoryLease,
    LeaseHeartbeat,
    ResultDecision,
    assert_lease_authorizes,
    canonical_json,
    decode_marker,
    encode_marker,
    evaluate_result,
    lease_binding_reasons,
    manifest_fingerprint,
    new_lease_times,
    parse_timestamp,
    portable_request_payload,
    request_fingerprint,
    select_recoverable_lease,
    sha256_fingerprint,
    utc_now,
    validate_fingerprint,
    validate_identifier,
)
from engine.provider_runtime import (
    DurableEvidence,
    ProviderExecutionResult,
    ProviderRunOutput,
    ProviderTaskRequest,
)

SHA_A = "a" * 40
SHA_B = "b" * 40
NOW = datetime(2026, 8, 27, 12, 0, tzinfo=timezone.utc)


class DurableProviderAgentTests(unittest.TestCase):
    @staticmethod
    def manifest(**overrides):
        value = {
            "schema_version": 1,
            "run_id": "durable-run",
            "goal": "Prove recovery without the initiating computer.",
            "max_parallel": 2,
            "tasks": [{"id": "worker-a", "paths": ["docs/worker-a"]}],
        }
        value.update(overrides)
        return value

    @staticmethod
    def request(worktree: Path, **overrides) -> ProviderTaskRequest:
        raw = {
            "run_id": "durable-run",
            "task_id": "worker-a",
            "repository": "owner/repo",
            "worktree": str(worktree),
            "integration_branch": "factory/durable-run",
            "target_branch": "main",
            "working_branch": "factory/durable-run/worker-a",
            "paths": ["docs/worker-a"],
            "instruction": "Create durable provider evidence.",
            "allowed_commands": ["python -m unittest*"],
            "timeout_seconds": 900,
            "remote": "origin",
        }
        raw.update(overrides)
        return ProviderTaskRequest.from_mapping(raw)

    def lease(
        self,
        request: ProviderTaskRequest,
        manifest=None,
        **overrides,
    ) -> FactoryLease:
        issued = NOW - timedelta(minutes=5)
        expires = NOW + timedelta(minutes=25)
        value = FactoryLease(
            lease_id="lease-001",
            run_id=request.run_id,
            task_id=request.task_id,
            issue_number=101,
            provider_id="antigravity",
            worker_id="executor-01",
            repository=request.repository,
            working_branch=request.working_branch,
            integration_branch=request.integration_branch,
            target_branch=request.target_branch,
            request_sha256=request_fingerprint(request),
            manifest_sha256=manifest_fingerprint(manifest or self.manifest()),
            issued_at=issued.isoformat(),
            expires_at=expires.isoformat(),
            actor=TRUSTED_CONTROL_ACTOR,
        )
        return replace(value, **overrides)

    def test_timestamp_canonicalization_and_fingerprint_helpers(self) -> None:
        now_text = utc_now()
        self.assertIsNotNone(parse_timestamp(now_text, label="now").tzinfo)
        self.assertEqual(
            parse_timestamp("2026-08-27T12:00:00Z", label="zulu"),
            NOW,
        )
        with self.assertRaisesRegex(ValueError, "invalid broken"):
            parse_timestamp("not-a-date", label="broken")
        with self.assertRaisesRegex(ValueError, "timezone"):
            parse_timestamp("2026-08-27T12:00:00", label="naive")

        left = {"b": 2, "a": [1, {"z": True}]}
        right = {"a": [1, {"z": True}], "b": 2}
        self.assertEqual(canonical_json(left), canonical_json(right))
        self.assertEqual(sha256_fingerprint(left), sha256_fingerprint(right))
        self.assertNotEqual(sha256_fingerprint(left), sha256_fingerprint({"b": 3}))
        self.assertEqual(validate_fingerprint("A" * 64, label="fingerprint"), "a" * 64)
        with self.assertRaisesRegex(ValueError, "fingerprint"):
            validate_fingerprint("bad", label="fingerprint")
        self.assertEqual(validate_identifier("worker:host-1", label="worker"), "worker:host-1")
        with self.assertRaisesRegex(ValueError, "worker"):
            validate_identifier("bad worker", label="worker")
        with self.assertRaisesRegex(ValueError, "manifest"):
            manifest_fingerprint(["not", "an", "object"])

    def test_request_fingerprint_is_portable_between_executor_worktrees(self) -> None:
        with tempfile.TemporaryDirectory() as left_raw, tempfile.TemporaryDirectory() as right_raw:
            left = self.request(Path(left_raw).resolve())
            right = self.request(Path(right_raw).resolve())
            self.assertEqual(request_fingerprint(left), request_fingerprint(right))
            self.assertNotIn("worktree", portable_request_payload(left))
            changed = self.request(
                Path(right_raw).resolve(), instruction="A materially different task instruction."
            )
            self.assertNotEqual(request_fingerprint(left), request_fingerprint(changed))

    def test_factory_lease_roundtrip_trust_activity_and_serialization(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            request = self.request(Path(raw).resolve())
            lease = self.lease(request)
            lease.validate()
            self.assertTrue(lease.trusted)
            self.assertTrue(lease.active_at(NOW))
            self.assertFalse(lease.active_at(NOW - timedelta(hours=1)))
            self.assertFalse(lease.active_at(NOW + timedelta(hours=1)))
            self.assertLess(lease.issued_time, lease.expiry_time)
            payload = lease.to_dict()
            self.assertEqual(payload["schema_version"], DURABLE_AGENT_SCHEMA_VERSION)
            self.assertEqual(FactoryLease.from_mapping(payload), lease)
            self.assertEqual(AUTOMATIC_DURABLE_PROVIDERS, {"antigravity", "opencode_ollama"})

    def test_factory_lease_rejects_invalid_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            request = self.request(Path(raw).resolve())
            valid = self.lease(request)
            cases = (
                ({"schema_version": 2}, "schema_version"),
                ({"lease_id": "bad lease"}, "lease_id"),
                ({"run_id": ""}, "run_id"),
                ({"task_id": ""}, "task_id"),
                ({"worker_id": "bad worker"}, "worker_id"),
                ({"issue_number": 0}, "positive"),
                ({"provider_id": "codex"}, "not eligible"),
                ({"repository": "invalid"}, "owner/name"),
                ({"working_branch": valid.integration_branch}, "distinct"),
                ({"request_sha256": "bad"}, "request_sha256"),
                ({"manifest_sha256": "bad"}, "manifest_sha256"),
                ({"issued_at": "invalid"}, "issued_at"),
                ({"expires_at": "2026-08-27T12:00:00"}, "timezone"),
                ({"expires_at": (valid.issued_time + timedelta(seconds=30)).isoformat()}, "TTL"),
                ({"expires_at": (valid.issued_time + timedelta(hours=7)).isoformat()}, "TTL"),
                ({"actor": ""}, "actor"),
            )
            for overrides, message in cases:
                with self.subTest(overrides=overrides), self.assertRaisesRegex(ValueError, message):
                    replace(valid, **overrides).validate()
            with self.assertRaisesRegex(ValueError, "JSON object"):
                FactoryLease.from_mapping([])
            with self.assertRaises(ValueError):
                FactoryLease.from_mapping({})

    def test_heartbeat_is_bounded_redacted_and_machine_readable(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            request = self.request(Path(raw).resolve())
            lease = self.lease(request)
            heartbeat = LeaseHeartbeat.from_lease(
                lease,
                phase="running",
                head_sha=SHA_A,
                detail="token=secret-value",
                metrics={"seconds": 12, "progress": 0.5},
                observed_at=NOW.isoformat(),
            )
            payload = heartbeat.to_dict()
            self.assertEqual(payload["phase"], "running")
            self.assertNotIn("secret-value", payload["detail"])
            self.assertEqual(payload["head_sha"], SHA_A)

            cases = (
                ({"schema_version": 2}, "schema_version"),
                ({"lease_id": "bad lease"}, "lease_id"),
                ({"run_id": ""}, "run_id"),
                ({"task_id": ""}, "task_id"),
                ({"worker_id": "bad worker"}, "worker_id"),
                ({"provider_id": "codex"}, "provider"),
                ({"phase": "unknown"}, "phase"),
                ({"observed_at": "invalid"}, "observed_at"),
                ({"head_sha": "bad"}, "head_sha"),
                ({"metrics": {"bad": "value"}}, "numeric"),
            )
            for overrides, message in cases:
                with self.subTest(overrides=overrides), self.assertRaisesRegex(ValueError, message):
                    replace(heartbeat, **overrides).validate()

    def test_provider_result_from_success_and_failure_execution(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            request = self.request(Path(raw).resolve())
            lease = self.lease(request)
            evidence = DurableEvidence(
                branch=request.working_branch,
                commit_sha=SHA_A,
                changed_paths=("docs/worker-a/result.md",),
                pushed=True,
                start_sha=SHA_B,
            )
            execution = ProviderExecutionResult(
                output=ProviderRunOutput(
                    "antigravity",
                    "success",
                    response="done",
                    session_id="secret=session",
                ),
                evidence=evidence,
                telemetry=(),
            )
            result = DurableProviderResult.from_execution(
                lease, execution, observed_at=NOW.isoformat()
            )
            self.assertEqual(result.remote_sha, SHA_A)
            self.assertTrue(result.pushed)
            payload = result.to_dict()
            self.assertNotIn("session", payload["session_id"])

            failed_execution = ProviderExecutionResult(
                output=ProviderRunOutput(
                    "antigravity", "failed", error="password=bad"
                ),
                evidence=None,
                telemetry=(),
            )
            failed = DurableProviderResult.from_execution(
                lease, failed_execution, observed_at=NOW.isoformat()
            )
            self.assertEqual(failed.status, "failed")
            self.assertEqual(failed.branch, "")
            self.assertNotIn("bad", failed.to_dict()["error"])

    def test_provider_result_validation_rejects_invalid_shapes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            request = self.request(Path(raw).resolve())
            lease = self.lease(request)
            valid = DurableProviderResult(
                lease_id=lease.lease_id,
                run_id=lease.run_id,
                task_id=lease.task_id,
                issue_number=lease.issue_number,
                provider_id=lease.provider_id,
                worker_id=lease.worker_id,
                status="success",
                branch=lease.working_branch,
                commit_sha=SHA_A,
                remote_sha=SHA_A,
                changed_paths=("docs/worker-a/result.md",),
                pushed=True,
                request_sha256=lease.request_sha256,
                manifest_sha256=lease.manifest_sha256,
                observed_at=NOW.isoformat(),
            )
            valid.validate()
            cases = (
                ({"schema_version": 2}, "schema_version"),
                ({"lease_id": "bad lease"}, "lease_id"),
                ({"run_id": ""}, "run_id"),
                ({"task_id": ""}, "task_id"),
                ({"worker_id": "bad worker"}, "worker_id"),
                ({"issue_number": 0}, "positive"),
                ({"provider_id": "codex"}, "provider"),
                ({"status": "unknown"}, "status"),
                ({"request_sha256": "bad"}, "request_sha256"),
                ({"manifest_sha256": "bad"}, "manifest_sha256"),
                ({"observed_at": "invalid"}, "observed_at"),
                ({"branch": "bad branch"}, "branch"),
                ({"commit_sha": "bad"}, "commit_sha"),
                ({"remote_sha": "bad"}, "remote_sha"),
                ({"changed_paths": ()}, "changed_paths"),
            )
            for overrides, message in cases:
                with self.subTest(overrides=overrides), self.assertRaisesRegex(ValueError, message):
                    replace(valid, **overrides).validate()

    def test_lease_binding_and_assertion_fail_closed_on_every_identity(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            request = self.request(Path(raw).resolve())
            manifest = self.manifest()
            lease = self.lease(request, manifest)
            self.assertEqual(
                lease_binding_reasons(
                    lease,
                    request,
                    manifest,
                    worker_id=lease.worker_id,
                    when=NOW,
                ),
                (),
            )
            self.assertIs(
                assert_lease_authorizes(
                    lease,
                    request,
                    manifest,
                    worker_id=lease.worker_id,
                    when=NOW,
                ),
                lease,
            )

            mismatches = (
                {"run_id": "other-run"},
                {"task_id": "other-task"},
                {"repository": "other/repo"},
                {"working_branch": "factory/durable-run/other"},
                {"integration_branch": "factory/other-run"},
                {"target_branch": "develop"},
                {"worker_id": "executor-02"},
                {"request_sha256": "c" * 64},
                {"manifest_sha256": "d" * 64},
            )
            for overrides in mismatches:
                candidate = replace(lease, **overrides)
                with self.subTest(overrides=overrides):
                    reasons = lease_binding_reasons(
                        candidate,
                        request,
                        manifest,
                        worker_id=lease.worker_id,
                        when=NOW,
                    )
                    self.assertTrue(reasons)
            untrusted = replace(lease, actor="local-user")
            self.assertIn(
                "github-actions[bot]",
                " ".join(
                    lease_binding_reasons(
                        untrusted,
                        request,
                        manifest,
                        worker_id=lease.worker_id,
                        when=NOW,
                    )
                ),
            )
            expired = replace(
                lease,
                issued_at=(NOW - timedelta(hours=2)).isoformat(),
                expires_at=(NOW - timedelta(hours=1)).isoformat(),
            )
            self.assertIn(
                "not active",
                " ".join(
                    lease_binding_reasons(
                        expired,
                        request,
                        manifest,
                        worker_id=lease.worker_id,
                        when=NOW,
                    )
                ),
            )
            with self.assertRaises(ValueError):
                assert_lease_authorizes(
                    untrusted,
                    request,
                    manifest,
                    worker_id=lease.worker_id,
                    when=NOW,
                )
            invalid_request = ProviderTaskRequest(
                run_id=request.run_id,
                task_id=request.task_id,
                repository=request.repository,
                worktree=Path("relative"),
                integration_branch=request.integration_branch,
                target_branch=request.target_branch,
                working_branch=request.working_branch,
                paths=request.paths,
                instruction=request.instruction,
            )
            self.assertTrue(
                lease_binding_reasons(
                    lease,
                    invalid_request,
                    manifest,
                    worker_id=lease.worker_id,
                    when=NOW,
                )
            )

    def successful_result(self, lease: FactoryLease, **overrides) -> DurableProviderResult:
        value = DurableProviderResult(
            lease_id=lease.lease_id,
            run_id=lease.run_id,
            task_id=lease.task_id,
            issue_number=lease.issue_number,
            provider_id=lease.provider_id,
            worker_id=lease.worker_id,
            status="success",
            branch=lease.working_branch,
            commit_sha=SHA_A,
            remote_sha=SHA_A,
            changed_paths=("docs/worker-a/result.md",),
            pushed=True,
            request_sha256=lease.request_sha256,
            manifest_sha256=lease.manifest_sha256,
            observed_at=NOW.isoformat(),
        )
        return replace(value, **overrides)

    def test_result_evaluation_accepts_only_exact_durable_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            request = self.request(Path(raw).resolve())
            manifest = self.manifest()
            lease = self.lease(request, manifest)
            valid = evaluate_result(lease, self.successful_result(lease), request, manifest)
            self.assertTrue(valid.accepted)
            self.assertTrue(valid.completed)
            self.assertIn("ready", " ".join(valid.reasons))
            self.assertTrue(ResultDecision(True, True, ("ok",)).to_dict()["completed"])

            failed = self.successful_result(
                lease,
                status="failed",
                branch="",
                commit_sha="",
                remote_sha="",
                changed_paths=(),
                pushed=False,
                error="provider failed",
            )
            failed_decision = evaluate_result(lease, failed, request, manifest)
            self.assertTrue(failed_decision.accepted)
            self.assertFalse(failed_decision.completed)
            self.assertIn("failure", " ".join(failed_decision.reasons))

            mismatches = (
                ({"lease_id": "other-lease"}, "lease_id"),
                ({"run_id": "other-run"}, "run_id"),
                ({"task_id": "other-task"}, "task_id"),
                ({"issue_number": 999}, "issue_number"),
                ({"provider_id": "opencode_ollama"}, "provider_id"),
                ({"request_sha256": "c" * 64}, "request_sha256"),
                ({"manifest_sha256": "d" * 64}, "manifest_sha256"),
                ({"branch": "factory/durable-run/other"}, "branch"),
                ({"pushed": False}, "not pushed"),
                ({"remote_sha": SHA_B}, "remote SHA"),
                ({"changed_paths": ("src/escape.py",)}, "outside declared scope"),
                ({"changed_paths": (".github/workflows/escape.yml",)}, "protected path"),
            )
            for overrides, message in mismatches:
                with self.subTest(overrides=overrides):
                    decision = evaluate_result(
                        lease,
                        self.successful_result(lease, **overrides),
                        request,
                        manifest,
                    )
                    self.assertFalse(decision.accepted)
                    self.assertIn(message, " ".join(decision.reasons))

            invalid = self.successful_result(lease, commit_sha="bad")
            invalid_decision = evaluate_result(lease, invalid, request, manifest)
            self.assertFalse(invalid_decision.accepted)
            self.assertIn("commit_sha", " ".join(invalid_decision.reasons))

    def test_recovery_selects_one_active_trusted_lease_and_allows_takeover_after_expiry(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            request = self.request(Path(raw).resolve())
            manifest = self.manifest()
            active = self.lease(request, manifest)
            expired = replace(
                active,
                lease_id="lease-expired",
                issued_at=(NOW - timedelta(hours=2)).isoformat(),
                expires_at=(NOW - timedelta(hours=1)).isoformat(),
            )
            untrusted = replace(active, lease_id="lease-untrusted", actor="local-user")
            mismatch = replace(active, lease_id="lease-other", task_id="other-task")
            selected = select_recoverable_lease(
                [expired, untrusted, mismatch, active],
                request,
                manifest,
                worker_id=active.worker_id,
                when=NOW,
            )
            self.assertEqual(selected, active)
            self.assertIsNone(
                select_recoverable_lease(
                    [expired, untrusted, mismatch],
                    request,
                    manifest,
                    worker_id=active.worker_id,
                    when=NOW,
                )
            )
            with self.assertRaisesRegex(ValueError, "multiple active"):
                select_recoverable_lease(
                    [active, replace(active, lease_id="lease-002")],
                    request,
                    manifest,
                    worker_id=active.worker_id,
                    when=NOW,
                )

    def test_markers_roundtrip_reject_malformed_payloads_and_never_emit_secrets(self) -> None:
        payload = {"lease_id": "lease-001", "detail": "token=secret-value"}
        marker = encode_marker("lease", payload)
        self.assertIn("FACTORY_PROVIDER_LEASE", marker)
        self.assertNotIn("secret-value", marker)
        decoded = decode_marker(f"prefix\n{marker}\nsuffix", "lease")
        self.assertEqual(decoded["lease_id"], "lease-001")
        self.assertIsNone(decode_marker("no marker", "lease"))
        for kind in ("", "bad kind"):
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, "marker kind"):
                encode_marker(kind, {})
            with self.assertRaisesRegex(ValueError, "marker kind"):
                decode_marker("", kind)
        with self.assertRaisesRegex(ValueError, "terminator"):
            encode_marker("result", {"detail": "-->"})
        with self.assertRaisesRegex(ValueError, "marker JSON"):
            decode_marker("<!-- FACTORY_PROVIDER_RESULT {bad} -->", "result")

    def test_new_lease_times_are_utc_bounded_and_deterministic(self) -> None:
        issued, expires = new_lease_times(issued_at=NOW, ttl_seconds=600)
        self.assertEqual(parse_timestamp(issued, label="issued"), NOW)
        self.assertEqual(
            parse_timestamp(expires, label="expires"), NOW + timedelta(minutes=10)
        )
        with self.assertRaisesRegex(ValueError, "ttl_seconds"):
            new_lease_times(issued_at=NOW, ttl_seconds=30)


if __name__ == "__main__":
    unittest.main()
