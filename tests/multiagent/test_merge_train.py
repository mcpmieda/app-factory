from __future__ import annotations

import unittest

from engine.merge_train import (
    FinalPullRequestCandidate,
    WorkerMergeCandidate,
    evaluate_final_gate,
    evaluate_worker_merge,
)

SHA = "a" * 40


class MergeTrainTests(unittest.TestCase):
    def candidate(self, **overrides):
        value = {
            "task_id": "worker-a",
            "pull_request_number": 10,
            "base_branch": "factory/run",
            "head_branch": "factory/run/worker-a",
            "head_sha": SHA,
            "changed_paths": ("docs/a/result.md",),
            "declared_paths": ("docs/a",),
            "ci_event": "workflow_dispatch",
            "ci_head_sha": SHA,
            "ci_conclusion": "success",
            "review_conclusions": {"CodeRabbit": "success", "Semgrep": "success", "Sonar": "success"},
            "review_head_shas": {"CodeRabbit": SHA, "Semgrep": SHA, "Sonar": SHA},
            "blocking_review": False,
        }
        value.update(overrides)
        return WorkerMergeCandidate(**value)

    def test_worker_merge_is_allowed_only_into_integration_after_exact_ci_and_reviews(self) -> None:
        decision = evaluate_worker_merge(
            self.candidate(),
            integration_branch="factory/run",
            target_branch="main",
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.destination_branch, "factory/run")
        self.assertFalse(decision.auto_merge_target)

    def test_worker_merge_rejects_wrong_event_sha_target_scope_and_missing_review(self) -> None:
        decision = evaluate_worker_merge(
            self.candidate(
                base_branch="main",
                ci_event="pull_request",
                ci_head_sha="b" * 40,
                changed_paths=(".github/workflows/bad.yml",),
                review_conclusions={"CodeRabbit": "success", "Semgrep": "failure"},
            ),
            integration_branch="factory/run",
            target_branch="main",
        )
        self.assertFalse(decision.allowed)
        joined = " ".join(decision.reasons)
        self.assertIn("workflow_dispatch", joined)
        self.assertIn("exactly match", joined)
        self.assertIn("protected path", joined)
        self.assertIn("Sonar=missing", joined)
        self.assertIn("target", joined)

    def test_final_pr_must_be_draft_and_is_never_auto_merged(self) -> None:
        decision = evaluate_final_gate(
            FinalPullRequestCandidate(
                head_branch="factory/run",
                base_branch="main",
                draft=True,
                integration_head_sha=SHA,
                integration_ci_event="workflow_dispatch",
                integration_ci_head_sha=SHA,
                integration_ci_conclusion="success",
            ),
            integration_branch="factory/run",
            target_branch="main",
        )
        self.assertTrue(decision.ready_for_human_review)
        self.assertTrue(decision.draft_required)
        self.assertFalse(decision.auto_merge_allowed)

    def test_non_draft_final_pr_is_not_ready(self) -> None:
        decision = evaluate_final_gate(
            FinalPullRequestCandidate(
                head_branch="factory/run",
                base_branch="main",
                draft=False,
                integration_head_sha=SHA,
                integration_ci_event="workflow_dispatch",
                integration_ci_head_sha=SHA,
                integration_ci_conclusion="success",
            ),
            integration_branch="factory/run",
            target_branch="main",
        )
        self.assertFalse(decision.ready_for_human_review)
        self.assertFalse(decision.auto_merge_allowed)


if __name__ == "__main__":
    unittest.main()
