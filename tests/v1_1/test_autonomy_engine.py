from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine.autonomy_engine import (
    init_project,
    next_action,
    read_state,
    record_event,
    resume_project,
)


class AutonomyEngineTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "PROJECT_STATE.md").write_text(
            "# PROJECT_STATE\n\n## Objetivo atual\n\nConstruir um cadastro escolar simples e confiável.\n",
            encoding="utf-8",
        )
        (root / "app.py").write_text("def main():\n    return 1\n", encoding="utf-8")
        return temp, root

    def test_state_machine_reaches_delivery_after_verification_and_review(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        state = init_project(root, goal="Criar cadastro")
        self.assertEqual(state["phase"], "planning")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "plan")

        record_event(root, "plan-ready", "Fatia cadastro")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "implement")
        record_event(root, "implementation-ready", "Cadastro implementado")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "verify")
        record_event(root, "verification-pass", "tests green")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "review")
        record_event(root, "review-pass", "diff aprovado")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "deliver")
        record_event(root, "delivered", "merged")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "done")

    def test_repair_loop_stops_after_configured_limit(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        init_project(root, goal="Corrigir bug", max_repairs=3)
        record_event(root, "plan-ready")
        record_event(root, "implementation-ready")
        record_event(root, "verification-fail", "fail 1")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "repair")
        record_event(root, "repair-ready")
        record_event(root, "verification-fail", "fail 2")
        record_event(root, "repair-ready")
        record_event(root, "verification-fail", "fail 3")
        action = next_action(root, auto_refresh=False)[0]
        self.assertEqual(action["action"], "resolve_blocker")
        self.assertFalse(action["requires_human"])
        self.assertEqual(read_state(root)["repair_attempts"], 3)

    def test_resume_infers_goal_without_conversation_history(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        result = resume_project(root)
        self.assertIn("cadastro escolar", result.state["goal"])
        self.assertEqual(result.action["action"], "plan")
        self.assertTrue((root / ".factory/state.json").is_file())
        self.assertTrue((root / ".factory/context/repo-map.json").is_file())

    def test_external_repo_change_forces_context_reconciliation(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        init_project(root, goal="Continuar")
        record_event(root, "plan-ready")
        self.assertEqual(read_state(root)["phase"], "implementation")
        (root / "app.py").write_text("def main():\n    return 2\n", encoding="utf-8")
        result = resume_project(root)
        self.assertEqual(result.action["action"], "reconcile_context")
        self.assertIn("app.py", result.action["delta"]["changed"])
        record_event(root, "context-reconciled", "delta revisado")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "implement")

    def test_repeated_resume_preserves_pending_context_delta(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        init_project(root, goal="Continuar sem perder contexto")
        record_event(root, "plan-ready")
        (root / "app.py").write_text("def main():\n    return 3\n", encoding="utf-8")

        first = resume_project(root)
        self.assertIn("app.py", first.action["delta"]["changed"])
        second = resume_project(root)
        self.assertEqual(second.action["action"], "reconcile_context")
        self.assertIn("app.py", second.action["delta"]["changed"])

        record_event(root, "context-reconciled", "delta preservado e revisado")
        self.assertEqual(next_action(root, auto_refresh=False)[0]["action"], "implement")

    def test_human_intervention_is_explicit_and_categorized(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        init_project(root, goal="Publicar")
        record_event(root, "human-needed", "Definir orçamento mensal", category="cost")
        action = next_action(root, auto_refresh=False)[0]
        self.assertEqual(action["action"], "request_human")
        self.assertTrue(action["requires_human"])
        self.assertEqual(read_state(root)["human_needed"]["category"], "cost")

    def test_invalid_event_order_is_rejected_without_state_corruption(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        before = init_project(root, goal="Entregar com segurança")
        history_size = len(before["history"])

        with self.assertRaisesRegex(ValueError, "not allowed"):
            record_event(root, "delivered", "não deveria aceitar")

        after = read_state(root)
        self.assertEqual(after["phase"], "planning")
        self.assertEqual(after["status"], "active")
        self.assertEqual(len(after["history"]), history_size)
        self.assertNotIn("delivered", [item["event"] for item in after["history"]])


if __name__ == "__main__":
    unittest.main()
