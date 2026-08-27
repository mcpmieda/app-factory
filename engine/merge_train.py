from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engine.provider_runtime import SHA_PATTERN, validate_branch_name, validate_changed_paths

REQUIRED_AUTOMATED_REVIEWS = ("CodeRabbit", "Semgrep", "Sonar")
SUCCESS_CONCLUSIONS = frozenset({"success"})


@dataclass(frozen=True)
class WorkerMergeCandidate:
    task_id: str
    pull_request_number: int
    base_branch: str
    head_branch: str
    head_sha: str
    changed_paths: tuple[str, ...]
    declared_paths: tuple[str, ...]
    ci_event: str
    ci_head_sha: str
    ci_conclusion: str
    review_conclusions: Mapping[str, str] = field(default_factory=dict)
    review_head_shas: Mapping[str, str] = field(default_factory=dict)
    blocking_review: bool = False


@dataclass(frozen=True)
class MergeDecision:
    allowed: bool
    destination_branch: str | None
    reasons: tuple[str, ...]
    auto_merge_target: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "destination_branch": self.destination_branch,
            "reasons": list(self.reasons),
            "auto_merge_target": self.auto_merge_target,
        }


def evaluate_worker_merge(
    candidate: WorkerMergeCandidate,
    *,
    integration_branch: str,
    target_branch: str,
    required_reviews: tuple[str, ...] = REQUIRED_AUTOMATED_REVIEWS,
) -> MergeDecision:
    integration = validate_branch_name(integration_branch, label="integration branch")
    target = validate_branch_name(target_branch, label="target branch")
    reasons: list[str] = []

    if integration == target:
        reasons.append("integration branch must differ from target branch")
    if candidate.base_branch != integration:
        reasons.append("worker PR base must be the isolated integration branch")
    if candidate.base_branch == target:
        reasons.append("automatic worker merge to target is forbidden")
    if candidate.head_branch in {integration, target}:
        reasons.append("worker PR head must be a dedicated worker branch")
    if not SHA_PATTERN.fullmatch(candidate.head_sha):
        reasons.append("worker head SHA is invalid")
    if candidate.ci_event != "workflow_dispatch":
        reasons.append("worker CI must come from workflow_dispatch")
    if candidate.ci_head_sha != candidate.head_sha:
        reasons.append("worker CI head SHA must exactly match the current PR head")
    if candidate.ci_conclusion != "success":
        reasons.append("worker CI is not successful")
    try:
        validate_changed_paths(candidate.changed_paths, candidate.declared_paths)
    except ValueError as error:
        reasons.append(str(error))
    if candidate.blocking_review:
        reasons.append("a valid blocking review is unresolved")
    for context in required_reviews:
        conclusion = str(candidate.review_conclusions.get(context) or "missing").lower()
        if conclusion not in SUCCESS_CONCLUSIONS:
            reasons.append(f"required automated review is not green: {context}={conclusion}")
        review_sha = str(candidate.review_head_shas.get(context) or "")
        if review_sha != candidate.head_sha:
            reasons.append(f"required automated review is stale or missing SHA evidence: {context}")

    return MergeDecision(
        allowed=not reasons,
        destination_branch=integration if not reasons else None,
        reasons=tuple(reasons) or ("worker is eligible for squash merge into the integration branch only",),
        auto_merge_target=False,
    )


@dataclass(frozen=True)
class FinalPullRequestCandidate:
    head_branch: str
    base_branch: str
    draft: bool
    integration_head_sha: str
    integration_ci_event: str
    integration_ci_head_sha: str
    integration_ci_conclusion: str


@dataclass(frozen=True)
class FinalGateDecision:
    ready_for_human_review: bool
    draft_required: bool
    auto_merge_allowed: bool
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ready_for_human_review": self.ready_for_human_review,
            "draft_required": self.draft_required,
            "auto_merge_allowed": self.auto_merge_allowed,
            "reasons": list(self.reasons),
        }


def evaluate_final_gate(
    candidate: FinalPullRequestCandidate,
    *,
    integration_branch: str,
    target_branch: str,
) -> FinalGateDecision:
    integration = validate_branch_name(integration_branch, label="integration branch")
    target = validate_branch_name(target_branch, label="target branch")
    reasons: list[str] = []
    if integration == target:
        reasons.append("integration branch must differ from target branch")
    if candidate.head_branch != integration:
        reasons.append("final PR head must be the isolated integration branch")
    if candidate.base_branch != target:
        reasons.append("final PR base must be the human-controlled target branch")
    if not candidate.draft:
        reasons.append("final PR must remain draft until human review")
    if not SHA_PATTERN.fullmatch(candidate.integration_head_sha):
        reasons.append("integration head SHA is invalid")
    if candidate.integration_ci_event != "workflow_dispatch":
        reasons.append("integration CI must come from workflow_dispatch")
    if candidate.integration_ci_head_sha != candidate.integration_head_sha:
        reasons.append("integration CI head SHA must exactly match the integration head")
    if candidate.integration_ci_conclusion != "success":
        reasons.append("integration CI is not successful")
    return FinalGateDecision(
        ready_for_human_review=not reasons,
        draft_required=True,
        auto_merge_allowed=False,
        reasons=tuple(reasons) or ("final draft PR is ready for human review; automatic target merge remains forbidden",),
    )
