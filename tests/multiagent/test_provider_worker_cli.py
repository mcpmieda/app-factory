from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts" / "provider_worker.py"


class ProviderWorkerCliTests(unittest.TestCase):
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
    def request(worktree: Path) -> dict[str, object]:
        return {
            "run_id": "cli-provider",
            "task_id": "worker-a",
            "repository": "owner/repo",
            "worktree": str(worktree),
            "integration_branch": "factory/cli-provider",
            "target_branch": "main",
            "working_branch": "factory/cli-provider/worker-a",
            "paths": ["docs/worker-a"],
            "instruction": "SENSITIVE TASK INSTRUCTION",
            "allowed_commands": ["python -m unittest*"],
        }

    def test_validate_and_redacted_command_are_machine_readable(self) -> None:
        with tempfile.TemporaryDirectory(prefix="provider-cli-") as raw:
            root = Path(raw)
            worktree = root / "worktree"
            profile = root / "profile"
            worktree.mkdir()
            profile.mkdir()
            spec = root / "request.json"
            spec.write_text(json.dumps(self.request(worktree)), encoding="utf-8")

            validated = self.run_cli("validate", str(spec))
            payload = json.loads(validated.stdout)
            self.assertTrue(payload["valid"])
            self.assertNotIn("instruction", payload["request"])

            command = self.run_cli(
                "command",
                "--provider",
                "opencode_ollama",
                "--model",
                "qwen3-coder",
                "--profile-home",
                str(profile),
                str(spec),
            )
            command_payload = json.loads(command.stdout)
            rendered = json.dumps(command_payload)
            self.assertIn("<task-instruction>", rendered)
            self.assertNotIn("SENSITIVE TASK INSTRUCTION", rendered)
            self.assertIn("OPENCODE_CONFIG_CONTENT", rendered)

    def test_run_refuses_non_durable_local_only_completion(self) -> None:
        with tempfile.TemporaryDirectory(prefix="provider-cli-publish-") as raw:
            root = Path(raw)
            worktree = root / "worktree"
            profile = root / "profile"
            worktree.mkdir()
            profile.mkdir()
            spec = root / "request.json"
            spec.write_text(json.dumps(self.request(worktree)), encoding="utf-8")
            result = self.run_cli(
                "run",
                "--provider",
                "antigravity",
                "--profile-home",
                str(profile),
                str(spec),
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertIn("requires --publish", payload["error"])

    def test_validate_rejects_protected_scope(self) -> None:
        with tempfile.TemporaryDirectory(prefix="provider-cli-scope-") as raw:
            root = Path(raw)
            spec = root / "request.json"
            request = self.request(root / "worktree")
            request["paths"] = [".github/workflows"]
            spec.write_text(json.dumps(request), encoding="utf-8")
            result = self.run_cli("validate", str(spec), check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("protected path", json.loads(result.stdout)["error"])


if __name__ == "__main__":
    unittest.main()
