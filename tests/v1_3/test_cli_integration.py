from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from engine.learning_engine import record_learning_event


REPO_ROOT = Path(__file__).resolve().parents[2]
FACTORY = REPO_ROOT / "scripts" / "factory.py"
VERIFY_CAPS = ["deterministic_commands", "test"]


class LearningCLIIntegrationTests(unittest.TestCase):
    def make_project(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "README.md").write_text("Demo project for V1.3 tests.\n", encoding="utf-8")
        return temp, root

    def cli(self, root: Path, *args: str, backends: str | None = None) -> dict:
        command = [sys.executable, str(FACTORY), "--root", str(root)]
        if backends:
            command += ["--backends", backends]
        command += list(args)
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)

    def test_record_execution_updates_learning_without_summary_text(self) -> None:
        temp, root = self.make_project()
        self.addCleanup(temp.cleanup)
        secret_summary = "nome pessoal e log livre que não pode entrar no learning"
        payload = self.cli(
            root,
            "record-execution",
            "verify",
            "github_ci",
            "success",
            "--summary",
            secret_summary,
            "--duration-ms",
            "345",
        )
        self.assertEqual(payload["learning"]["events"], 1)
        raw_learning = (root / ".factory" / "learning.json").read_text(encoding="utf-8")
        self.assertNotIn(secret_summary, raw_learning)
        event = json.loads(raw_learning)["events"][0]
        self.assertEqual(event["capabilities"], VERIFY_CAPS)
        self.assertEqual(event["backend"], "github_ci")
        self.assertEqual(event["duration_ms"], 345)

    def test_cli_recommendation_recovers_learning_from_disk(self) -> None:
        temp, root = self.make_project()
        self.addCleanup(temp.cleanup)
        for _ in range(5):
            record_learning_event(
                root,
                action="verify",
                capabilities=VERIFY_CAPS,
                backend="github_ci",
                outcome="failure",
                duration_ms=5000,
            )
            record_learning_event(
                root,
                action="verify",
                capabilities=VERIFY_CAPS,
                backend="sandbox",
                outcome="success",
                duration_ms=1000,
            )
        payload = self.cli(
            root,
            "learning-recommend",
            "verify",
            backends="github_ci,sandbox",
        )
        self.assertEqual(payload["route"]["backend"], "sandbox")
        self.assertEqual(payload["route"]["selection_mode"], "learned")
        self.assertEqual(payload["learning"]["mode"], "learned")

    def test_no_learning_flag_exposes_v1_2_baseline(self) -> None:
        temp, root = self.make_project()
        self.addCleanup(temp.cleanup)
        for _ in range(5):
            record_learning_event(
                root,
                action="verify",
                capabilities=VERIFY_CAPS,
                backend="github_ci",
                outcome="failure",
            )
            record_learning_event(
                root,
                action="verify",
                capabilities=VERIFY_CAPS,
                backend="sandbox",
                outcome="success",
            )
        learned = self.cli(root, "route", "verify", backends="github_ci,sandbox")
        baseline = self.cli(root, "route", "verify", "--no-learning", backends="github_ci,sandbox")
        self.assertEqual(learned["backend"], "sandbox")
        self.assertEqual(baseline["backend"], "github_ci")
        self.assertEqual(baseline["selection_mode"], "baseline")

    def test_resume_exposes_execution_and_learning_explanation(self) -> None:
        temp, root = self.make_project()
        self.addCleanup(temp.cleanup)
        payload = self.cli(root, "resume")
        self.assertEqual(payload["action"]["action"], "plan")
        self.assertEqual(payload["execution"]["backend"], "current_agent")
        self.assertEqual(payload["execution"]["selection_mode"], "baseline")
        self.assertIsInstance(payload["execution"]["learning"], dict)

    def test_learning_status_is_aggregate_and_local_only(self) -> None:
        temp, root = self.make_project()
        self.addCleanup(temp.cleanup)
        self.cli(root, "record-execution", "verify", "github_ci", "success")
        payload = self.cli(root, "learning-status")
        self.assertEqual(payload["events"], 1)
        self.assertEqual(payload["contexts"], 1)
        self.assertTrue(payload["local_only"])
        self.assertFalse(payload["external_telemetry"])
        self.assertNotIn("raw_events", payload)


if __name__ == "__main__":
    unittest.main()
