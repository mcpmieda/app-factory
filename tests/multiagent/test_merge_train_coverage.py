from __future__ import annotations

import unittest

from engine.merge_train import (
    FinalPullRequestCandidate,
    MergeDecision,
    WorkerMergeCandidate,
    evaluate_final_gate,
    evaluate_worker_merge,
)

SHA = "a" * 40


class MergeTrainCoverageTests(unittest.TestCase):
    def worker(self, **overrides) -> WorkerMergeCandidate:
        raw = {
            "task_id": "worker",
            "pull_request_number": 1,
            "base_branch": "factory/run",
            "head_branch": "factory/run/worker",
            "head_sha": SHA,
            "changed_paths": ("docs/worker/result.md",),
            "declared_paths": ("docs/worker",),
            "ci_event": "workflow_dispatch",
            "ci_head_sha": SHA,
            "ci_conclusion": "success",
            "review_conclusions": {
                "CodeRabbit": "success",
                "Semgrep": "success",
                "Sonar": "success",
            },
            "review_head_shas": {
                "CodeRabbit": SHA,
                "Semgrep": SHA,
                "Sonar": SHA,
            },
            "blocking_review": False,
        }
        raw.update(overrides)
        return WorkerMergeCandidate(**raw)

    def final(self, **overrides) -> FinalPullRequestCandidate:
        raw = {
            "head_branch": "factory/run",
            "base_branch": "main",
            "draft": True,
            "integration_head_sha": SHA,
            "integration_ci_event": "workflow_dispatch",
            "integration_ci_head_sha": SHA,
            "integration_ci_conclusion": "success",
        }
        raw.update(overrides)
        return FinalPullRequestCandidate(**raw)

    def test_worker_decision_serialization_and_all_negative_gates(self) -> None:
        valid = evaluate_worker_merge(
            self.worker(), integration_branch="factory/run", target_branch="main"
        )
        payload = valid.to_dict()
        self.assertTrue(payload["allowed"])
        self.assertEqual(payload["destination_branch"], "factory/run")
        self.assertFalse(payload["auto_merge_target"])

        cases = (
            ({}, {"integration_branch": "main", "target_branch": "main"}, "must differ"),
            ({"base_branch": "factory/other"}, {}, "isolated integration branch"),
            ({"base_branch": "main"}, {}, "target is forbidden"),
            ({"head_branch": "factory/run"}, {}, "dedicated worker branch"),
            ({"head_branch": "main"}, {}, "dedicated worker branch"),
            ({"head_sha": "bad"}, {}, "head SHA is invalid"),
            ({"ci_event": "pull_request"}, {}, "workflow_dispatch"),
            ({"ci_head_sha": "b" * 40}, {}, "exactly match"),
            ({"ci_conclusion": "failure"}, {}, "not successful"),
            ({"changed_paths": ("src/escape.py",)}, {}, "outside declared scope"),
            ({"blocking_review": True}, {}, "blocking review"),
            ({"review_conclusions": {"CodeRabbit": "failure", "Semgrep": "success", "Sonar": "success"}}, {}, "CodeRabbit=failure"),
            ({"review_conclusions": {"CodeRabbit": "success", "Semgrep": "success"}}, {}, "Sonar=missing"),
            ({"review_head_shas": {"CodeRabbit": "b" * 40, "Semgrep": SHA, "Sonar": SHA}}, {}, "stale or missing SHA evidence: CodeRabbit"),
            ({"review_head_shas": {"CodeRabbit": SHA, "Semgrep": SHA}}, {}, "stale or missing SHA evidence: Sonar"),
        )
        for candidate_overrides, gate_overrides, message in cases:
            with self.subTest(message=message):
                integration_branch = gate_overrides.get("integration_branch", "factory/run")
                target_branch = gate_overrides.get("target_branch", "main")
                decision = evaluate_worker_merge(
                    self.worker(**candidate_overrides),
                    integration_branch=integration_branch,
                    target_branch=target_branch,
                )
                self.assertFalse(decision.allowed)
                self.assertIsNone(decision.destination_branch)
                self.assertIn(message, " ".join(decision.reasons))
                self.assertFalse(decision.auto_merge_target)

        custom = evaluate_worker_merge(
            self.worker(review_conclusions={"Custom": "success"}, review_head_shas={"Custom": SHA}),
            integration_branch="factory/run",
            target_branch="main",
            required_reviews=("Custom",),
        )
        self.assertTrue(custom.allowed)
        self.assertEqual(
            MergeDecision(False, None, ("why",), False).to_dict()["reasons"],
            ["why"],
        )

    def test_final_decision_serialization_and_all_negative_gates(self) -> None:
        valid = evaluate_final_gate(
            self.final(), integration_branch="factory/run", target_branch="main"
        )
        payload = valid.to_dict()
        self.assertTrue(payload["ready_for_human_review"])
        self.assertTrue(payload["draft_required"])
        self.assertFalse(payload["auto_merge_allowed"])

        cases = (
            ({}, {"integration_branch": "main", "target_branch": "main"}, "must differ"),
            ({"head_branch": "factory/other"}, {}, "head must be"),
            ({"base_branch": "other"}, {}, "base must be"),
            ({"draft": False}, {}, "must remain draft"),
            ({"integration_head_sha": "bad"}, {}, "head SHA is invalid"),
            ({"integration_ci_event": "pull_request"}, {}, "workflow_dispatch"),
            ({"integration_ci_head_sha": "b" * 40}, {}, "exactly match"),
            ({"integration_ci_conclusion": "failure"}, {}, "not successful"),
        )
        for candidate_overrides, gate_overrides, message in cases:
            with self.subTest(message=message):
                decision = evaluate_final_gate(
                    self.final(**candidate_overrides),
                    integration_branch=gate_overrides.get("integration_branch", "factory/run"),
                    target_branch=gate_overrides.get("target_branch", "main"),
                )
                self.assertFalse(decision.ready_for_human_review)
                self.assertTrue(decision.draft_required)
                self.assertFalse(decision.auto_merge_allowed)
                self.assertIn(message, " ".join(decision.reasons))


if __name__ == "__main__":
    unittest.main()
