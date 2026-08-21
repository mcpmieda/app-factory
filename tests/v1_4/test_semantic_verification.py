from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.semantic_verification import (
    create_verification_plan,
    read_review_evidence,
    semantic_spec_required,
    semantic_status,
    spec_fingerprint,
    validate_review_evidence,
    validate_spec,
    validate_verification_plan,
    write_review_evidence,
    write_spec,
    write_verification_plan,
)


class SemanticVerificationTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "scripts").mkdir()
        (root / "scripts/validate_factory.py").write_text("print('ok')\n", encoding="utf-8")
        (root / "tests").mkdir()
        (root / "tests/test_app.py").write_text("def test_save():\n    assert True\n", encoding="utf-8")
        (root / "app.py").write_text("def save():\n    return True\n", encoding="utf-8")
        return temp, root

    def valid_spec(self, *, risk: str = "medium") -> dict[str, object]:
        return {
            "schema_version": 1,
            "goal": "Salvar cadastro escolar com validação observável.",
            "change_type": "functional",
            "risk": risk,
            "scope": {"in": ["cadastro"], "out": ["relatórios"]},
            "assumptions": [],
            "invariants": [
                {"id": "INV-001", "statement": "Cadastro inválido nunca é persistido."}
            ],
            "data_contracts": [],
            "interfaces": [],
            "acceptance_criteria": [
                {
                    "id": "AC-001",
                    "priority": "must",
                    "given": "dados válidos",
                    "when": "o usuário salva",
                    "then": ["o cadastro é persistido", "o usuário recebe confirmação"],
                    "verification": ["test"],
                },
                {
                    "id": "AC-002",
                    "priority": "should",
                    "given": "dados inválidos",
                    "when": "o usuário tenta salvar",
                    "then": ["a persistência é rejeitada"],
                    "verification": ["test"],
                },
            ],
        }

    def attach_must_evidence(self, plan: dict[str, object]) -> None:
        rows = plan["criteria"]
        assert isinstance(rows, list)
        row = next(item for item in rows if item["id"] == "AC-001")
        row["evidence"] = [
            {
                "kind": "test",
                "ref": "tests/test_app.py",
                "gate": "python:scripts/validate_factory.py",
            }
        ]

    def test_relevant_work_requires_semantic_spec_but_docs_do_not(self) -> None:
        self.assertTrue(semantic_spec_required("functional", "low"))
        self.assertTrue(semantic_spec_required("bugfix", "medium"))
        self.assertFalse(semantic_spec_required("docs", "high"))
        self.assertFalse(semantic_spec_required("refactor", "low"))

    def test_valid_spec_and_traceability_pass(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec = self.valid_spec()
        write_spec(root, spec)
        plan = create_verification_plan(spec)
        self.attach_must_evidence(plan)
        write_verification_plan(root, plan)

        self.assertEqual(validate_spec(spec), [])
        self.assertEqual(validate_verification_plan(root), [])

    def test_missing_must_evidence_fails(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec = self.valid_spec()
        write_spec(root, spec)
        write_verification_plan(root, create_verification_plan(spec))

        errors = validate_verification_plan(root)
        self.assertTrue(any("AC-001" in error and "executable" in error for error in errors))

    def test_plan_becomes_stale_when_spec_changes(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec = self.valid_spec()
        write_spec(root, spec)
        plan = create_verification_plan(spec)
        self.attach_must_evidence(plan)
        write_verification_plan(root, plan)

        changed = json.loads(json.dumps(spec))
        changed["goal"] = "Salvar cadastro escolar com nova regra obrigatória."
        write_spec(root, changed)
        errors = validate_verification_plan(root)
        self.assertTrue(any("stale" in error for error in errors))
        self.assertNotEqual(plan["spec_fingerprint"], spec_fingerprint(changed))

    def test_medium_risk_rejects_ci_only_review(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec = self.valid_spec(risk="medium")
        write_spec(root, spec)
        plan = create_verification_plan(spec)
        self.attach_must_evidence(plan)
        write_verification_plan(root, plan)

        with self.assertRaisesRegex(ValueError, "clean-context"):
            write_review_evidence(
                root,
                mode="deterministic-ci",
                verdict="pass",
                criterion_results={"AC-001": "pass"},
            )

    def test_clean_context_review_is_bound_to_current_subject(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec = self.valid_spec(risk="medium")
        write_spec(root, spec)
        plan = create_verification_plan(spec)
        self.attach_must_evidence(plan)
        write_verification_plan(root, plan)
        review = write_review_evidence(
            root,
            mode="clean-context",
            verdict="pass",
            criterion_results={"AC-001": "pass", "AC-002": "pass"},
        )

        self.assertEqual(validate_review_evidence(root), [])
        self.assertEqual(read_review_evidence(root)["subject_fingerprint"], review["subject_fingerprint"])
        self.assertTrue(semantic_status(root).ready_for_delivery)

        (root / "app.py").write_text("def save():\n    return False\n", encoding="utf-8")
        errors = validate_review_evidence(root)
        self.assertTrue(any("subject changed" in error for error in errors))
        self.assertFalse(semantic_status(root).ready_for_delivery)

    def test_low_risk_can_use_deterministic_ci_review(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec = self.valid_spec(risk="low")
        write_spec(root, spec)
        plan = create_verification_plan(spec)
        self.attach_must_evidence(plan)
        write_verification_plan(root, plan)
        write_review_evidence(
            root,
            mode="deterministic-ci",
            verdict="pass",
            criterion_results={"AC-001": "pass"},
        )
        self.assertEqual(validate_review_evidence(root), [])


if __name__ == "__main__":
    unittest.main()
