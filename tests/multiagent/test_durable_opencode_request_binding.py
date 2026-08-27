from __future__ import annotations

import io
import json
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

SHA = "a" * 40


class DurableOpenCodeRequestBindingTests(unittest.TestCase):
    def test_run_builds_opencode_adapter_from_exact_leased_request(self) -> None:
        with tempfile.TemporaryDirectory(prefix="durable-opencode-request-") as raw:
            root = Path(raw)
            worktree = root / "worktree"
            profile = root / "profile"
            worktree.mkdir()
            profile.mkdir()
            request_raw = {
                "schema_version": 1,
                "run_id": "durable-opencode",
                "task_id": "worker-a",
                "repository": "owner/repo",
                "worktree": str(worktree.resolve()),
                "integration_branch": "factory/durable-opencode",
                "target_branch": "main",
                "working_branch": "factory/durable-opencode/worker-a",
                "paths": ["docs/worker-a"],
                "instruction": "Create the exact scoped evidence file.",
                "allowed_commands": [],
                "timeout_seconds": 600,
                "remote": "origin",
            }
            manifest = {
                "schema_version": 1,
                "run_id": "durable-opencode",
                "goal": "Prove request-bound durable OpenCode execution.",
                "max_parallel": 1,
                "tasks": [{"id": "worker-a", "paths": ["docs/worker-a"]}],
            }
            request = ProviderTaskRequest.from_mapping(request_raw)
            now = datetime.now(timezone.utc).replace(microsecond=0)
            lease = FactoryLease(
                lease_id="lease-opencode-001",
                run_id=request.run_id,
                task_id=request.task_id,
                issue_number=321,
                provider_id="opencode_ollama",
                worker_id="hosted-opencode-1",
                repository=request.repository,
                working_branch=request.working_branch,
                integration_branch=request.integration_branch,
                target_branch=request.target_branch,
                request_sha256=request_fingerprint(request),
                manifest_sha256=manifest_fingerprint(manifest),
                issued_at=(now - timedelta(minutes=1)).isoformat(),
                expires_at=(now + timedelta(minutes=20)).isoformat(),
                actor=TRUSTED_CONTROL_ACTOR,
            )
            spec_path = root / "request.json"
            manifest_path = root / "manifest.json"
            lease_path = root / "lease.json"
            spec_path.write_text(json.dumps(request_raw), encoding="utf-8")
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            lease_path.write_text(json.dumps(lease.to_dict()), encoding="utf-8")

            execution = ProviderExecutionResult(
                output=ProviderRunOutput("opencode_ollama", "success", response="done"),
                evidence=DurableEvidence(
                    branch=request.working_branch,
                    commit_sha=SHA,
                    changed_paths=("docs/worker-a/result.md",),
                    pushed=True,
                    start_sha="b" * 40,
                ),
                telemetry=(),
            )
            captured_request: ProviderTaskRequest | None = None

            def request_bound_adapter(args, actual_request):
                nonlocal captured_request
                captured_request = actual_request
                return SimpleNamespace(provider_id="opencode_ollama")

            stream = io.StringIO()
            with (
                patch.object(cli, "build_adapter", side_effect=request_bound_adapter),
                patch.object(cli, "execute_provider_task", return_value=execution),
                redirect_stdout(stream),
            ):
                code = cli.main(
                    [
                        "run",
                        str(spec_path),
                        str(manifest_path),
                        str(lease_path),
                        "--worker-id",
                        lease.worker_id,
                        "--publish",
                        "--model",
                        "qwen3:0.6b",
                        "--profile-home",
                        str(profile),
                    ]
                )

            payload = json.loads(stream.getvalue())
            self.assertEqual(code, 0)
            self.assertIsNotNone(captured_request)
            self.assertEqual(captured_request.task_id, request.task_id)
            self.assertEqual(captured_request.normalized_paths, request.normalized_paths)
            self.assertEqual(payload["candidate"], "provider-result")
            self.assertTrue(payload["decision"]["accepted"])


if __name__ == "__main__":
    unittest.main()
