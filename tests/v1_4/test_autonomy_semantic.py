from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine.autonomy_engine import init_project, next_action, read_state, record_event
from engine.semantic_verification import (
    create_verification_plan,
    write_review_evidence,
    write_spec,
    write_verification_plan,
)


class AutonomySemanticTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "PROJECT_STATE.md").write_text(
            "# PROJECT_STATE\n\n## Objetivo atual\n\nCriar cadastro escolar verificável.\n",
            encoding="utf-8",
        )
        (root / "app.py").write_text("def save():\n    return True\n", encoding="utf-8")
        (root / "scripts").mkdir()
        (root / "scripts/validate_factory.py").write_text("print('ok')\n", encoding="utf-8")
        (root / "tests").mkdir()
        (root / "tests/test_app.py").write_text("def test_save():\n    assert True\n", encoding="utf-8")
        return temp, root

    def spec(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "goal": "Criar cadastro escolar verificável.",
            "change_type": "functional",
            "risk": "medium",
            "scope": {"in": ["salvar cadastro"], "out": ["relatórios"]},
            "assumptions": [],
            "invariants": [
                {"id": "INV-001", "statement": "Dados inválidos não são persistidos."}
            ],
            "data_contracts": [],
            "interfaces": [],
            "acceptance_criteria": [
                {
                    "id": "AC-001",
                    "priority": "must",
                    "given": "dados válidos",
                    "when": "o cadastro é salvo",
                    "then": ["o cadastro é persistido"],
                    "verification": ["test"],
                }
            ],
        }

    def attach_plan(self, root: Path, spec: dict[str, object]) -> None:
        plan = create_verification_plan(spec)
        plan["criteria"][0]["evidence"] = [
            {
                "kind": "test",
                "ref": "tests/test_app.py",
                "gate": "python:scripts/validate_factory.py",
            }
        ]
        write_verification_plan(root, plan)

    def test_required_spec_inserts_semantic_phase_and_guards_delivery(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        state = init_project(root, goal="Criar cadastro", require_spec=True)
        self.assertTrue(state["spec_required"])

        record_event(root, "plan-ready", "cadastro completo")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "specify")

        with self.assertRaisesRegex(ValueError, "Semantic specification"):
            record_event(root, "spec-ready")
        self.assertEqual(read_state(root)["phase"], "specification")

        spec = self.spec()
        write_spec(root, spec)
        record_event(root, "spec-ready", "contrato aprovado")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "implement")

        record_event(root, "implementation-ready", "implementado")
        with self.assertRaisesRegex(ValueError, "verification plan"):
            record_event(root, "verification-pass", "testes verdes")
        self.assertEqual(read_state(root)["phase"], "verification")

        self.attach_plan(root, spec)
        record_event(root, "verification-pass", "gates executados")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "review")

        with self.assertRaisesRegex(ValueError, "review evidence"):
            record_event(root, "review-pass", "autoaprovação não permitida")
        self.assertEqual(read_state(root)["phase"], "review")

        write_review_evidence(
            root,
            mode="clean-context",
            verdict="pass",
            criterion_results={"AC-001": "pass"},
        )
        record_event(root, "review-pass", "review clean-context aprovado")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "deliver")

    def test_legacy_flow_remains_available_when_spec_is_not_required(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        init_project(root, goal="Ajuste técnico pequeno")
        record_event(root, "plan-ready", "ajuste localizado")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "implement")


if __name__ == "__main__":
    unittest.main()
