from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from engine.provider_runtime import CommandResult, ProviderTaskRequest
from engine.providers.antigravity import AntigravityAdapter
from engine.providers.opencode_ollama import OpenCodeOllamaAdapter


class QueueRunner:
    def __init__(self, *results: CommandResult) -> None:
        self.results = list(results)
        self.invocations = []

    def run(self, invocation):
        self.invocations.append(invocation)
        return self.results.pop(0)


class ProviderAdapterTests(unittest.TestCase):
    def request(self, worktree: Path) -> ProviderTaskRequest:
        return ProviderTaskRequest.from_mapping({
            "run_id": "adapter-test",
            "task_id": "worker-a",
            "repository": "owner/repo",
            "worktree": str(worktree),
            "integration_branch": "factory/adapter-test",
            "target_branch": "main",
            "working_branch": "factory/adapter-test/worker-a",
            "paths": ["docs/worker-a"],
            "instruction": "Create the requested documentation and validate it.",
            "allowed_commands": ["python -m unittest*"],
        })

    def test_antigravity_uses_fixed_argv_json_and_never_skips_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            worktree = root / "worktree"
            profile = root / "profile"
            worktree.mkdir()
            profile.mkdir()
            request = self.request(worktree)
            invocation = AntigravityAdapter(
                model="gemini-test", effort="high", profile_home=profile
            ).build_invocation(request)
        self.assertEqual(invocation.argv[0], "agy")
        self.assertIn("-p", invocation.argv)
        self.assertIn("--output-format", invocation.argv)
        self.assertIn("json", invocation.argv)
        self.assertNotIn("--dangerously-skip-permissions", invocation.argv)
        self.assertIn("<task-instruction>", invocation.display_argv())
        self.assertNotIn(request.instruction, " ".join(invocation.display_argv()))
        self.assertEqual(invocation.env["HOME"], str(profile.resolve()))

    def test_antigravity_rejects_profile_inside_worktree(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            worktree = Path(raw)
            profile = worktree / ".provider-profile"
            profile.mkdir()
            with self.assertRaisesRegex(ValueError, "outside"):
                AntigravityAdapter(profile_home=profile).build_invocation(
                    self.request(worktree)
                )

    def test_antigravity_parses_machine_readable_success(self) -> None:
        output = AntigravityAdapter(profile_home=Path.cwd()).parse_output(CommandResult(
            0,
            json.dumps({
                "conversation_id": "conv-1",
                "status": "SUCCESS",
                "response": "done",
                "usage": {"total_tokens": 12},
            }),
            "",
        ))
        self.assertEqual(output.status, "success")
        self.assertEqual(output.session_id, "conv-1")

    def test_antigravity_probe_detects_installed_but_unauthenticated_cli(self) -> None:
        runner = QueueRunner(
            CommandResult(0, "agy 1.0", ""),
            CommandResult(1, "", "authentication required"),
        )
        with tempfile.TemporaryDirectory() as raw, patch(
            "engine.providers.antigravity.shutil.which", return_value="/bin/agy"
        ):
            health = AntigravityAdapter(profile_home=Path(raw)).probe(runner)
        self.assertEqual(health.status, "degraded")

    def test_opencode_permission_config_is_scope_bounded_and_denies_push(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            worktree = root / "worktree"
            profile = root / "profile"
            worktree.mkdir()
            profile.mkdir()
            request = self.request(worktree)
            adapter = OpenCodeOllamaAdapter(
                model="qwen3-coder", profile_home=profile
            )
            invocation = adapter.build_invocation(request)
            permissions = json.loads(invocation.env["OPENCODE_PERMISSION"])
            config = json.loads(invocation.env["OPENCODE_CONFIG_CONTENT"])
        self.assertEqual(invocation.argv[:3], ("opencode", "run", "--auto"))
        self.assertEqual(permissions["edit"]["*"], "deny")
        self.assertEqual(permissions["edit"]["docs/worker-a/**"], "allow")
        self.assertEqual(permissions["edit"][".github/**"], "deny")
        self.assertEqual(permissions["external_directory"], "deny")
        self.assertEqual(permissions["webfetch"], "deny")
        self.assertEqual(permissions["lsp"], "deny")
        self.assertEqual(permissions["bash"]["git push*"], "deny")
        self.assertEqual(permissions["bash"]["git commit*"], "deny")
        self.assertEqual(permissions["bash"]["python -m unittest*"], "allow")
        self.assertEqual(config["enabled_providers"], ["ollama"])
        self.assertEqual(config["mcp"], {})
        self.assertEqual(config["plugin"], [])
        self.assertTrue(config["tools"]["bash"])
        self.assertTrue(config["tools"]["read"])
        self.assertTrue(config["tools"]["edit"])
        self.assertTrue(config["tools"]["write"])
        self.assertFalse(config["tools"]["lsp"])
        self.assertFalse(config["tools"]["webfetch"])
        self.assertFalse(config["tools"]["websearch"])
        self.assertFalse(config["tools"]["task"])
        self.assertFalse(config["tools"]["skill"])
        self.assertFalse(config["tools"]["question"])
        self.assertEqual(invocation.env["HOME"], str(profile.resolve()))
        self.assertIn("<task-instruction>", invocation.display_argv())

    def test_opencode_hides_bash_when_task_has_no_control_plane_commands(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            worktree = root / "worktree"
            profile = root / "profile"
            worktree.mkdir()
            profile.mkdir()
            request = ProviderTaskRequest.from_mapping({
                "run_id": "adapter-test",
                "task_id": "write-only",
                "repository": "owner/repo",
                "worktree": str(worktree),
                "integration_branch": "factory/adapter-test",
                "target_branch": "main",
                "working_branch": "factory/adapter-test/write-only",
                "paths": ["docs/result.md"],
                "instruction": "Create exactly the requested file.",
                "allowed_commands": [],
            })
            config = OpenCodeOllamaAdapter(
                model="qwen3-coder", profile_home=profile
            ).opencode_config(request)
        self.assertFalse(config["tools"]["bash"])
        self.assertTrue(config["tools"]["write"])
        self.assertFalse(config["tools"]["edit"])
        self.assertFalse(config["tools"]["read"])
        self.assertFalse(config["tools"]["todowrite"])
        self.assertFalse(config["tools"]["lsp"])

    def test_opencode_rejects_repository_runtime_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            worktree = root / "worktree"
            profile = root / "profile"
            worktree.mkdir()
            profile.mkdir()
            (worktree / "opencode.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "repository-provided"):
                OpenCodeOllamaAdapter(
                    model="qwen3-coder", profile_home=profile
                ).build_invocation(self.request(worktree))

    def test_opencode_probe_requires_binaries_service_model_and_profile(self) -> None:
        runner = QueueRunner(
            CommandResult(0, "qwen3-coder latest", ""),
            CommandResult(0, "ollama/qwen3-coder", ""),
        )
        with tempfile.TemporaryDirectory() as raw, patch(
            "engine.providers.opencode_ollama.shutil.which", return_value="/bin/tool"
        ):
            health = OpenCodeOllamaAdapter(
                model="qwen3-coder", profile_home=Path(raw)
            ).probe(runner)
        self.assertEqual(health.status, "healthy")

    def test_opencode_rejects_remote_or_credentialed_ollama_url(self) -> None:
        for url in (
            "https://ollama.example.com/v1",
            "http://user:password@localhost:11434/v1",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                OpenCodeOllamaAdapter(model="qwen3-coder", ollama_base_url=url)


if __name__ == "__main__":
    unittest.main()
