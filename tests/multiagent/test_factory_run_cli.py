from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts" / "factory_run.py"


class FactoryRunCliTests(unittest.TestCase):
    def run_cli(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=ROOT,
            check=check,
            capture_output=True,
            text=True,
            timeout=60,
        )

    def test_template_is_valid_json(self) -> None:
        result = self.run_cli("template")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema_version"], 1)
        self.assertTrue(payload["tasks"])

    def test_plan_routes_remote_workers(self) -> None:
        spec = {
            "schema_version": 1,
            "run_id": "cli",
            "goal": "plan",
            "tasks": [
                {
                    "id": "a",
                    "title": "A",
                    "paths": ["src/a"],
                    "required_capabilities": ["reasoning", "repo_read", "repo_write"],
                },
                {
                    "id": "b",
                    "title": "B",
                    "paths": ["src/b"],
                    "required_capabilities": ["reasoning", "repo_read", "repo_write"],
                },
            ],
        }
        with tempfile.TemporaryDirectory(prefix="factory-run-") as raw:
            path = Path(raw) / "run.json"
            path.write_text(json.dumps(spec), encoding="utf-8")
            result = self.run_cli("plan", str(path), "--providers", "jules,antigravity")
            payload = json.loads(result.stdout)
        self.assertEqual(len(payload["waves"]), 1)
        self.assertEqual(len(payload["waves"][0]["assignments"]), 2)
        self.assertFalse(payload["blocked"])

    def test_blocked_plan_returns_two(self) -> None:
        spec = {
            "schema_version": 1,
            "run_id": "blocked",
            "goal": "blocked",
            "tasks": [
                {
                    "id": "activate",
                    "title": "Activate",
                    "human_gates": ["production_activation"],
                    "required_capabilities": ["reasoning"],
                }
            ],
        }
        with tempfile.TemporaryDirectory(prefix="factory-run-blocked-") as raw:
            path = Path(raw) / "run.json"
            path.write_text(json.dumps(spec), encoding="utf-8")
            result = self.run_cli("plan", str(path), "--providers", "jules", check=False)
            payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["blocked"][0]["status"], "human-required")

    def test_cli_rejects_parallelism_above_control_plane_ceiling(self) -> None:
        with tempfile.TemporaryDirectory(prefix="factory-run-parallel-") as raw:
            path = Path(raw) / "run.json"
            path.write_text(json.dumps({
                "schema_version": 1,
                "run_id": "parallel",
                "goal": "guard",
                "tasks": [{
                    "id": "a",
                    "title": "A",
                    "paths": ["src/a"],
                    "required_capabilities": ["reasoning"],
                }],
            }), encoding="utf-8")
            result = self.run_cli(
                "plan", str(path), "--providers", "jules", "--max-parallel", "4", check=False
            )
            payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertIn("between 1 and 3", payload["error"])


if __name__ == "__main__":
    unittest.main()
