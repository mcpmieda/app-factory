from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from engine.provider_runtime import CommandResult, ProviderInvocation, ProviderTaskRequest
from engine.providers.antigravity import AntigravityAdapter, _last_json_object, _probe_cwd
from engine.providers.opencode_ollama import (
    OpenCodeOllamaAdapter,
    _first_string,
    _json_objects,
)


class QueueRunner:
    def __init__(self, *results: CommandResult) -> None:
        self.results = list(results)
        self.invocations: list[ProviderInvocation] = []

    def run(self, invocation: ProviderInvocation) -> CommandResult:
        self.invocations.append(invocation)
        return self.results.pop(0)


class ProviderAdapterCoverageTests(unittest.TestCase):
    def request(self, worktree: Path) -> ProviderTaskRequest:
        return ProviderTaskRequest.from_mapping({
            "run_id": "run",
            "task_id": "worker",
            "repository": "owner/repo",
            "worktree": str(worktree),
            "integration_branch": "factory/run",
            "target_branch": "main",
            "working_branch": "factory/run/worker",
            "paths": ["docs/worker"],
            "instruction": "Create docs.",
            "allowed_commands": ["python -m unittest*"],
        })

    def test_antigravity_constructor_environment_and_profile_guards(self) -> None:
        with self.assertRaisesRegex(ValueError, "effort"):
            AntigravityAdapter(effort="extreme")
        with patch.dict(os.environ, {
            "ANTIGRAVITY_BIN": "custom-agy",
            "ANTIGRAVITY_MODEL": "model-x",
            "ANTIGRAVITY_EFFORT": "medium",
            "ANTIGRAVITY_AGENT": "worker",
            "ANTIGRAVITY_PROFILE_HOME": "/tmp/ag-profile",
        }, clear=False):
            adapter = AntigravityAdapter.from_environment()
        self.assertEqual(adapter.binary, "custom-agy")
        self.assertEqual(adapter.model, "model-x")
        self.assertEqual(adapter.effort, "medium")
        self.assertEqual(adapter.agent, "worker")

        with self.assertRaisesRegex(ValueError, "PROFILE_HOME"):
            AntigravityAdapter().profile_environment()
        with tempfile.TemporaryDirectory() as raw:
            missing = Path(raw) / "missing"
            with self.assertRaisesRegex(ValueError, "does not exist"):
                AntigravityAdapter(profile_home=missing).profile_environment()
            profile = Path(raw) / "profile"
            profile.mkdir()
            env = AntigravityAdapter(profile_home=profile).profile_environment()
            self.assertEqual(env["HOME"], str(profile.resolve()))
            self.assertIn("XDG_CONFIG_HOME", env)

            worktree = Path(raw) / "repo"
            worktree.mkdir()
            request = self.request(worktree)
            inside = worktree / "profile"
            inside.mkdir()
            with self.assertRaisesRegex(ValueError, "outside"):
                AntigravityAdapter(profile_home=inside).validate_workspace(request)
            AntigravityAdapter(profile_home=profile).validate_workspace(request)

    def test_antigravity_probe_all_health_paths(self) -> None:
        no_profile = AntigravityAdapter().probe(QueueRunner())
        self.assertEqual(no_profile.status, "unavailable")
        with tempfile.TemporaryDirectory() as raw:
            profile = Path(raw)
            adapter = AntigravityAdapter(profile_home=profile, binary="agy")
            with patch("engine.providers.antigravity.shutil.which", return_value=None):
                self.assertEqual(adapter.probe(QueueRunner()).status, "unavailable")
            with patch("engine.providers.antigravity.shutil.which", return_value="/bin/agy"):
                version_fail = adapter.probe(QueueRunner(CommandResult(1, "", "version failed")))
                self.assertEqual(version_fail.status, "unavailable")

                auth_fail = adapter.probe(QueueRunner(
                    CommandResult(0, "agy 1.0", ""),
                    CommandResult(1, "", "auth required"),
                ))
                self.assertEqual(auth_fail.status, "degraded")
                self.assertIn("version", auth_fail.details)

                missing_model = AntigravityAdapter(
                    profile_home=profile, binary="agy", model="wanted-model"
                ).probe(QueueRunner(
                    CommandResult(0, "agy 1.0", ""),
                    CommandResult(0, "other-model", ""),
                ))
                self.assertEqual(missing_model.status, "unavailable")

                healthy = AntigravityAdapter(
                    profile_home=profile, binary="agy", model="wanted-model"
                ).probe(QueueRunner(
                    CommandResult(0, "agy 1.0", ""),
                    CommandResult(0, "wanted-model", ""),
                ))
                self.assertEqual(healthy.status, "healthy")

    def test_antigravity_invocation_and_output_parsing_edges(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            worktree = root / "repo"
            profile = root / "profile"
            worktree.mkdir()
            profile.mkdir()
            request = self.request(worktree)
            adapter = AntigravityAdapter(
                profile_home=profile,
                binary="agy-custom",
                model="model-x",
                effort="high",
                agent="agent-x",
            )
            invocation = adapter.build_invocation(request)
            self.assertEqual(invocation.argv[0], "agy-custom")
            self.assertIn("--model", invocation.argv)
            self.assertIn("--effort", invocation.argv)
            self.assertIn("--agent", invocation.argv)
            self.assertEqual(invocation.sensitive_argument_indexes, frozenset({2}))

        success = adapter.parse_output(CommandResult(0, json.dumps({
            "status": "SUCCESS",
            "response": "done",
            "conversation_id": "conversation",
            "usage": {"tokens": 2},
        }), ""))
        self.assertEqual(success.status, "success")
        self.assertEqual(success.session_id, "conversation")

        canceled = adapter.parse_output(CommandResult(1, '{"status":"CANCELED","error":"token=abc"}', ""))
        self.assertEqual(canceled.status, "canceled")
        self.assertNotIn("abc", canceled.error)
        interrupted = adapter.parse_output(CommandResult(1, '{"status":"INTERRUPTED"}', ""))
        self.assertEqual(interrupted.status, "interrupted")
        failed = adapter.parse_output(CommandResult(1, "not-json", "password=bad"))
        self.assertEqual(failed.status, "failed")
        self.assertNotIn("bad", failed.error)

        self.assertEqual(_last_json_object('{"status":"SUCCESS"}')["status"], "SUCCESS")
        self.assertEqual(_last_json_object('noise\n{"status":"SUCCESS"}\n')["status"], "SUCCESS")
        self.assertEqual(_last_json_object("noise\n[]\n"), {})
        self.assertEqual(_probe_cwd(), Path.cwd())

    def test_opencode_constructor_environment_profile_and_workspace_guards(self) -> None:
        with self.assertRaisesRegex(ValueError, "explicit local model"):
            OpenCodeOllamaAdapter(model="")
        with self.assertRaisesRegex(ValueError, "only the ollama provider"):
            OpenCodeOllamaAdapter(model="openai/gpt")
        for url in ("https://example.com/v1", "http://user:pass@localhost:11434/v1", "ftp://localhost"):
            with self.subTest(url=url), self.assertRaisesRegex(ValueError, "loopback-only"):
                OpenCodeOllamaAdapter(model="qwen", ollama_base_url=url)

        with patch.dict(os.environ, {
            "OPENCODE_OLLAMA_MODEL": "qwen",
            "OPENCODE_BIN": "oc",
            "OLLAMA_BIN": "ol",
            "OPENCODE_AGENT": "worker",
            "OLLAMA_BASE_URL": "http://127.0.0.1:11434/v1",
            "OPENCODE_PROFILE_HOME": "/tmp/oc-profile",
        }, clear=False):
            adapter = OpenCodeOllamaAdapter.from_environment()
        self.assertEqual(adapter.model, "ollama/qwen")
        self.assertEqual(adapter.binary, "oc")
        self.assertEqual(adapter.ollama_binary, "ol")
        self.assertEqual(adapter.agent, "worker")

        with self.assertRaisesRegex(ValueError, "PROFILE_HOME"):
            OpenCodeOllamaAdapter(model="qwen").profile_environment()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            missing = root / "missing"
            with self.assertRaisesRegex(ValueError, "does not exist"):
                OpenCodeOllamaAdapter(model="qwen", profile_home=missing).profile_environment()
            profile = root / "profile"
            worktree = root / "repo"
            profile.mkdir()
            worktree.mkdir()
            env = OpenCodeOllamaAdapter(model="qwen", profile_home=profile).profile_environment()
            self.assertTrue(Path(env["OPENCODE_CONFIG_DIR"]).is_dir())
            request = self.request(worktree)
            inside = worktree / "profile"
            inside.mkdir()
            with self.assertRaisesRegex(ValueError, "outside"):
                OpenCodeOllamaAdapter(model="qwen", profile_home=inside).validate_workspace(request)
            for relative in ("opencode.json", "opencode.jsonc", ".opencode"):
                path = worktree / relative
                if relative == ".opencode":
                    path.mkdir()
                else:
                    path.write_text("{}", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "repository-provided"):
                    OpenCodeOllamaAdapter(model="qwen", profile_home=profile).validate_workspace(request)
                if path.is_dir():
                    path.rmdir()
                else:
                    path.unlink()

    def test_opencode_probe_all_health_paths(self) -> None:
        self.assertEqual(OpenCodeOllamaAdapter(model="qwen").probe(QueueRunner()).status, "unavailable")
        with tempfile.TemporaryDirectory() as raw:
            profile = Path(raw)
            adapter = OpenCodeOllamaAdapter(model="qwen", profile_home=profile)
            with patch("engine.providers.opencode_ollama.shutil.which", side_effect=lambda binary: None if binary == "ollama" else "/bin/tool"):
                self.assertEqual(adapter.probe(QueueRunner()).status, "unavailable")
            with patch("engine.providers.opencode_ollama.shutil.which", return_value="/bin/tool"):
                service_fail = adapter.probe(QueueRunner(CommandResult(1, "", "service down")))
                self.assertEqual(service_fail.status, "unavailable")

                missing_model = adapter.probe(QueueRunner(CommandResult(0, "NAME ID SIZE\nother:latest x 1GB", "")))
                self.assertEqual(missing_model.status, "unavailable")

                enumerate_fail = adapter.probe(QueueRunner(
                    CommandResult(0, "NAME ID SIZE\nqwen:latest x 1GB", ""),
                    CommandResult(1, "", "opencode failed"),
                ))
                self.assertEqual(enumerate_fail.status, "degraded")

                healthy = adapter.probe(QueueRunner(
                    CommandResult(0, "NAME ID SIZE\nqwen:latest x 1GB", ""),
                    CommandResult(0, "ollama/qwen", ""),
                ))
                self.assertEqual(healthy.status, "healthy")
                self.assertEqual(healthy.details["model"], "ollama/qwen")

    def test_opencode_config_invocation_and_output_parsing_edges(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            profile = root / "profile"
            worktree = root / "repo"
            profile.mkdir()
            worktree.mkdir()
            request = self.request(worktree)
            adapter = OpenCodeOllamaAdapter(
                model="qwen", profile_home=profile, agent="worker-agent"
            )
            permissions = adapter.permission_config(request)
            self.assertEqual(permissions["edit"]["docs/worker/**"], "allow")
            self.assertEqual(permissions["edit"][".github/**"], "deny")
            self.assertEqual(permissions["bash"]["git push*"], "deny")
            config = adapter.opencode_config(request)
            self.assertEqual(config["enabled_providers"], ["ollama"])
            invocation = adapter.build_invocation(request)
            self.assertIn("--agent", invocation.argv)
            self.assertIn("worker-agent", invocation.argv)
            self.assertEqual(invocation.sensitive_argument_indexes, frozenset({len(invocation.argv) - 1}))
            self.assertIn("OPENCODE_CONFIG_CONTENT", invocation.env)
            self.assertIn("OPENCODE_DISABLE_DEFAULT_PLUGINS", invocation.env)

        parsed = adapter.parse_output(CommandResult(0, "\n".join([
            '{"type":"message","sessionID":"session","text":"first","usage":{"tokens":1}}',
            '{"event":"message","content":"second"}',
            '{"response":"third"}',
            '{"message":"fourth"}',
        ]), ""))
        self.assertEqual(parsed.status, "success")
        self.assertEqual(parsed.session_id, "session")
        self.assertEqual(parsed.usage, {"tokens": 1})
        self.assertNotIn("first", parsed.response)
        self.assertIn("fourth", parsed.response)

        event_error = adapter.parse_output(CommandResult(0, '{"type":"error","message":"token=abc"}', ""))
        self.assertEqual(event_error.status, "failed")
        self.assertNotIn("abc", event_error.error)
        process_error = adapter.parse_output(CommandResult(1, "not-json", "password=bad"))
        self.assertEqual(process_error.status, "failed")
        self.assertNotIn("bad", process_error.error)

        self.assertEqual(_json_objects('noise\n[]\n{"type":"ok"}\n'), [{"type": "ok"}])
        self.assertEqual(_first_string({"a": "", "b": " value "}, "a", "b"), "value")
        self.assertIsNone(_first_string({"a": 1}, "a", "b"))


if __name__ == "__main__":
    unittest.main()
