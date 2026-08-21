from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from engine.review_packet import build_clean_review_packet


@unittest.skipUnless(shutil.which("git"), "git is required for review-packet validation")
class ReviewPacketTests(unittest.TestCase):
    def git(self, root: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def test_packet_contains_current_spec_and_diff_but_not_prior_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.git(root, "init", "-b", "main")
            self.git(root, "config", "user.email", "factory@example.invalid")
            self.git(root, "config", "user.name", "App Factory Test")

            specs = root / "specs"
            specs.mkdir()
            spec = {
                "schema_version": 1,
                "goal": "Salvar cadastro escolar verificável.",
                "change_type": "functional",
                "risk": "medium",
                "scope": {"in": ["cadastro"], "out": []},
                "assumptions": [],
                "invariants": [],
                "data_contracts": [],
                "interfaces": [],
                "acceptance_criteria": [
                    {
                        "id": "AC-001",
                        "priority": "must",
                        "given": "dados válidos",
                        "when": "salvar",
                        "then": ["persistir"],
                        "verification": ["test"],
                    }
                ],
            }
            (specs / "semantic-contract.json").write_text(json.dumps(spec), encoding="utf-8")
            (specs / "verification-plan.json").write_text(
                json.dumps({"schema_version": 1, "spec_fingerprint": "fixture", "criteria": []}),
                encoding="utf-8",
            )
            (root / "app.py").write_text("def save():\n    return False\n", encoding="utf-8")
            self.git(root, "add", "app.py", "specs/semantic-contract.json", "specs/verification-plan.json")
            self.git(root, "commit", "-m", "baseline")

            self.git(root, "checkout", "-b", "feature")
            (root / "app.py").write_text("def save():\n    return True\n", encoding="utf-8")
            (specs / "review-evidence.json").write_text(
                json.dumps({"implementation_reasoning": "trust me", "verdict": "pass"}),
                encoding="utf-8",
            )
            self.git(root, "add", "app.py", "specs/review-evidence.json")
            self.git(root, "commit", "-m", "implement save")

            packet = build_clean_review_packet(root, base_ref="main")
            self.assertIn("Fresh review input only", packet["review_contract"])
            self.assertEqual(packet["spec"]["goal"], spec["goal"])
            self.assertTrue(packet["change"]["available"])
            self.assertIn("app.py", packet["change"]["changed_files"])
            self.assertNotIn("specs/review-evidence.json", packet["change"]["changed_files"])
            self.assertIn("return True", packet["change"]["diff"])
            self.assertNotIn("implementation_reasoning", json.dumps(packet))
            self.assertNotIn("current_review", packet)


if __name__ == "__main__":
    unittest.main()
