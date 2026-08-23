from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.semantic_assurance import (
    analyze_assurance,
    coverage_report,
    new_assurance,
    recommend_semantic_depth,
    semantic_diff,
    validate_assurance,
    write_assurance,
)
from engine.semantic_verification import create_verification_plan, write_spec, write_verification_plan


class SemanticAssuranceTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "scripts").mkdir()
        (root / "scripts/validate_factory.py").write_text("print('ok')\n", encoding="utf-8")
        (root / "tests").mkdir()
        (root / "tests/test_app.py").write_text("def test_rule():\n    assert True\n", encoding="utf-8")
        return temp, root

    def spec(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "goal": "Controlar lançamento de notas por professor e turma.",
            "change_type": "functional",
            "risk": "medium",
            "scope": {"in": ["lançamento de nota"], "out": ["boletim público"]},
            "assumptions": [],
            "invariants": [
                {"id": "INV-001", "statement": "Professor nunca altera turma sem vínculo."}
            ],
            "data_contracts": [],
            "interfaces": [],
            "acceptance_criteria": [
                {
                    "id": "AC-001",
                    "priority": "must",
                    "given": "professor vinculado à turma",
                    "when": "salva uma nota válida",
                    "then": ["a nota é persistida"],
                    "verification": ["test"],
                },
                {
                    "id": "AC-002",
                    "priority": "must",
                    "given": "professor sem vínculo à turma",
                    "when": "tenta alterar uma nota",
                    "then": ["a alteração é negada"],
                    "verification": ["test"],
                },
            ],
        }

    def assurance(self, spec: dict[str, object]) -> dict[str, object]:
        value = new_assurance(spec, depth="domain")
        value.update(
            {
                "glossary": [
                    {"id": "TERM-001", "term": "vínculo", "definition": "Associação vigente entre professor, turma e disciplina.", "aliases": []}
                ],
                "entities": [
                    {"id": "ENT-001", "name": "Professor", "definition": "Docente responsável por uma ou mais turmas.", "attributes": []},
                    {"id": "ENT-002", "name": "Turma", "definition": "Grupo escolar em que notas são lançadas.", "attributes": []},
                ],
                "relations": [
                    {"id": "REL-001", "from": "ENT-001", "to": "ENT-002", "name": "possui vínculo", "min": 0, "max": None}
                ],
                "requirements": [
                    {
                        "id": "REQ-001",
                        "priority": "must",
                        "pattern": "event",
                        "component": "Sistema de notas",
                        "scope": ["professor autenticado"],
                        "preconditions": ["professor possui vínculo vigente"],
                        "trigger": "professor salva uma nota",
                        "response": ["persistir a nota"],
                        "timing": None,
                        "concept_refs": ["ENT-001", "ENT-002", "TERM-001"],
                        "acceptance_refs": ["AC-001"],
                        "invariant_refs": ["INV-001"],
                        "formalization_refs": [],
                    },
                    {
                        "id": "REQ-002",
                        "priority": "must",
                        "pattern": "policy",
                        "component": "Sistema de notas",
                        "scope": ["operação protegida"],
                        "preconditions": [],
                        "trigger": "professor sem vínculo tenta alterar uma nota",
                        "response": ["negar a alteração"],
                        "timing": None,
                        "concept_refs": ["ENT-001", "ENT-002", "TERM-001"],
                        "acceptance_refs": ["AC-002"],
                        "invariant_refs": ["INV-001"],
                        "formalization_refs": [],
                    },
                ],
                "constraints": [],
                "formalizations": [],
                "open_questions": [],
                "coverage_exceptions": [],
            }
        )
        return value

    def test_depth_is_proportional(self) -> None:
        self.assertEqual(recommend_semantic_depth(semantic_required=False), "none")
        self.assertEqual(recommend_semantic_depth(semantic_required=True), "scenario")
        self.assertEqual(
            recommend_semantic_depth(
                semantic_required=True,
                system_level="multi-user-system",
                roles_or_permissions=True,
            ),
            "domain",
        )
        self.assertEqual(
            recommend_semantic_depth(
                semantic_required=True,
                risk="high",
                concurrency_or_distribution=True,
            ),
            "formal",
        )

    def test_valid_domain_assurance_passes(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec = self.spec()
        write_spec(root, spec)
        assurance = self.assurance(spec)
        write_assurance(root, assurance)
        errors, warnings = validate_assurance(root)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertTrue(analyze_assurance(root)["ready"])

    def test_must_criterion_needs_requirement_origin(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec = self.spec()
        write_spec(root, spec)
        assurance = self.assurance(spec)
        assurance["requirements"] = assurance["requirements"][:1]
        write_assurance(root, assurance)
        errors, _ = validate_assurance(root)
        self.assertTrue(any("AC-002" in error and "origin" in error for error in errors))

    def test_impossible_constraints_and_conflicting_dependencies_fail(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec = self.spec()
        write_spec(root, spec)
        assurance = self.assurance(spec)
        assurance["constraints"] = [
            {"id": "CON-001", "kind": "range", "subject": "nota", "field": "valor", "min": 10, "max": 0},
            {"id": "CON-002", "kind": "requires", "source": "REQ-001", "target": "REQ-002"},
            {"id": "CON-003", "kind": "forbids", "source": "REQ-001", "target": "REQ-002"},
        ]
        write_assurance(root, assurance)
        errors, _ = validate_assurance(root)
        self.assertTrue(any("impossible range" in error for error in errors))
        self.assertTrue(any("simultaneously required" in error for error in errors))

    def test_blocking_question_prevents_ready_state(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec = self.spec()
        write_spec(root, spec)
        assurance = self.assurance(spec)
        assurance["open_questions"] = [
            {
                "id": "Q-001",
                "severity": "blocking",
                "text": "Qual etapa letiva controla o lançamento?",
                "requirement_refs": ["REQ-001"],
            }
        ]
        write_assurance(root, assurance)
        report = analyze_assurance(root)
        self.assertFalse(report["ready"])
        self.assertTrue(any("Q-001" in error for error in report["errors"]))

    def test_assurance_becomes_stale_when_contract_changes(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec = self.spec()
        write_spec(root, spec)
        write_assurance(root, self.assurance(spec))
        changed = json.loads(json.dumps(spec))
        changed["goal"] = "Controlar lançamento e revisão de notas por professor e turma."
        write_spec(root, changed)
        errors, _ = validate_assurance(root)
        self.assertTrue(any("stale" in error for error in errors))

    def test_coverage_distinguishes_traceability_from_correctness(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec = self.spec()
        write_spec(root, spec)
        assurance = self.assurance(spec)
        write_assurance(root, assurance)
        plan = create_verification_plan(spec)
        for row in plan["criteria"]:
            row["evidence"] = [
                {"kind": "test", "ref": "tests/test_app.py", "gate": "python:scripts/validate_factory.py"}
            ]
        write_verification_plan(root, plan)
        coverage = coverage_report(root)
        self.assertEqual(coverage["must_requirements"]["with_acceptance_refs"], 2)
        self.assertEqual(coverage["must_acceptance_criteria"]["with_requirement_origin"], 2)
        self.assertEqual(coverage["must_acceptance_criteria"]["with_executable_gate"], 2)
        self.assertIn("does not prove semantic correctness", coverage["note"])

    def test_semantic_diff_propagates_to_acceptance_invariant_and_gate(self) -> None:
        spec = self.spec()
        old = self.assurance(spec)
        new = json.loads(json.dumps(old))
        new["requirements"][0]["response"] = ["persistir a nota e registrar autoria"]
        plan = {
            "criteria": [
                {
                    "id": "AC-001",
                    "evidence": [
                        {"kind": "test", "ref": "tests/test_app.py", "gate": "npm:test"}
                    ],
                }
            ]
        }
        diff = semantic_diff(old, new, verification_plan=plan)
        self.assertTrue(diff["changed"])
        self.assertIn("REQ-001", diff["impact"]["requirements"])
        self.assertIn("AC-001", diff["impact"]["acceptance_criteria"])
        self.assertIn("INV-001", diff["impact"]["invariants"])
        self.assertIn("npm:test", diff["impact"]["gates"])


if __name__ == "__main__":
    unittest.main()
