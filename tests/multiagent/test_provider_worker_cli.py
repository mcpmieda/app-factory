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

    @staticmethod
    def init_repo(worktree: Path, branch: str) -> None:
        worktree.mkdir()
        subprocess.run(
            ["git", "init", "-b", branch], cwd=worktree, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.name", "Factory Test"], cwd=worktree, check=True
        )
        subprocess.run(
            ["git", "config", "user.email", "factory-test@example.invalid"],
            cwd=worktree,
            check=True,
        )
        subprocess.run(
            ["git", "remote", "add", "origin", "https://github.com/owner/repo.git"],
            cwd=worktree,
            check=True,
        )
        (worktree / "README.md").write_text("baseline\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=worktree, check=True)
        subprocess.run(
            ["git", "commit", "-m", "baseline"],
            cwd=worktree,
            check=True,
            capture_output=True,
        )

    @staticmethod
    def fake_antigravity(path: Path, *, content: str) -> None:
        path.write_text(
            "#!/usr/bin/env python3\n"
            "import json\n"
            "from pathlib import Path\n"
            "target = Path('docs/stage.txt')\n"
            "target.parent.mkdir(parents=True, exist_ok=True)\n"
            f"target.write_text({content!r}, encoding='utf-8')\n"
            "print(json.dumps({'status': 'SUCCESS', 'response': 'done', 'conversation_id': 'fake'}))\n",
            encoding="utf-8",
        )
        path.chmod(0o755)

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

    def test_stage_creates_sanitized_bundle_without_push(self) -> None:
        with tempfile.TemporaryDirectory(prefix="provider-cli-stage-") as raw:
            root = Path(raw)
            worktree = root / "worktree"
            profile = root / "profile"
            profile.mkdir()
            branch = "factory/cli-provider-worker-a"
            self.init_repo(worktree, branch)
            fake = root / "agy"
            self.fake_antigravity(fake, content="Antigravity staged provider evidence\n")

            request = self.request(worktree)
            request["working_branch"] = branch
            request["paths"] = ["docs/stage.txt"]
            request["allowed_commands"] = []
            spec = root / "request.json"
            spec.write_text(json.dumps(request), encoding="utf-8")
            bundle = root / "stage" / "provider.bundle"
            record = root / "stage" / "stage-record.json"

            result = self.run_cli(
                "stage",
                "--provider",
                "antigravity",
                "--binary",
                str(fake),
                "--profile-home",
                str(profile),
                "--effort",
                "medium",
                "--bundle",
                str(bundle),
                "--record",
                str(record),
                str(spec),
            )
            payload = json.loads(result.stdout)
            stage = json.loads(record.read_text(encoding="utf-8"))
            self.assertTrue(payload["staged"])
            self.assertTrue(bundle.is_file())
            self.assertEqual(stage["provider"], "antigravity")
            self.assertEqual(stage["working_branch"], branch)
            self.assertEqual(stage["changed_paths"], ["docs/stage.txt"])
            self.assertEqual(stage["declared_paths"], ["docs/stage.txt"])
            self.assertNotIn("instruction", stage)
            self.assertNotIn("response", stage)
            self.assertNotIn("session_id", stage)
            rendered = json.dumps(stage)
            self.assertNotIn("SENSITIVE TASK INSTRUCTION", rendered)
            self.assertNotIn(str(profile), rendered)
            subprocess.run(
                ["git", "bundle", "verify", str(bundle)],
                cwd=worktree,
                check=True,
                capture_output=True,
            )
            remote = subprocess.run(
                ["git", "ls-remote", "--heads", "origin", branch],
                cwd=worktree,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(remote.stdout.strip(), "")

    def test_stage_rejects_credential_pattern_before_bundle(self) -> None:
        with tempfile.TemporaryDirectory(prefix="provider-cli-stage-secret-") as raw:
            root = Path(raw)
            worktree = root / "worktree"
            profile = root / "profile"
            profile.mkdir()
            branch = "factory/cli-provider-secret-worker"
            self.init_repo(worktree, branch)
            fake = root / "agy"
            self.fake_antigravity(
                fake,
                content="token: ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\n",
            )

            request = self.request(worktree)
            request["working_branch"] = branch
            request["paths"] = ["docs/stage.txt"]
            request["allowed_commands"] = []
            spec = root / "request.json"
            spec.write_text(json.dumps(request), encoding="utf-8")
            bundle = root / "stage" / "provider.bundle"
            record = root / "stage" / "stage-record.json"

            result = self.run_cli(
                "stage",
                "--provider",
                "antigravity",
                "--binary",
                str(fake),
                "--profile-home",
                str(profile),
                "--bundle",
                str(bundle),
                "--record",
                str(record),
                str(spec),
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("credential pattern", json.loads(result.stdout)["error"])
            self.assertFalse(bundle.exists())
            self.assertFalse(record.exists())

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
