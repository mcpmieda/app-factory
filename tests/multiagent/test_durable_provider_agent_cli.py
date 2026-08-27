from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import scripts.durable_provider_agent as cli
from engine.durable_provider_agent import (
    TRUSTED_CONTROL_ACTOR,
    FactoryLease,
    manifest_fingerprint,
    request_fingerprint,
)
from engine.provider_runtime import (
    DurableEvidence,
    ProviderExecutionResult,
    ProviderRunOutput,
    ProviderTaskRequest,
)

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts" / "durable_provider_agent.py"
SHA = "a" * 40


class DurableProviderAgentCliTests(unittest.TestCase):
    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=ROOT,
            check=check,
            capture_output=True,
            text=True,
            timeout=60,
        )

    @staticmethod
    def request_mapping(worktree: Path) -> dict[str, object]:
        return {
            "run_id": "durable-cli",
            "task_id": "worker-a",
            "repository": "owner/repo",
            "worktree": str(worktree),
            "integration_branch": "factory/durable-cli",
            "target_branch": "main",
            "working_branch": "factory/durable-cli/worker-a",
            "paths": ["docs/worker-a"],
            "instruction": "SENSITIVE DURABLE TASK INSTRUCTION",
            "allowed_commands": ["python -m unittest*"],
            "timeout_seconds": 600,
            "remote": "origin",
        }

    @staticmethod
    def manifest_mapping() -> dict[str, object]:
        return {
            "schema_version": 1,
            "run_id": "durable-cli",
            "goal": "Test the durable provider CLI.",
            "max_parallel": 1,
            "tasks": [{"id": "worker-a", "paths": ["docs/worker-a"]}],
        }

    def write_contract(self, root: Path, *, actor: str = TRUSTED_CONTROL_ACTOR):
        root.mkdir(parents=True, exist_ok=True)
        worktree = root / "worktree"
        profile = root / "profile"
        worktree.mkdir()
        profile.mkdir()
        request_raw = self.request_mapping(worktree.resolve())
        manifest_raw = self.manifest_mapping()
        request = ProviderTaskRequest.from_mapping(request_raw)
        now = datetime.now(timezone.utc).replace(microsecond=0)
        lease = FactoryLease(
            lease_id="lease-cli-001",
            run_id=request.run_id,
            task_id=request.task_id,
            issue_number=123,
            provider_id="antigravity",
            worker_id="executor-cli-01",
            repository=request.repository,
            working_branch=request.working_branch,
            integration_branch=request.integration_branch,
            target_branch=request.target_branch,
            request_sha256=request_fingerprint(request),
            manifest_sha256=manifest_fingerprint(manifest_raw),
            issued_at=(now - timedelta(minutes=5)).isoformat(),
            expires_at=(now + timedelta(minutes=25)).isoformat(),
            actor=actor,
        )
        paths = {
            "spec": root / "request.json",
            "manifest": root / "manifest.json",
            "lease": root / "lease.json",
            "profile": profile,
        }
        paths["spec"].write_text(json.dumps(request_raw), encoding="utf-8")
        paths["manifest"].write_text(json.dumps(manifest_raw), encoding="utf-8")
        paths["lease"].write_text(json.dumps(lease.to_dict()), encoding="utf-8")
        return paths, request, lease

    def test_fingerprint_is_portable_machine_readable_and_does_not_leak_instruction(self) -> None:
        with tempfile.TemporaryDirectory(prefix="durable-cli-fingerprint-") as raw:
            paths, _, _ = self.write_contract(Path(raw))
            result = self.run_cli("fingerprint", str(paths["spec"]), str(paths["manifest"]))
            payload = json.loads(result.stdout)
        self.assertEqual(len(payload["request_sha256"]), 64)
        self.assertEqual(len(payload["manifest_sha256"]), 64)
        self.assertNotIn("SENSITIVE DURABLE TASK INSTRUCTION", result.stdout)
        self.assertNotIn("worktree", payload)

    def test_validate_accepts_only_the_exact_active_trusted_lease(self) -> None:
        with tempfile.TemporaryDirectory(prefix="durable-cli-validate-") as raw:
            root = Path(raw)
            paths, _, lease = self.write_contract(root)
            valid = self.run_cli(
                "validate",
                str(paths["spec"]),
                str(paths["manifest"]),
                str(paths["lease"]),
                "--worker-id",
                lease.worker_id,
            )
            payload = json.loads(valid.stdout)
            self.assertTrue(payload["authorized"])
            self.assertEqual(payload["authority"], "github-control-plane")

            wrong_worker = self.run_cli(
                "validate",
                str(paths["spec"]),
                str(paths["manifest"]),
                str(paths["lease"]),
                "--worker-id",
                "executor-other",
                check=False,
            )
            self.assertEqual(wrong_worker.returncode, 1)
            self.assertIn("worker_id", json.loads(wrong_worker.stdout)["error"])

            untrusted_paths, _, untrusted = self.write_contract(
                root / "untrusted", actor="local-user"
            )
            untrusted_result = self.run_cli(
                "validate",
                str(untrusted_paths["spec"]),
                str(untrusted_paths["manifest"]),
                str(untrusted_paths["lease"]),
                "--worker-id",
                untrusted.worker_id,
                check=False,
            )
            self.assertEqual(untrusted_result.returncode, 1)
            self.assertIn("github-actions[bot]", untrusted_result.stdout)

    def test_heartbeat_is_sanitized_numeric_and_pending_control_plane_validation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="durable-cli-heartbeat-") as raw:
            paths, _, _ = self.write_contract(Path(raw))
            result = self.run_cli(
                "heartbeat",
                str(paths["lease"]),
                "--phase",
                "running",
                "--head-sha",
                SHA,
                "--detail",
                "token=secret-value",
                "--metric",
                "elapsed=12",
                "--metric",
                "progress=0.5",
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["candidate"], "heartbeat")
            self.assertEqual(payload["heartbeat"]["metrics"]["elapsed"], 12)
            self.assertEqual(payload["heartbeat"]["metrics"]["progress"], 0.5)
            self.assertNotIn("secret-value", result.stdout)
            self.assertIn("pending-github-control-plane", payload["authority"])

            bad_metric = self.run_cli(
                "heartbeat",
                str(paths["lease"]),
                "--phase",
                "running",
                "--metric",
                "elapsed=not-a-number",
                check=False,
            )
            self.assertEqual(bad_metric.returncode, 1)
            self.assertIn("numeric", bad_metric.stdout)

    def test_run_refuses_local_only_completion_before_provider_execution(self) -> None:
        with tempfile.TemporaryDirectory(prefix="durable-cli-publish-") as raw:
            paths, _, lease = self.write_contract(Path(raw))
            result = self.run_cli(
                "run",
                str(paths["spec"]),
                str(paths["manifest"]),
                str(paths["lease"]),
                "--worker-id",
                lease.worker_id,
                "--profile-home",
                str(paths["profile"]),
                check=False,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires --publish", json.loads(result.stdout)["error"])

    def call_main(self, arguments: list[str]) -> tuple[int, dict[str, object]]:
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = cli.main(arguments)
        return code, json.loads(stream.getvalue())

    def test_run_emits_a_complete_candidate_only_after_validated_remote_evidence(self) -> None:
        with tempfile.TemporaryDirectory(prefix="durable-cli-run-") as raw:
            paths, request, lease = self.write_contract(Path(raw))
            evidence = DurableEvidence(
                branch=request.working_branch,
                commit_sha=SHA,
                changed_paths=("docs/worker-a/result.md",),
                pushed=True,
                start_sha="b" * 40,
            )
            execution = ProviderExecutionResult(
                output=ProviderRunOutput("antigravity", "success", response="done"),
                evidence=evidence,
                telemetry=(),
            )
            arguments = [
                "run",
                str(paths["spec"]),
                str(paths["manifest"]),
                str(paths["lease"]),
                "--worker-id",
                lease.worker_id,
                "--publish",
                "--profile-home",
                str(paths["profile"]),
            ]
            with patch.object(
                cli, "build_adapter", return_value=SimpleNamespace(provider_id="antigravity")
            ), patch.object(cli, "execute_provider_task", return_value=execution):
                code, payload = self.call_main(arguments)
        self.assertEqual(code, 0)
        self.assertEqual(payload["candidate"], "provider-result")
        self.assertTrue(payload["decision"]["accepted"])
        self.assertTrue(payload["decision"]["completed"])
        self.assertEqual(payload["result"]["remote_sha"], SHA)
        self.assertIn("pending-github-control-plane", payload["authority"])

    def test_run_returns_two_for_a_bound_terminal_provider_failure(self) -> None:
        with tempfile.TemporaryDirectory(prefix="durable-cli-failure-") as raw:
            paths, _, lease = self.write_contract(Path(raw))
            execution = ProviderExecutionResult(
                output=ProviderRunOutput(
                    "antigravity", "failed", error="password=provider-secret"
                ),
                evidence=None,
                telemetry=(),
            )
            arguments = [
                "run",
                str(paths["spec"]),
                str(paths["manifest"]),
                str(paths["lease"]),
                "--worker-id",
                lease.worker_id,
                "--publish",
                "--profile-home",
                str(paths["profile"]),
            ]
            with patch.object(
                cli, "build_adapter", return_value=SimpleNamespace(provider_id="antigravity")
            ), patch.object(cli, "execute_provider_task", return_value=execution):
                code, payload = self.call_main(arguments)
        self.assertEqual(code, 2)
        self.assertTrue(payload["decision"]["accepted"])
        self.assertFalse(payload["decision"]["completed"])
        self.assertNotIn("provider-secret", json.dumps(payload))

    def test_run_fails_closed_when_adapter_does_not_match_lease(self) -> None:
        with tempfile.TemporaryDirectory(prefix="durable-cli-adapter-") as raw:
            paths, _, lease = self.write_contract(Path(raw))
            arguments = [
                "run",
                str(paths["spec"]),
                str(paths["manifest"]),
                str(paths["lease"]),
                "--worker-id",
                lease.worker_id,
                "--publish",
                "--profile-home",
                str(paths["profile"]),
            ]
            with patch.object(
                cli,
                "build_adapter",
                return_value=SimpleNamespace(provider_id="opencode_ollama"),
            ):
                code, payload = self.call_main(arguments)
        self.assertEqual(code, 1)
        self.assertIn("does not match", payload["error"])


if __name__ == "__main__":
    unittest.main()
