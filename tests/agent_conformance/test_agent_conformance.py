from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("agent_conformance", ROOT / "scripts" / "agent_conformance.py")
assert SPEC and SPEC.loader
agent_conformance = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(agent_conformance)


class AgentConformanceTests(unittest.TestCase):
    def case(self, case_id: str):
        return agent_conformance.load_cases(case_id)[0]

    def test_reference_corpus_passes(self) -> None:
        for case in agent_conformance.load_cases():
            result = agent_conformance.run_reference_case(case)
            self.assertTrue(result["pass"], msg=json.dumps(result, indent=2, ensure_ascii=False))

    def test_empty_files_do_not_fake_functional_conformance(self) -> None:
        case = self.case("functional-spec-and-plan")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "specs").mkdir()
            (root / "specs" / "semantic-contract.json").write_text("{}\n", encoding="utf-8")
            (root / "specs" / "verification-plan.json").write_text("{}\n", encoding="utf-8")
            result = agent_conformance.score_workspace(case, root)
            self.assertFalse(result["pass"])
            self.assertTrue(any(check["kind"] == "semantic_spec_valid" and not check["pass"] for check in result["checks"]))

    def test_plan_presence_without_executable_evidence_fails(self) -> None:
        case = self.case("functional-spec-and-plan")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            actions = case["reference_actions"]
            for action in actions:
                if action["kind"] in {"attach_evidence"}:
                    break
                agent_conformance.execute_reference_action(root, action)
            result = agent_conformance.score_workspace(case, root)
            self.assertFalse(result["pass"])
            self.assertTrue(any(check["kind"] == "verification_plan_valid" and not check["pass"] for check in result["checks"]))

    def test_docs_case_rejects_unnecessary_semantic_contract(self) -> None:
        case = self.case("docs-change-stays-light")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for action in case["reference_actions"]:
                agent_conformance.execute_reference_action(root, action)
            (root / "specs").mkdir(exist_ok=True)
            (root / "specs" / "semantic-contract.json").write_text("{}\n", encoding="utf-8")
            result = agent_conformance.score_workspace(case, root)
            self.assertFalse(result["pass"])
            self.assertTrue(any(check["kind"] == "file_absent" and not check["pass"] for check in result["checks"]))

    def test_case_audit_rejects_path_traversal(self) -> None:
        case = {
            "schema_version": 1,
            "id": "bad-case",
            "prompt": "Uma tarefa válida o bastante para testar path traversal.",
            "reference_actions": [{"kind": "write_text", "path": "../escape", "content": "x"}],
            "assertions": [{"kind": "text_contains", "path": "README.md", "text": "x"}],
        }
        errors = agent_conformance.validate_case(case)
        self.assertTrue(any("unsafe relative path" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
