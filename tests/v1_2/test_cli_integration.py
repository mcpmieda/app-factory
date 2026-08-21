from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts" / "factory.py"


class CLIIntegrationTests(unittest.TestCase):
    def run_cli(self, project: Path, *args: str) -> dict[str, object]:
        completed = subprocess.run(
            [sys.executable, str(CLI), "--root", str(project), *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return json.loads(completed.stdout)

    def make_project(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        project = Path(temp.name)
        (project / "PROJECT_STATE.md").write_text(
            "# PROJECT_STATE\n\n## Objetivo atual\n\nCriar um sistema escolar simples.\n",
            encoding="utf-8",
        )
        (project / "app.py").write_text("def run():\n    return 1\n", encoding="utf-8")
        return temp, project

    def test_resume_includes_current_agent_execution_decision(self) -> None:
        temp, project = self.make_project()
        self.addCleanup(temp.cleanup)
        payload = self.run_cli(project, "resume")
        self.assertEqual(payload["action"]["action"], "plan")
        self.assertEqual(payload["execution"]["backend"], "current_agent")

    def test_verification_routes_to_ci_after_state_transition(self) -> None:
        temp, project = self.make_project()
        self.addCleanup(temp.cleanup)
        self.run_cli(project, "resume")
        self.run_cli(project, "record", "plan-ready", "--summary", "fatia")
        payload = self.run_cli(project, "record", "implementation-ready", "--summary", "feito")
        self.assertEqual(payload["next"]["action"], "verify")
        self.assertEqual(payload["execution"]["backend"], "github_ci")

    def test_interactive_route_requires_explicit_local_backend_availability(self) -> None:
        temp, project = self.make_project()
        self.addCleanup(temp.cleanup)
        failed = subprocess.run(
            [
                sys.executable,
                str(CLI),
                "--root",
                str(project),
                "route",
                "verify",
                "--interactive-browser",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(failed.returncode, 2)
        payload = json.loads(failed.stdout)
        self.assertIsNone(payload["backend"])

        completed = subprocess.run(
            [
                sys.executable,
                str(CLI),
                "--root",
                str(project),
                "--backends",
                "current_agent,github_ci,local_full",
                "route",
                "verify",
                "--interactive-browser",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["backend"], "local_full")


if __name__ == "__main__":
    unittest.main()
