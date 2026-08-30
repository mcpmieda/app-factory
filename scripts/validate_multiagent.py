#!/usr/bin/env python3
"""Executable gate for the finalized multiagent execution scope."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.durable_provider_agent import (  # noqa: E402
    TRUSTED_CONTROL_ACTOR,
    DurableProviderResult,
    FactoryLease,
    evaluate_result,
    manifest_fingerprint,
    request_fingerprint,
)
from engine.merge_train import (  # noqa: E402
    FinalPullRequestCandidate,
    WorkerMergeCandidate,
    evaluate_final_gate,
    evaluate_worker_merge,
)
from engine.provider_runtime import ProviderTaskRequest  # noqa: E402
from engine.work_orchestrator import MAX_AUTOMATIC_PARALLEL  # noqa: E402

REQUIRED = [
    "engine/work_orchestrator.py",
    "engine/provider_runtime.py",
    "engine/durable_provider_agent.py",
    "engine/providers/opencode_ollama.py",
    "engine/merge_train.py",
    "scripts/factory_run.py",
    "scripts/provider_worker.py",
    "scripts/durable_provider_agent.py",
    "core/MULTIAGENT_EXECUTION.md",
    "core/PROVIDER_RUNTIME.md",
    "core/DURABLE_PROVIDER_AGENT.md",
    "core/MERGE_TRAIN.md",
    "docs/MULTIAGENT_IMPLEMENTATION_STATUS.md",
    "docs/JULES_API_FIRST_PILOT_EVIDENCE.md",
    "tests/multiagent/test_work_orchestrator.py",
    "tests/multiagent/test_factory_run_cli.py",
    "tests/multiagent/test_parallel_guardrails.py",
    "tests/multiagent/test_provider_runtime.py",
    "tests/multiagent/test_provider_adapters.py",
    "tests/multiagent/test_provider_worker_cli.py",
    "tests/multiagent/test_durable_provider_agent.py",
    "tests/multiagent/test_durable_provider_agent_cli.py",
    "tests/multiagent/test_merge_train.py",
]


def stop(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def run(*args: str, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=cwd, check=check, capture_output=True, text=True, timeout=180
    )


def validate_files() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        stop("Multiagent required files missing: " + ", ".join(missing))


def validate_unit_tests() -> None:
    result = run(
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests/multiagent",
        "-v",
        check=False,
    )
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        stop("Multiagent unit tests failed")


def write_plan_spec(directory: Path) -> Path:
    spec = directory / "run.json"
    spec.write_text(
        json.dumps({
            "schema_version": 1,
            "run_id": "gate",
            "goal": "prove provider routing",
            "tasks": [{
                "id": "implementation",
                "title": "Implementation",
                "paths": ["src/feature"],
                "required_capabilities": ["reasoning", "repo_read", "repo_write"],
            }],
        }),
        encoding="utf-8",
    )
    return spec


def validate_finalized_provider_scope() -> None:
    with tempfile.TemporaryDirectory(prefix="app-factory-multiagent-") as raw:
        spec = write_plan_spec(Path(raw))
        local = run(
            sys.executable,
            "scripts/factory_run.py",
            "plan",
            str(spec),
            "--providers",
            "jules,opencode_ollama",
        )
        payload = json.loads(local.stdout)
        if payload["waves"][0]["assignments"][0]["provider"] != "opencode_ollama":
            stop("zero-cost OpenCode/Ollama provider was not preferred")

        remote = run(
            sys.executable,
            "scripts/factory_run.py",
            "plan",
            str(spec),
            "--providers",
            "jules",
        )
        remote_payload = json.loads(remote.stdout)
        if remote_payload["waves"][0]["assignments"][0]["provider"] != "jules":
            stop("Jules fallback was not selected")

        retired = run(
            sys.executable,
            "scripts/factory_run.py",
            "plan",
            str(spec),
            "--providers",
            "antigravity",
            check=False,
        )
        if retired.returncode == 0 or "Unsupported automatic provider" not in retired.stdout:
            stop("retired Antigravity provider was not rejected")

        excessive = run(
            sys.executable,
            "scripts/factory_run.py",
            "plan",
            str(spec),
            "--providers",
            "jules",
            "--max-parallel",
            str(MAX_AUTOMATIC_PARALLEL + 1),
            check=False,
        )
        if excessive.returncode == 0 or "between 1 and 3" not in excessive.stdout:
            stop("max_parallel ceiling 1-3 is not enforced")


def validate_provider_command_is_redacted_and_bounded() -> None:
    with tempfile.TemporaryDirectory(prefix="app-factory-provider-command-") as raw:
        root = Path(raw)
        worktree = root / "worktree"
        profile = root / "profile"
        worktree.mkdir()
        profile.mkdir()
        instruction = "DO NOT LEAK THIS TASK INSTRUCTION"
        request = root / "request.json"
        request.write_text(
            json.dumps({
                "run_id": "provider-gate",
                "task_id": "worker-a",
                "repository": "owner/repo",
                "worktree": str(worktree),
                "integration_branch": "factory/provider-gate",
                "target_branch": "main",
                "working_branch": "factory/provider-gate/worker-a",
                "paths": ["docs/worker-a"],
                "instruction": instruction,
                "allowed_commands": ["python -m unittest*"],
            }),
            encoding="utf-8",
        )
        result = run(
            sys.executable,
            "scripts/provider_worker.py",
            "command",
            "--provider",
            "opencode_ollama",
            "--model",
            "qwen3-coder",
            "--profile-home",
            str(profile),
            str(request),
        )
        payload = json.loads(result.stdout)
        rendered = json.dumps(payload)
        if instruction in rendered or "<task-instruction>" not in rendered:
            stop("provider command output leaks the task instruction")
        required_keys = {
            "HOME",
            "OPENCODE_CONFIG_CONTENT",
            "OPENCODE_PERMISSION",
            "OPENCODE_CONFIG_DIR",
        }
        if not required_keys.issubset(set(payload["invocation"]["environment_keys"])):
            stop("OpenCode worker is missing isolated profile/config environment")
        argv = payload["invocation"]["argv"]
        if "--auto" not in argv or "--format" not in argv or "json" not in argv:
            stop("OpenCode invocation is not noninteractive and machine-readable")


def validate_codex_manual_only() -> None:
    providers = json.loads(run(sys.executable, "scripts/factory_run.py", "providers").stdout)
    codex = providers.get("codex") or {}
    if codex.get("automatic") is not False or codex.get("cost_class") != "metered":
        stop("Codex must remain a metered manual-only escalation provider")
    if "antigravity" in providers:
        stop("retired Antigravity provider is still exposed by the finalized registry")


def validate_durable_agent_contract() -> None:
    with tempfile.TemporaryDirectory(prefix="app-factory-durable-agent-") as raw:
        root = Path(raw).resolve()
        request = ProviderTaskRequest.from_mapping({
            "run_id": "durable-gate",
            "task_id": "worker-a",
            "repository": "owner/repo",
            "worktree": str(root),
            "integration_branch": "factory/durable-gate",
            "target_branch": "main",
            "working_branch": "factory/durable-gate/worker-a",
            "paths": ["docs/worker-a"],
            "instruction": "Create durable evidence.",
        })
        manifest = {
            "schema_version": 1,
            "run_id": "durable-gate",
            "max_parallel": 1,
            "tasks": [{"id": "worker-a", "paths": ["docs/worker-a"]}],
        }
        now = datetime.now(timezone.utc).replace(microsecond=0)
        lease = FactoryLease(
            lease_id="durable-gate-lease",
            run_id=request.run_id,
            task_id=request.task_id,
            issue_number=1,
            provider_id="opencode_ollama",
            worker_id="executor-gate",
            repository=request.repository,
            working_branch=request.working_branch,
            integration_branch=request.integration_branch,
            target_branch=request.target_branch,
            request_sha256=request_fingerprint(request),
            manifest_sha256=manifest_fingerprint(manifest),
            issued_at=(now - timedelta(minutes=1)).isoformat(),
            expires_at=(now + timedelta(minutes=10)).isoformat(),
            actor=TRUSTED_CONTROL_ACTOR,
        )
        result = DurableProviderResult(
            lease_id=lease.lease_id,
            run_id=lease.run_id,
            task_id=lease.task_id,
            issue_number=lease.issue_number,
            provider_id=lease.provider_id,
            worker_id=lease.worker_id,
            status="success",
            branch=lease.working_branch,
            commit_sha="a" * 40,
            remote_sha="a" * 40,
            changed_paths=("docs/worker-a/result.md",),
            pushed=True,
            request_sha256=lease.request_sha256,
            manifest_sha256=lease.manifest_sha256,
            observed_at=now.isoformat(),
        )
        decision = evaluate_result(lease, result, request, manifest)
        if not decision.accepted or not decision.completed:
            stop("exact durable provider evidence was not accepted")


def validate_merge_train_contract() -> None:
    sha = "a" * 40
    worker = evaluate_worker_merge(
        WorkerMergeCandidate(
            task_id="worker-a",
            pull_request_number=1,
            base_branch="factory/gate",
            head_branch="factory/gate/worker-a",
            head_sha=sha,
            changed_paths=("docs/worker-a/result.md",),
            declared_paths=("docs/worker-a",),
            ci_event="workflow_dispatch",
            ci_head_sha=sha,
            ci_conclusion="success",
            review_conclusions={
                "CodeRabbit": "success",
                "Semgrep": "success",
                "Sonar": "success",
            },
            review_head_shas={
                "CodeRabbit": sha,
                "Semgrep": sha,
                "Sonar": sha,
            },
        ),
        integration_branch="factory/gate",
        target_branch="main",
    )
    if not worker.allowed or worker.destination_branch != "factory/gate":
        stop("green worker cannot enter the isolated integration branch")
    if worker.auto_merge_target:
        stop("worker merge train may never auto-merge the target branch")

    final = evaluate_final_gate(
        FinalPullRequestCandidate(
            head_branch="factory/gate",
            base_branch="main",
            draft=True,
            integration_head_sha=sha,
            integration_ci_event="workflow_dispatch",
            integration_ci_head_sha=sha,
            integration_ci_conclusion="success",
        ),
        integration_branch="factory/gate",
        target_branch="main",
    )
    if not final.ready_for_human_review or final.auto_merge_allowed:
        stop("final gate must be draft/human-only after exact integration CI")


def main() -> int:
    validate_files()
    validate_unit_tests()
    validate_finalized_provider_scope()
    validate_provider_command_is_redacted_and_bounded()
    validate_codex_manual_only()
    validate_durable_agent_contract()
    validate_merge_train_contract()
    print(
        "OK: finalized Jules + OpenCode/Ollama scope, 1-3 parallelism, provider runtime isolation, "
        "GitHub-backed durable leases/results, exact-SHA merge train, and manual premium escalation validated."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
