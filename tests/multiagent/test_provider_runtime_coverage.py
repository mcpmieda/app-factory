from __future__ import annotations

import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import engine.provider_runtime as runtime
from engine.provider_runtime import (
    CommandResult,
    DurableEvidence,
    GitClient,
    GitSecuritySnapshot,
    ProviderExecutionResult,
    ProviderHealth,
    ProviderInvocation,
    ProviderRunOutput,
    ProviderSelection,
    ProviderTaskRequest,
    SubprocessRunner,
    TelemetryEvent,
    _git_marker,
    _hash_file,
    _nul_paths,
    _parse_refs,
    _resolve_git_path,
    _snapshot_path,
    _status_paths,
    assert_git_security_unchanged,
    assert_only_worker_ref_changed,
    execute_provider_task,
    normalize_runtime_path,
    sanitize_value,
    select_runtime_provider,
    validate_allowed_commands,
    validate_branch_name,
    validate_changed_paths,
)
from engine.work_orchestrator import WorkItem

SHA_A = "a" * 40
SHA_B = "b" * 40


class QueueRunner:
    def __init__(self, *results: CommandResult) -> None:
        self.results = list(results)
        self.invocations: list[ProviderInvocation] = []

    def run(self, invocation: ProviderInvocation) -> CommandResult:
        self.invocations.append(invocation)
        if self.results:
            return self.results.pop(0)
        return CommandResult(0, "", "")


class DummyAdapter:
    provider_id = "dummy"

    def __init__(self, output: ProviderRunOutput | None = None) -> None:
        self.output = output or ProviderRunOutput("dummy", "success", response="done")

    def probe(self, runner):
        return ProviderHealth("dummy", "healthy", "ok")

    def build_invocation(self, request: ProviderTaskRequest) -> ProviderInvocation:
        return ProviderInvocation("dummy", ("dummy", "run"), request.worktree, 5)

    def parse_output(self, result: CommandResult) -> ProviderRunOutput:
        return self.output


class ScriptedGit:
    def __init__(self, text_values=None, run_values=None) -> None:
        self.text_values = list(text_values or [])
        self.run_values = list(run_values or [])
        self.calls: list[tuple[str, ...]] = []

    def text(self, worktree: Path, *args: str) -> str:
        self.calls.append(tuple(args))
        if not self.text_values:
            raise AssertionError(f"unexpected git.text call: {args}")
        value = self.text_values.pop(0)
        if isinstance(value, Exception):
            raise value
        return value

    def run(self, worktree: Path, *args: str, timeout_seconds: int = 120) -> CommandResult:
        self.calls.append(tuple(args))
        if not self.run_values:
            return CommandResult(0, "", "")
        value = self.run_values.pop(0)
        if isinstance(value, Exception):
            raise value
        return value


class CustomValue:
    def __str__(self) -> str:
        return "password=secret-value"


