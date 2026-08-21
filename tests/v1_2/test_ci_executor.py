from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.ci_executor import build_ci_plan, discover_declared_gates, run_declared_gates


class CIExecutorTests(unittest.TestCase):
    def make_node_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "package.json").write_text(json.dumps({
            "scripts": {
                "lint": "echo lint",
                "typecheck": "echo types",
                "test": "echo tests",
                "build": "echo build",
                "dangerous": "rm -rf /",
            }
        }), encoding="utf-8")
        (root / "package-lock.json").write_text("{}", encoding="utf-8")
        return temp, root

    def test_gate_discovery_uses_ids_and_never_script_body(self) -> None:
        temp, root = self.make_node_repo()
        self.addCleanup(temp.cleanup)
        gates = discover_declared_gates(root)
        ids = [gate.gate_id for gate in gates]
        self.assertEqual(ids, ["package:lint", "package:typecheck", "package:test", "package:build"])
        argv = [gate.argv for gate in gates]
        self.assertIn(("npm", "run", "lint"), argv)
        self.assertFalse(any("rm -rf" in part for gate in gates for part in gate.argv))
        self.assertNotIn("package:dangerous", ids)

    def test_ci_plan_declares_no_shell_prompt_or_secret_execution(self) -> None:
        temp, root = self.make_node_repo()
        self.addCleanup(temp.cleanup)
        plan = build_ci_plan(root)
        self.assertEqual(plan["install_argv"], ["npm", "ci"])
        self.assertFalse(plan["security"]["shell"])
        self.assertFalse(plan["security"]["prompt_commands"])
        self.assertFalse(plan["security"]["secrets_required"])

    def test_known_python_validator_can_run_without_shell(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "scripts").mkdir()
        (root / "scripts/validate_factory.py").write_text(
            "print('validator-ok')\n",
            encoding="utf-8",
        )
        results = run_declared_gates(root)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].success)
        self.assertIn("validator-ok", results[0].stdout_tail)

    def test_unknown_gate_id_is_rejected_before_execution(self) -> None:
        temp, root = self.make_node_repo()
        self.addCleanup(temp.cleanup)
        with self.assertRaisesRegex(ValueError, "Unknown or undeclared"):
            run_declared_gates(root, gate_ids=["package:dangerous"])


if __name__ == "__main__":
    unittest.main()
