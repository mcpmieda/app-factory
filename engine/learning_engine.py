from __future__ import annotations

import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

LEARNING_SCHEMA_VERSION = 1
EVENT_LIMIT = 500
DEFAULT_MIN_SAMPLES = 5
DEFAULT_MIN_SCORE_MARGIN = 0.10
DURATION_TIE_SCORE_DELTA = 0.03
DURATION_IMPROVEMENT_RATIO = 0.75
BETA_SUCCESS_PRIOR = 2
BETA_FAILURE_PRIOR = 2
ALLOWED_OUTCOMES = {"success", "failure", "blocked", "cancelled"}
PROTECTED_HEAVY_BACKENDS = {"local_full"}
SAFE_BACKENDS = {"current_agent", "github_ci", "sandbox", "local_full"}
SAFE_ACTIONS = {
    "plan",
    "reconcile_context",
    "implement",
    "verify",
    "repair",
    "review",
    "deliver",
    "resolve_blocker",
    "request_human",
    "done",
    "inspect_state",
}
SAFE_CAPABILITIES = {
    "reasoning",
    "repo_read",
    "repo_write",
    "github_api",
    "review",
    "deterministic_commands",
    "build",
    "test",
    "headless_browser",
    "ephemeral_services",
    "interactive_shell",
    "interactive_browser",
    "local_services",
    "live_migration",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def learning_path(root: Path | str) -> Path:
    return Path(root).resolve() / ".factory" / "learning.json"


def normalize_action(action: str) -> str:
    """Classify action without persisting arbitrary/user-provided text."""
    compact = str(action).strip().lower().replace("-", "_")
    return compact if compact in SAFE_ACTIONS else "other"


def normalize_backend(backend: str) -> str:
    compact = str(backend).strip().lower()
    if compact not in SAFE_BACKENDS:
        raise ValueError(f"unsupported learning backend: {backend}")
    return compact


def normalize_capabilities(capabilities: Iterable[str]) -> tuple[str, ...]:
    result = tuple(sorted({str(value).strip().lower() for value in capabilities if str(value).strip()}))
    unknown = set(result) - SAFE_CAPABILITIES
    if unknown:
        raise ValueError(f"unsupported learning capabilities: {', '.join(sorted(unknown))}")
    return result


def context_key(action: str, capabilities: Iterable[str]) -> str:
    safe_action = normalize_action(action)
    safe_capabilities = normalize_capabilities(capabilities)
    return f"{safe_action}|{','.join(safe_capabilities)}"


def read_learning_state(root: Path | str) -> dict[str, Any]:
    path = learning_path(root)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        value = None
    if not isinstance(value, dict):
        return {"schema_version": LEARNING_SCHEMA_VERSION, "events": []}
    events = value.get("events")
    if not isinstance(events, list):
        value["events"] = []
    value["schema_version"] = LEARNING_SCHEMA_VERSION
    return value


def write_learning_state(root: Path | str, state: dict[str, Any]) -> None:
    path = learning_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def record_learning_event(
    root: Path | str,
    *,
    action: str,
    capabilities: Iterable[str],
    backend: str,
    outcome: str,
    duration_ms: int | None = None,
) -> dict[str, Any]:
    """Persist only allowlisted execution metadata; never prompts, code, logs, summaries or task text."""
    safe_outcome = str(outcome).strip().lower()
    if safe_outcome not in ALLOWED_OUTCOMES:
        raise ValueError(f"unsupported learning outcome: {outcome}")
    safe_action = normalize_action(action)
    safe_backend = normalize_backend(backend)
    safe_capabilities = normalize_capabilities(capabilities)
    event = {
        "at": utc_now(),
        "context": context_key(safe_action, safe_capabilities),
        "action": safe_action,
        "capabilities": list(safe_capabilities),
        "backend": safe_backend,
        "outcome": safe_outcome,
        "duration_ms": max(0, min(int(duration_ms), 86_400_000)) if duration_ms is not None else None,
    }
    state = read_learning_state(root)
    events = state.setdefault("events", [])
    events.append(event)
    if len(events) > EVENT_LIMIT:
        del events[:-EVENT_LIMIT]
    state["updated_at"] = utc_now()
    write_learning_state(root, state)
    return state


def posterior_success(successes: int, failures: int) -> float:
    return (successes + BETA_SUCCESS_PRIOR) / (
        successes + failures + BETA_SUCCESS_PRIOR + BETA_FAILURE_PRIOR
    )


def aggregate_context(
    root: Path | str,
    *,
    action: str,
    capabilities: Iterable[str],
) -> dict[str, dict[str, Any]]:
    key = context_key(action, capabilities)
    buckets: dict[str, dict[str, Any]] = {}
    for event in read_learning_state(root).get("events", []):
        if not isinstance(event, dict) or event.get("context") != key:
            continue
        backend = event.get("backend")
        if not isinstance(backend, str) or backend not in SAFE_BACKENDS:
            continue
        bucket = buckets.setdefault(
            backend,
            {"successes": 0, "failures": 0, "blocked": 0, "cancelled": 0, "durations_ms": []},
        )
        outcome = event.get("outcome")
        if outcome == "success":
            bucket["successes"] += 1
        elif outcome == "failure":
            bucket["failures"] += 1
        elif outcome == "blocked":
            bucket["blocked"] += 1
        elif outcome == "cancelled":
            bucket["cancelled"] += 1
        duration = event.get("duration_ms")
        if isinstance(duration, int) and duration >= 0 and outcome in {"success", "failure"}:
            bucket["durations_ms"].append(duration)

    result: dict[str, dict[str, Any]] = {}
    for backend, bucket in buckets.items():
        resolved = int(bucket["successes"]) + int(bucket["failures"])
        durations = list(bucket["durations_ms"])
        result[backend] = {
            "successes": int(bucket["successes"]),
            "failures": int(bucket["failures"]),
            "blocked": int(bucket["blocked"]),
            "cancelled": int(bucket["cancelled"]),
            "resolved_samples": resolved,
            "posterior_success": round(posterior_success(int(bucket["successes"]), int(bucket["failures"])), 6),
            "median_duration_ms": int(statistics.median(durations)) if durations else None,
        }
    return dict(sorted(result.items()))


def learning_status(root: Path | str) -> dict[str, Any]:
    state = read_learning_state(root)
    events = [event for event in state.get("events", []) if isinstance(event, dict)]
    contexts = sorted({str(event.get("context")) for event in events if event.get("context")})
    outcomes: dict[str, int] = {}
    backends: dict[str, int] = {}
    for event in events:
        outcome = str(event.get("outcome"))
        backend = str(event.get("backend"))
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
        backends[backend] = backends.get(backend, 0) + 1
    return {
        "schema_version": LEARNING_SCHEMA_VERSION,
        "events": len(events),
        "event_limit": EVENT_LIMIT,
        "contexts": len(contexts),
        "outcomes": dict(sorted(outcomes.items())),
        "backends": dict(sorted(backends.items())),
        "updated_at": state.get("updated_at"),
        "local_only": True,
        "external_telemetry": False,
        "persisted_fields": ["at", "context", "action", "capabilities", "backend", "outcome", "duration_ms"],
    }


def recommend_backend(
    root: Path | str,
    *,
    action: str,
    capabilities: Iterable[str],
    eligible_backends: Iterable[str],
    baseline_backend: str | None,
    min_samples: int = DEFAULT_MIN_SAMPLES,
    min_score_margin: float = DEFAULT_MIN_SCORE_MARGIN,
) -> dict[str, Any]:
    eligible = tuple(dict.fromkeys(normalize_backend(value) for value in eligible_backends))
    baseline = normalize_backend(baseline_backend) if baseline_backend else None
    stats = aggregate_context(root, action=action, capabilities=capabilities)
    base = {
        "context": context_key(action, capabilities),
        "baseline_backend": baseline,
        "eligible_backends": list(eligible),
        "min_samples": max(1, int(min_samples)),
        "stats": {backend: stats[backend] for backend in eligible if backend in stats},
    }

    if baseline is None or baseline not in eligible:
        return {**base, "mode": "baseline", "backend": baseline, "reason": "No valid baseline candidate to adapt."}
    if baseline in PROTECTED_HEAVY_BACKENDS:
        return {**base, "mode": "baseline", "backend": baseline, "reason": "Heavy/local backend is capability-driven, not learning-promoted."}

    alternatives = [backend for backend in eligible if backend != baseline and backend not in PROTECTED_HEAVY_BACKENDS]
    if not alternatives:
        return {**base, "mode": "insufficient-data", "backend": baseline, "reason": "No eligible lightweight alternative exists."}

    minimum = max(1, int(min_samples))
    baseline_stats = stats.get(baseline)
    if not baseline_stats or baseline_stats["resolved_samples"] < minimum:
        return {**base, "mode": "insufficient-data", "backend": baseline, "reason": "Baseline does not yet have enough resolved samples."}

    qualified = [backend for backend in alternatives if stats.get(backend, {}).get("resolved_samples", 0) >= minimum]
    if not qualified:
        return {**base, "mode": "insufficient-data", "backend": baseline, "reason": "Alternatives do not yet have enough resolved samples."}

    qualified.sort(
        key=lambda backend: (
            float(stats[backend]["posterior_success"]),
            -(stats[backend]["median_duration_ms"] or 10**18),
            backend,
        ),
        reverse=True,
    )
    best = qualified[0]
    baseline_score = float(baseline_stats["posterior_success"])
    best_score = float(stats[best]["posterior_success"])
    score_margin = best_score - baseline_score

    if score_margin >= float(min_score_margin):
        return {
            **base,
            "mode": "learned",
            "backend": best,
            "reason": f"Learned success score exceeds baseline by {score_margin:.3f}.",
            "signal": "success-rate",
        }

    baseline_duration = baseline_stats.get("median_duration_ms")
    best_duration = stats[best].get("median_duration_ms")
    if (
        abs(score_margin) <= DURATION_TIE_SCORE_DELTA
        and baseline_score >= 0.75
        and best_score >= 0.75
        and isinstance(baseline_duration, int)
        and isinstance(best_duration, int)
        and baseline_duration > 0
        and best_duration <= baseline_duration * DURATION_IMPROVEMENT_RATIO
    ):
        return {
            **base,
            "mode": "learned",
            "backend": best,
            "reason": "Success confidence is comparable and the alternative median duration is materially lower.",
            "signal": "duration",
        }

    return {
        **base,
        "mode": "baseline",
        "backend": baseline,
        "reason": "Evidence is not strong enough to override the baseline order.",
    }
