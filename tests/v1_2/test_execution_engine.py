from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine.execution_engine import (
    record_execution_attempt,
    request_for_action,
    route_action,
    route_execution,
)


class ExecutionEngineTests(unittest.TestCase):
    def make_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        return temp, root

    def test_current_agent_wins_when_it_has_every_required_capability(self) -> None:
        request = request_for_action("implement")
        decision = route_execution(request, available_backends=["current_agent", "github_ci", "local_full"])
        self.assertEqual(decision.backend_id, "current_agent")

    def test_ci_is_selected_for_deterministic_verification(self) -> None:
        request = request_for_action("verify")
        decision = route_execution(request, available_backends=["current_agent", "github_ci", "local_full"])
        self.assertEqual(decision.backend_id, "github_ci")
        self.assertIn("missing:deterministic_commands", decision.rejected["current_agent"])

    def test_headless_browser_stays_on_ci_when_available(self) -> None:
        request = request_for_action("verify", headless_browser=True)
        decision = route_execution(request, available_backends=["current_agent", "github_ci", "local_full"])
        self.assertEqual(decision.backend_id, "github_ci")

    def test_interactive_browser_requires_full_local_backend(self) -> None:
        request = request_for_action("verify", interactive_browser=True)
        decision = route_execution(request, available_backends=["current_agent", "github_ci", "local_full"])
        self.assertEqual(decision.backend_id, "local_full")
        self.assertIn("missing:interactive_browser", decision.rejected["github_ci"])

    def test_backend_without_capability_is_never_selected(self) -> None:
        request = request_for_action("verify", live_migration=True)
        decision = route_execution(request, available_backends=["current_agent", "github_ci"])
        self.assertIsNone(decision.backend_id)
        self.assertIn("missing:live_migration", decision.rejected["github_ci"])

    def test_repeated_ci_failures_escalate_to_available_sandbox(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        for index in range(2):
            record_execution_attempt(
                root,
                action="verify",
                backend_id="github_ci",
                required_capabilities=["deterministic_commands", "test"],
                outcome="failure",
                summary=f"failure {index + 1}",
            )
        decision = route_action(
            root,
            "verify",
            available_backends=["current_agent", "github_ci", "sandbox", "local_full"],
        )
        self.assertEqual(decision.backend_id, "sandbox")
        self.assertEqual(decision.rejected["github_ci"], ["failure-threshold-reached"])

    def test_recent_failures_still_escalate_when_older_success_exists(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        for outcome in ("success", "failure", "failure"):
            record_execution_attempt(
                root,
                action="verify",
                backend_id="github_ci",
                required_capabilities=["deterministic_commands", "test"],
                outcome=outcome,
            )
        decision = route_action(root, "verify", available_backends=["current_agent", "github_ci", "sandbox"])
        self.assertEqual(decision.backend_id, "sandbox")
        self.assertEqual(decision.rejected["github_ci"], ["failure-threshold-reached"])

    def test_success_resets_failure_escalation_for_backend(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        for outcome in ("failure", "failure", "success"):
            record_execution_attempt(
                root,
                action="verify",
                backend_id="github_ci",
                required_capabilities=["deterministic_commands", "test"],
                outcome=outcome,
            )
        decision = route_action(root, "verify", available_backends=["current_agent", "github_ci", "sandbox"])
        self.assertEqual(decision.backend_id, "github_ci")

    def test_old_task_failures_do_not_penalize_new_task(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        for _ in range(2):
            record_execution_attempt(
                root,
                task_key="task-old",
                action="verify",
                backend_id="github_ci",
                required_capabilities=["deterministic_commands", "test"],
                outcome="failure",
            )
        old_decision = route_action(
            root,
            "verify",
            task_key="task-old",
            available_backends=["current_agent", "github_ci", "sandbox"],
        )
        new_decision = route_action(
            root,
            "verify",
            task_key="task-new",
            available_backends=["current_agent", "github_ci", "sandbox"],
        )
        self.assertEqual(old_decision.backend_id, "sandbox")
        self.assertEqual(new_decision.backend_id, "github_ci")

    def test_execution_history_does_not_persist_raw_multiline_logs(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        state = record_execution_attempt(
            root,
            action="verify",
            backend_id="github_ci",
            required_capabilities=["test"],
            outcome="failure",
            summary="line one\nline two\n" + ("x" * 1000),
        )
        summary = state["attempts"][-1]["summary"]
        self.assertNotIn("\n", summary)
        self.assertLessEqual(len(summary), 500)


if __name__ == "__main__":
    unittest.main()
