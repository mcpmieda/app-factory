from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts" / "factory.py"


class SemanticCliTests(unittest.TestCase):
    def run_cli(self, root: Path, *args: str, expected: int = 0) -> dict[str, object]:
        result = subprocess.run(
            [sys.executable, str(CLI), "--root", str(root), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, expected, msg=result.stderr or result.stdout)
        return json.loads(result.stdout)

    def test_require_spec_routes_to_specification_and_cli_validates_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "PROJECT_STATE.md").write_text(
                "# PROJECT_STATE\n\n## Objetivo atual\n\nCriar cadastro verificável.\n",
                encoding="utf-8",
            )
            (root / "app.py").write_text("def main():\n    return True\n", encoding="utf-8")

            template = self.run_cli(
                root,
                "spec-template",
                "--goal",
                "Criar cadastro verificável",
                "--change-type",
                "functional",
                "--risk",
                "medium",
            )
            self.assertEqual(template["change_type"], "functional")
            self.assertEqual(template["acceptance_criteria"], [])

            self.run_cli(root, "init", "--goal", "Criar cadastro", "--require-spec")
            recorded = self.run_cli(root, "record", "plan-ready", "--summary", "cadastro")
            self.assertEqual(recorded["next"]["action"], "specify")

            invalid = self.run_cli(root, "spec-validate", expected=1)
            self.assertFalse(invalid["valid"])

            specs = root / "specs"
            specs.mkdir()
            (specs / "semantic-contract.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "goal": "Criar cadastro verificável.",
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
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            valid = self.run_cli(root, "spec-validate")
            self.assertTrue(valid["valid"])
            plan = self.run_cli(root, "verification-plan-init")
            self.assertTrue(plan["written"])
            self.assertTrue((specs / "verification-plan.json").is_file())


if __name__ == "__main__":
    unittest.main()
