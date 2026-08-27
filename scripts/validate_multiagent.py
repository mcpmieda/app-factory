#!/usr/bin/env python3
"""Executable gate for provider-neutral multiagent execution."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.merge_train import (  # noqa: E402
    FinalPullRequestCandidate,
    WorkerMergeCandidate,
    evaluate_final_gate,
    evaluate_worker_merge,
)
from engine.work_orchestrator import MAX_AUTOMATIC_PARALLEL  # noqa: E402

REQUIRED = [
    "engine/work_orchestrator.py",
    "engine/provider_runtime.py",
    "engine/providers/__init__.py",
    "engine/providers/antigravity.py",
    "engine/providers/opencode_ollama.py",
    "engine/merge_train.py",
    "scripts/factory_run.py",
    "scripts/provider_worker.py",
    "core/MULTIAGENT_EXECUTION.md",
    "core/PROVIDER_RUNTIME.md",
    "core/MERGE_TRAIN.md",
    "docs/MULTIAGENT_IMPLEMENTATION_STATUS.md",
    "docs/JULES_API_FIRST_PILOT_EVIDENCE.md",
    "tests/multiagent/test_work_orchestrator.py",
    "tests/multiagent/test_factory_run_cli.py",
    "tests/multiagent/test_parallel_guardrails.py",
    "tests/multiagent/test_provider_runtime.py",
    "tests/multiagent/test_provider_adapters.py",
    "tests/multiagent/test_provider_worker_cli.py",
    "tests/multiagent/test_merge_train.py",
]


def stop(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def run(
    *args: str,
    cwd: Path = ROOT,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
        timeout=180,
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
            "tasks": [
                {
                    "id": "implementation",
                    "title": "Implementation",
                    "paths": ["src/feature"],
                    "required_capabilities": [
                        "reasoning",
                        "repo_read",
                        "repo_write",
                    ],
                }
            ],
        }),
        encoding="utf-8",
    )
    return spec


def validate_zero_first_and_remote_fallback() -> None:
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
        local_payload = json.loads(local.stdout)
        if local_payload["waves"][0]["assignments"][0]["provider"] != "opencode_ollama":
            stop("zero-cost local provider was not preferred when explicitly available")

        remote = run(
            sys.executable,
            "scripts/factory_run.py",
            "plan",
            str(spec),
            "--providers",
            "jules,antigravity",
        )
        remote_payload = json.loads(remote.stdout)
        if remote_payload["waves"][0]["assignments"][0]["provider"] not in {
            "jules",
            "antigravity",
        }:
            stop("remote free-quota fallback was not selected")

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
        keys = set(payload["invocation"]["environment_keys"])
        required_keys = {
            "HOME",
            "OPENCODE_CONFIG_CONTENT",
            "OPENCODE_PERMISSION",
            "OPENCODE_CONFIG_DIR",
        }
        if not required_keys.issubset(keys):
            stop("OpenCode worker is missing isolated profile/config environment")
        argv = payload["invocation"]["argv"]
        if "--auto" not in argv or "--format" not in argv or "json" not in argv:
            stop("OpenCode invocation is not noninteractive and machine-readable")


def validate_codex_manual_only() -> None:
    providers = json.loads(
        run(sys.executable, "scripts/factory_run.py", "providers").stdout
    )
    codex = providers.get("codex") or {}
    if codex.get("automatic") is not False or codex.get("cost_class") != "metered":
        stop("Codex must remain a metered manual-only escalation provider")


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
    validate_zero_first_and_remote_fallback()
    validate_provider_command_is_redacted_and_bounded()
    validate_codex_manual_only()
    validate_merge_train_contract()
    print(
        "OK: multiagent graph, 1-3 parallelism, provider runtime isolation, "
        "durable branch evidence, merge train, and premium escalation guard validated."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