class ProviderRuntimeCoverageTests(unittest.TestCase):
    def request(self, worktree: Path, **overrides) -> ProviderTaskRequest:
        raw = {
            "run_id": "run",
            "task_id": "worker",
            "repository": "owner/repo",
            "worktree": str(worktree),
            "integration_branch": "factory/run",
            "target_branch": "main",
            "working_branch": "factory/run/worker",
            "paths": ["docs/worker"],
            "instruction": "Create the result.",
            "allowed_commands": ["python -m unittest*"],
            "timeout_seconds": 30,
            "remote": "origin",
        }
        raw.update(overrides)
        return ProviderTaskRequest.from_mapping(raw)

    def snapshot(self, worktree: Path, **overrides) -> GitSecuritySnapshot:
        value = GitSecuritySnapshot(
            top_level=worktree,
            git_marker="missing",
            git_dir=worktree / ".git",
            common_dir=worktree / ".git",
            sensitive_metadata={
                f"{label}:{relative}": "missing"
                for relative in runtime.SENSITIVE_GIT_PATHS
                for label in ("git", "common")
            },
            refs={f"refs/heads/factory/run/worker": SHA_A},
            remote_url="/tmp/remote.git",
        )
        return replace(value, **overrides)

    def test_sanitizers_cover_scalar_collections_and_custom_values(self) -> None:
        self.assertIsNone(sanitize_value(None))
        self.assertEqual(sanitize_value(3), 3)
        self.assertEqual(sanitize_value("token=abc"), "token=<redacted>")
        mapped = sanitize_value({"nested": ["api_key=abc", CustomValue()]})
        self.assertEqual(mapped["nested"][0], "api_key=<redacted>")
        self.assertIn("<redacted>", mapped["nested"][1])
        self.assertEqual(sanitize_value(("x",)), ["x"])

    def test_path_branch_and_command_validation_negative_edges(self) -> None:
        for value in ("/abs", "C:/abs", "", ".", "../escape", "a/../b"):
            with self.subTest(path=value), self.assertRaises(ValueError):
                normalize_runtime_path(value)
        for value in ("", "/bad", "-bad", "bad/", "bad.", "bad..x", "bad@{x", "bad//x", "bad space"):
            with self.subTest(branch=value), self.assertRaises(ValueError):
                validate_branch_name(value, label="branch")
        for value in ("*", "git status", "curl example", "npm test && echo bad", "python -c pass"):
            with self.subTest(command=value), self.assertRaises(ValueError):
                validate_allowed_commands([value])
        self.assertEqual(validate_allowed_commands(["", "npm test", "npm test"]), ("npm test",))

    def test_changed_paths_require_tracked_in_scope_output(self) -> None:
        with self.assertRaisesRegex(ValueError, "no tracked changes"):
            validate_changed_paths([], ["docs/a"])
        with self.assertRaisesRegex(ValueError, "outside declared scope"):
            validate_changed_paths(["src/a.py"], ["docs/a"])
        with self.assertRaisesRegex(ValueError, "protected path"):
            validate_changed_paths([".github/workflows/a.yml"], ["docs/a"])
        self.assertEqual(
            validate_changed_paths(["docs/a/x.md", "docs/a/x.md"], ["docs/a"]),
            ("docs/a/x.md",),
        )

    def test_health_selection_and_dataclass_serialization_edges(self) -> None:
        with self.assertRaises(ValueError):
            ProviderHealth("x", "bad", "reason")
        health = ProviderHealth("x", "degraded", "token=abc", details={"api_key": "abc"})
        self.assertTrue(health.usable)
        serialized = health.to_dict()
        self.assertIn("<redacted>", serialized["reason"])
        self.assertEqual(serialized["details"]["api_key"], "abc")
        self.assertFalse(ProviderHealth("x", "unknown", "no").usable)

        item = WorkItem(
            task_id="task",
            title="Task",
            role="implementation",
            paths=("docs/a",),
            required_capabilities=frozenset({"reasoning", "repo_read", "repo_write"}),
        )
        selection = select_runtime_provider(
            item,
            available_provider_ids=["opencode_ollama", "jules"],
            health={
                "opencode_ollama": ProviderHealth("opencode_ollama", "unavailable", "no"),
                "jules": ProviderHealth("jules", "degraded", "slow"),
            },
        )
        self.assertEqual(selection.provider_id, "jules")
        self.assertEqual(selection.to_dict()["status"], "selected")
        no_provider = select_runtime_provider(
            item,
            available_provider_ids=["jules"],
            health={"jules": ProviderHealth("jules", "unavailable", "down")},
        )
        self.assertIsNone(no_provider.provider_id)
        self.assertEqual(no_provider.status, "no-healthy-provider")
        self.assertEqual(ProviderSelection(None, "blocked", "why", ()).to_dict()["considered"], [])

    def test_request_validation_and_prompt_serialization_edges(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            request = self.request(root, allowed_commands=[])
            self.assertIn("none beyond built-in", request.worker_prompt())
            self.assertNotIn("instruction", request.to_dict())
            self.assertEqual(request.to_dict(include_instruction=True)["instruction"], "Create the result.")
            self.assertEqual(request.normalized_paths, ("docs/worker",))
            self.assertEqual(request.normalized_commands, ())

            cases = (
                ({"paths": "docs"}, "paths must be an array"),
                ({"allowed_commands": "npm test"}, "allowed_commands must be an array"),
                ({"run_id": ""}, "run_id"),
                ({"task_id": "x" * 121}, "task_id"),
                ({"repository": "invalid"}, "owner/name"),
                ({"instruction": ""}, "instruction"),
                ({"integration_branch": "main"}, "must differ from target"),
                ({"working_branch": "main"}, "worker branch must differ"),
                ({"timeout_seconds": 7201}, "timeout_seconds"),
                ({"remote": "bad/url"}, "remote"),
            )
            for overrides, message in cases:
                with self.subTest(overrides=overrides), self.assertRaisesRegex(ValueError, message):
                    self.request(root, **overrides)

    def test_invocation_subprocess_output_evidence_and_result_serialization(self) -> None:
        invocation = ProviderInvocation(
            "provider",
            ("tool", "secret", "--flag"),
            Path("/tmp"),
            10,
            env={"B": "2", "A": "1"},
            sensitive_argument_indexes=frozenset({1}),
        )
        self.assertEqual(invocation.display_argv(), ["tool", "<task-instruction>", "--flag"])
        self.assertEqual(invocation.to_dict()["environment_keys"], ["A", "B"])
        completed = SimpleNamespace(returncode=7, stdout="out", stderr="err")
        with patch.object(runtime.subprocess, "run", return_value=completed) as run_mock:
            result = SubprocessRunner().run(invocation)
        self.assertEqual(result.returncode, 7)
        self.assertFalse(run_mock.call_args.kwargs["shell"])
        self.assertEqual(run_mock.call_args.kwargs["env"]["GIT_TERMINAL_PROMPT"], "0")

        with self.assertRaises(ValueError):
            ProviderRunOutput("x", "unknown")
        output = ProviderRunOutput(
            "x", "failed", response="token=abc", session_id="secret=abc", usage={"api_key": "abc"}, error="password=abc"
        )
        payload = output.to_dict()
        self.assertNotIn("abc", payload["response"])
        self.assertNotIn("abc", payload["session_id"])
        self.assertNotIn("abc", payload["error"])

        incomplete = DurableEvidence("branch", "bad", (), False)
        self.assertFalse(incomplete.complete)
        self.assertFalse(incomplete.to_dict()["durable"])
        evidence = DurableEvidence("branch", SHA_A, ("docs/a.md",), True, start_sha=SHA_B, pull_request_url="url")
        self.assertTrue(evidence.complete)
        event = TelemetryEvent("run", "task", "x", "phase", "ok", "token=abc", metrics={"count": 1})
        self.assertIn("<redacted>", event.to_json_line())
        execution = ProviderExecutionResult(ProviderRunOutput("x", "success"), evidence, (event,))
        self.assertTrue(execution.completed)
        self.assertEqual(execution.to_dict()["evidence"]["commit_sha"], SHA_A)
        failed = ProviderExecutionResult(ProviderRunOutput("x", "failed"), None, ())
        self.assertFalse(failed.completed)
        self.assertIsNone(failed.to_dict()["evidence"])

    def test_git_client_and_filesystem_helpers_cover_error_and_marker_shapes(self) -> None:
        runner = QueueRunner(CommandResult(1, "", "password=bad"))
        with self.assertRaisesRegex(RuntimeError, "<redacted>"):
            GitClient(runner, Path("/tmp/hooks")).run(Path("/tmp"), "status")

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            missing = root / "missing"
            self.assertEqual(_snapshot_path(missing), "missing")
            file_path = root / "file.txt"
            file_path.write_text("x", encoding="utf-8")
            self.assertTrue(_hash_file(file_path))
            self.assertTrue(_snapshot_path(file_path).startswith("file:"))
            directory = root / "tree"
            (directory / "child").mkdir(parents=True)
            (directory / "child" / "a.txt").write_text("a", encoding="utf-8")
            self.assertTrue(_snapshot_path(directory).startswith("tree:"))
            link = root / "link"
            link.symlink_to(file_path)
            self.assertTrue(_hash_file(link))

            worktree = root / "worktree"
            worktree.mkdir()
            self.assertEqual(_git_marker(worktree), "missing")
            marker = worktree / ".git"
            marker.write_text("gitdir: ../real", encoding="utf-8")
            self.assertTrue(_git_marker(worktree).startswith("file:"))
            marker.unlink()
            marker.mkdir()
            self.assertTrue(_git_marker(worktree).startswith("directory:"))
            marker.rmdir()
            marker.symlink_to(file_path)
            self.assertTrue(_git_marker(worktree).startswith("symlink:"))
            self.assertEqual(_resolve_git_path(worktree, "../file.txt"), file_path.resolve())
            self.assertEqual(_resolve_git_path(worktree, str(file_path)), file_path.resolve())

    def test_ref_status_and_security_helpers_fail_closed(self) -> None:
        refs = _parse_refs(f"no-tab\nrefs/heads/a\tbad\nrefs/heads/b\t{SHA_A}\n")
        self.assertEqual(refs, {"refs/heads/b": SHA_A})
        self.assertEqual(_nul_paths("a\0\0b\0"), ("a", "b"))
        self.assertEqual(_status_paths(" M docs/a.md\0R  docs/new.md\0docs/old.md\0"), ("docs/a.md", "docs/new.md", "docs/old.md"))
        with self.assertRaisesRegex(ValueError, "parse provider worktree status"):
            _status_paths("x\0")
        with self.assertRaisesRegex(ValueError, "rename/copy"):
            _status_paths("R  docs/new.md\0")
        assert_only_worker_ref_changed({"refs/heads/worker": SHA_A}, {"refs/heads/worker": SHA_B}, "worker")
        with self.assertRaisesRegex(ValueError, "outside the worker branch"):
            assert_only_worker_ref_changed({"refs/heads/main": SHA_A}, {"refs/heads/main": SHA_B}, "worker")

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            request = self.request(root)
            snapshot = self.snapshot(root, git_marker="file:old")
            with self.assertRaisesRegex(ValueError, "Git control entry"):
                assert_git_security_unchanged(snapshot, request)
            snapshot = self.snapshot(root, sensitive_metadata={"x": "different"})
            with self.assertRaisesRegex(ValueError, "protected Git"):
                assert_git_security_unchanged(snapshot, request)

    def test_take_snapshot_rejects_wrong_root_and_empty_remote(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            request = self.request(root)
            wrong = ScriptedGit(text_values=[str(root / "other")])
            with self.assertRaisesRegex(ValueError, "repository root"):
                runtime.take_git_security_snapshot(wrong, request)

            git_dir = root / ".git"
            git_dir.mkdir()
            values = [str(root), ".git", ".git", "", ""]
            empty_remote = ScriptedGit(text_values=values)
            with self.assertRaisesRegex(ValueError, "no URL"):
                runtime.take_git_security_snapshot(empty_remote, request)

    def test_execute_preconditions_and_provider_failure(self) -> None:
        missing = Path("/tmp/definitely-missing-app-factory-worktree")
        with self.assertRaisesRegex(ValueError, "does not exist"):
            execute_provider_task(DummyAdapter(), self.request(missing), runner=QueueRunner())

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            request = self.request(root)
            cases = (
                (["wrong"], "branch mismatch"),
                ([request.working_branch, "?? dirty\0"], "must be clean"),
                ([request.working_branch, "", "bad-sha"], "starting commit SHA"),
            )
            for values, message in cases:
                with self.subTest(message=message), patch.object(runtime, "GitClient", return_value=ScriptedGit(values)):
                    with self.assertRaisesRegex(ValueError, message):
                        execute_provider_task(DummyAdapter(), request, runner=QueueRunner())

            git = ScriptedGit([request.working_branch, "", SHA_A])
            failed_adapter = DummyAdapter(ProviderRunOutput("dummy", "failed", error="boom"))
            with patch.object(runtime, "GitClient", return_value=git), patch.object(
                runtime, "take_git_security_snapshot", return_value=self.snapshot(root)
            ):
                result = execute_provider_task(failed_adapter, request, runner=QueueRunner(CommandResult(1)))
            self.assertFalse(result.completed)
            self.assertEqual(len(result.telemetry), 2)

    def test_execute_rejects_branch_history_merge_and_remote_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            request = self.request(root)
            security = self.snapshot(root)

            scenarios = [
                (
                    ScriptedGit([request.working_branch, "", SHA_A, "wrong"]),
                    QueueRunner(CommandResult(0)),
                    "changed the active branch",
                ),
                (
                    ScriptedGit([request.working_branch, "", SHA_A, request.working_branch, SHA_A]),
                    QueueRunner(CommandResult(0), CommandResult(1)),
                    "rewrote or detached",
                ),
                (
                    ScriptedGit([request.working_branch, "", SHA_A, request.working_branch, SHA_A, SHA_B]),
                    QueueRunner(CommandResult(0), CommandResult(0)),
                    "merge commits",
                ),
                (
                    ScriptedGit([
                        request.working_branch, "", SHA_A, request.working_branch, SHA_A, "",
                        f"refs/heads/{request.working_branch}\t{SHA_A}", "https://evil.example/repo.git"
                    ]),
                    QueueRunner(CommandResult(0), CommandResult(0)),
                    "configured Git remote",
                ),
            ]
            for git, runner, message in scenarios:
                with self.subTest(message=message), patch.object(runtime, "GitClient", return_value=git), patch.object(
                    runtime, "take_git_security_snapshot", return_value=security
                ), patch.object(runtime, "assert_git_security_unchanged"):
                    with self.assertRaisesRegex(ValueError, message):
                        execute_provider_task(DummyAdapter(), request, runner=runner)

    def test_execute_rejects_dirty_after_commit_and_wrong_remote_sha(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            request = self.request(root)
            security = self.snapshot(root)

            dirty_git = ScriptedGit(
                text_values=[
                    request.working_branch, "", SHA_A, request.working_branch, SHA_A, "",
                    f"refs/heads/{request.working_branch}\t{SHA_A}", security.remote_url,
                    "?? docs/worker/result.md\0", SHA_B, "?? docs/worker/late.md\0",
                ],
                run_values=[
                    CommandResult(0, "", ""),
                    CommandResult(0, "docs/worker/result.md\0", ""),
                    CommandResult(0, "", ""),
                    CommandResult(0, "docs/worker/result.md\0", ""),
                ],
            )
            with patch.object(runtime, "GitClient", return_value=dirty_git), patch.object(
                runtime, "take_git_security_snapshot", return_value=security
            ), patch.object(runtime, "assert_git_security_unchanged"), patch.object(
                runtime, "assert_only_worker_ref_changed"
            ):
                with self.assertRaisesRegex(ValueError, "not clean after controlled commit"):
                    execute_provider_task(DummyAdapter(), request, runner=QueueRunner(CommandResult(0), CommandResult(0)))

            wrong_sha_git = ScriptedGit(
                text_values=[
                    request.working_branch, "", SHA_A, request.working_branch, SHA_A, "",
                    f"refs/heads/{request.working_branch}\t{SHA_A}", security.remote_url,
                    "?? docs/worker/result.md\0", SHA_B, "",
                    f"refs/heads/{request.working_branch}\t{SHA_B}",
                    f"{SHA_A}\trefs/heads/{request.working_branch}",
                ],
                run_values=[
                    CommandResult(0, "", ""),
                    CommandResult(0, "docs/worker/result.md\0", ""),
                    CommandResult(0, "", ""),
                    CommandResult(0, "docs/worker/result.md\0", ""),
                    CommandResult(0, "", ""),
                ],
            )
            with patch.object(runtime, "GitClient", return_value=wrong_sha_git), patch.object(
                runtime, "take_git_security_snapshot", return_value=security
            ), patch.object(runtime, "assert_git_security_unchanged"), patch.object(
                runtime, "assert_only_worker_ref_changed"
            ):
                with self.assertRaisesRegex(ValueError, "does not match the validated commit SHA"):
                    execute_provider_task(DummyAdapter(), request, runner=QueueRunner(CommandResult(0), CommandResult(0)))


if __name__ == "__main__":
    unittest.main()
