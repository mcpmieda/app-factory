from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import engine.learning_engine as learning
from engine.execution_engine import record_execution_attempt, route_action
from engine.learning_engine import (
    aggregate_context,
    learning_status,
    read_learning_state,
    recommend_backend,
    record_learning_event,
)


VERIFY_CAPS = ["deterministic_commands", "test"]
IMPLEMENT_CAPS = ["reasoning", "repo_read", "repo_write"]


class LearningEngineTests(unittest.TestCase):
    def make_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        return temp, Path(temp.name)

    def add_samples(
        self,
        root: Path,
        *,
        action: str,
        capabilities: list[str],
        backend: str,
        outcomes: list[str],
        duration_ms: int = 1000,
    ) -> None:
        for outcome in outcomes:
            record_learning_event(
                root,
                action=action,
                capabilities=capabilities,
                backend=backend,
                outcome=outcome,
                duration_ms=duration_ms,
            )

    def test_learning_file_persists_only_allowlisted_metadata(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        secret_phrase = "Guilherme aluno segredo prompt completo"
        record_learning_event(
            root,
            action=secret_phrase,
            capabilities=["test"],
            backend="github_ci",
            outcome="success",
            duration_ms=120,
        )
        state = read_learning_state(root)
        event = state["events"][0]
        self.assertEqual(
            set(event),
            {"at", "context", "action", "capabilities", "backend", "outcome", "duration_ms"},
        )
        self.assertEqual(event["action"], "other")
        raw = (root / ".factory" / "learning.json").read_text(encoding="utf-8")
        self.assertNotIn(secret_phrase, raw)
        self.assertNotIn("Guilherme", raw)
        self.assertNotIn("prompt completo", raw)

    def test_unknown_capability_is_rejected_before_persistence(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        with self.assertRaisesRegex(ValueError, "unsupported learning capabilities"):
            record_learning_event(
                root,
                action="verify",
                capabilities=["test", "nome-do-aluno"],
                backend="github_ci",
                outcome="success",
            )
        self.assertFalse((root / ".factory" / "learning.json").exists())

    def test_tampered_learning_file_is_sanitized_on_read(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        factory = root / ".factory"
        factory.mkdir()
        secret = "NOME-PESSOAL-PROMPT-SECRETO"
        (factory / "learning.json").write_text(
            json.dumps(
                {
                    "schema_version": 999,
                    "secret_top_level": secret,
                    "events": [
                        {
                            "at": learning.utc_now(),
                            "action": secret,
                            "capabilities": ["test"],
                            "backend": "github_ci",
                            "outcome": "success",
                            "duration_ms": 100,
                            "raw_prompt": secret,
                        },
                        {
                            "at": learning.utc_now(),
                            "action": "verify",
                            "capabilities": ["test"],
                            "backend": secret,
                            "outcome": "success",
                            "duration_ms": 1,
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )
        state = read_learning_state(root)
        self.assertEqual(state["schema_version"], 1)
        self.assertEqual(len(state["events"]), 1)
        self.assertEqual(state["events"][0]["action"], "other")
        self.assertNotIn(secret, json.dumps(state))
        self.assertNotIn("raw_prompt", json.dumps(state))
        self.assertNotIn(secret, json.dumps(learning_status(root)))

    def test_dataset_is_bounded(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        with patch.object(learning, "EVENT_LIMIT", 10):
            for _ in range(14):
                record_learning_event(
                    root,
                    action="verify",
                    capabilities=VERIFY_CAPS,
                    backend="github_ci",
                    outcome="success",
                )
            self.assertEqual(len(read_learning_state(root)["events"]), 10)

    def test_insufficient_data_preserves_baseline(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        self.add_samples(
            root,
            action="verify",
            capabilities=VERIFY_CAPS,
            backend="github_ci",
            outcomes=["failure"] * 4,
        )
        self.add_samples(
            root,
            action="verify",
            capabilities=VERIFY_CAPS,
            backend="sandbox",
            outcomes=["success"] * 4,
        )
        recommendation = recommend_backend(
            root,
            action="verify",
            capabilities=VERIFY_CAPS,
            eligible_backends=["github_ci", "sandbox"],
            baseline_backend="github_ci",
        )
        self.assertEqual(recommendation["mode"], "insufficient-data")
        self.assertEqual(recommendation["backend"], "github_ci")
        decision = route_action(root, "verify", available_backends=["github_ci", "sandbox"])
        self.assertEqual(decision.backend_id, "github_ci")
        self.assertEqual(decision.selection_mode, "baseline")

    def test_sufficient_evidence_can_prefer_capable_lightweight_backend(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        self.add_samples(
            root,
            action="verify",
            capabilities=VERIFY_CAPS,
            backend="github_ci",
            outcomes=["failure"] * 5,
            duration_ms=5000,
        )
        self.add_samples(
            root,
            action="verify",
            capabilities=VERIFY_CAPS,
            backend="sandbox",
            outcomes=["success"] * 5,
            duration_ms=1000,
        )
        decision = route_action(
            root,
            "verify",
            available_backends=["github_ci", "sandbox", "local_full"],
        )
        self.assertEqual(decision.backend_id, "sandbox")
        self.assertEqual(decision.selection_mode, "learned")
        self.assertEqual(decision.learning["mode"], "learned")
        self.assertEqual(decision.learning["signal"], "success-rate")

    def test_incapable_backend_cannot_be_resurrected_by_artificial_learning(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        caps = ["deterministic_commands", "test", "live_migration"]
        self.add_samples(
            root,
            action="verify",
            capabilities=caps,
            backend="sandbox",
            outcomes=["success"] * 20,
        )
        self.add_samples(
            root,
            action="verify",
            capabilities=caps,
            backend="local_full",
            outcomes=["failure"] * 5,
        )
        decision = route_action(
            root,
            "verify",
            available_backends=["sandbox", "local_full"],
            live_migration=True,
        )
        self.assertEqual(decision.backend_id, "local_full")
        self.assertIn("missing:live_migration", decision.rejected["sandbox"])
        self.assertEqual(decision.selection_mode, "baseline")

    def test_local_full_is_never_learning_promoted_over_capable_light_backend(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        self.add_samples(
            root,
            action="implement",
            capabilities=IMPLEMENT_CAPS,
            backend="current_agent",
            outcomes=["failure"] * 5,
        )
        self.add_samples(
            root,
            action="implement",
            capabilities=IMPLEMENT_CAPS,
            backend="local_full",
            outcomes=["success"] * 20,
        )
        decision = route_action(root, "implement", available_backends=["current_agent", "local_full"])
        self.assertEqual(decision.backend_id, "current_agent")
        self.assertEqual(decision.selection_mode, "baseline")
        self.assertNotEqual((decision.learning or {}).get("backend"), "local_full")

    def test_current_task_failure_threshold_beats_historical_learning(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        self.add_samples(
            root,
            action="verify",
            capabilities=VERIFY_CAPS,
            backend="github_ci",
            outcomes=["success"] * 20,
        )
        self.add_samples(
            root,
            action="verify",
            capabilities=VERIFY_CAPS,
            backend="sandbox",
            outcomes=["failure"] * 5,
        )
        for _ in range(2):
            record_execution_attempt(
                root,
                action="verify",
                backend_id="github_ci",
                required_capabilities=VERIFY_CAPS,
                outcome="failure",
                task_key="task-current",
            )
        decision = route_action(
            root,
            "verify",
            available_backends=["github_ci", "sandbox", "local_full"],
            task_key="task-current",
        )
        self.assertNotEqual(decision.backend_id, "github_ci")
        self.assertEqual(decision.rejected["github_ci"], ["failure-threshold-reached"])

    def test_new_task_is_not_contaminated_by_previous_task_failures(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        for _ in range(2):
            record_execution_attempt(
                root,
                action="verify",
                backend_id="github_ci",
                required_capabilities=VERIFY_CAPS,
                outcome="failure",
                task_key="old-task",
            )
        decision = route_action(
            root,
            "verify",
            available_backends=["github_ci", "sandbox"],
            task_key="new-task",
        )
        self.assertEqual(decision.backend_id, "github_ci")

    def test_duration_can_break_high_confidence_near_tie(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        self.add_samples(
            root,
            action="verify",
            capabilities=VERIFY_CAPS,
            backend="github_ci",
            outcomes=["success"] * 12,
            duration_ms=4000,
        )
        self.add_samples(
            root,
            action="verify",
            capabilities=VERIFY_CAPS,
            backend="sandbox",
            outcomes=["success"] * 12,
            duration_ms=1000,
        )
        recommendation = recommend_backend(
            root,
            action="verify",
            capabilities=VERIFY_CAPS,
            eligible_backends=["github_ci", "sandbox"],
            baseline_backend="github_ci",
        )
        self.assertEqual(recommendation["mode"], "learned")
        self.assertEqual(recommendation["backend"], "sandbox")
        self.assertEqual(recommendation["signal"], "duration")

    def test_failure_duration_does_not_make_backend_look_faster(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        for _ in range(5):
            record_learning_event(
                root,
                action="verify",
                capabilities=VERIFY_CAPS,
                backend="github_ci",
                outcome="success",
                duration_ms=4000,
            )
            record_learning_event(
                root,
                action="verify",
                capabilities=VERIFY_CAPS,
                backend="github_ci",
                outcome="failure",
                duration_ms=1,
            )
        stats = aggregate_context(root, action="verify", capabilities=VERIFY_CAPS)["github_ci"]
        self.assertEqual(stats["median_success_duration_ms"], 4000)

    def test_blocked_and_cancelled_do_not_inflate_resolved_samples(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        self.add_samples(
            root,
            action="verify",
            capabilities=VERIFY_CAPS,
            backend="github_ci",
            outcomes=["success", "failure", "blocked", "cancelled"],
        )
        stats = aggregate_context(root, action="verify", capabilities=VERIFY_CAPS)["github_ci"]
        self.assertEqual(stats["resolved_samples"], 2)
        self.assertEqual(stats["blocked"], 1)
        self.assertEqual(stats["cancelled"], 1)

    def test_learning_survives_fresh_reader_session(self) -> None:
        temp, root = self.make_root()
        self.addCleanup(temp.cleanup)
        record_learning_event(
            root,
            action="verify",
            capabilities=VERIFY_CAPS,
            backend="github_ci",
            outcome="success",
            duration_ms=222,
        )
        status = learning_status(root)
        self.assertEqual(status["events"], 1)
        self.assertTrue(status["local_only"])
        self.assertFalse(status["external_telemetry"])
        reloaded = json.loads((root / ".factory" / "learning.json").read_text(encoding="utf-8"))
        self.assertEqual(reloaded["events"][0]["duration_ms"], 222)


if __name__ == "__main__":
    unittest.main()
