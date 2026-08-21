from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

EXECUTION_SCHEMA_VERSION = 1
HISTORY_LIMIT = 100
DEFAULT_FAILURE_THRESHOLD = 2

CAPABILITIES = {
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

BACKEND_ORDER = ("current_agent", "github_ci", "sandbox", "local_full")


@dataclass(frozen=True)
class BackendSpec:
    backend_id: str
    tier: int
    capabilities: frozenset[str]
    description: str


@dataclass(frozen=True)
class ExecutionRequest:
    action: str
    required_capabilities: frozenset[str]
    preferred_capabilities: frozenset[str] = frozenset()
    risk: str = "normal"


@dataclass(frozen=True)
class RouteDecision:
    backend_id: str | None
    action: str
    required_capabilities: tuple[str, ...]
    available_backends: tuple[str, ...]
    rejected: dict[str, list[str]]
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "backend": self.backend_id,
            "action": self.action,
            "required_capabilities": list(self.required_capabilities),
            "available_backends": list(self.available_backends),
            "rejected": self.rejected,
            "reason": self.reason,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_backends() -> dict[str, BackendSpec]:
    return {
        "current_agent": BackendSpec(
            backend_id="current_agent",
            tier=0,
            capabilities=frozenset({"reasoning", "repo_read", "repo_write", "github_api", "review"}),
            description="Current agent plus directly connected repository/GitHub tools.",
        ),
        "github_ci": BackendSpec(
            backend_id="github_ci",
            tier=1,
            capabilities=frozenset({
                "repo_read", "deterministic_commands", "build", "test",
                "headless_browser", "ephemeral_services",
            }),
            description="GitHub Actions/CI for deterministic reproducible execution.",
        ),
        "sandbox": BackendSpec(
            backend_id="sandbox",
            tier=2,
            capabilities=frozenset({
                "repo_read", "repo_write", "deterministic_commands", "build", "test", "headless_browser",
            }),
            description="Lightweight shell/sandbox backend when available.",
        ),
        "local_full": BackendSpec(
            backend_id="local_full",
            tier=3,
            capabilities=frozenset(CAPABILITIES),
            description="Full local/interactive executor such as Codex or another compatible agent.",
        ),
    }


def validate_capabilities(values: Iterable[str]) -> frozenset[str]:
    result = frozenset(str(value).strip() for value in values if str(value).strip())
    unknown = result - CAPABILITIES
    if unknown:
        raise ValueError(f"Unknown execution capabilities: {', '.join(sorted(unknown))}")
    return result


def request_for_action(
    action: str,
    *,
    headless_browser: bool = False,
    interactive_shell: bool = False,
    interactive_browser: bool = False,
    live_migration: bool = False,
    extra_capabilities: Iterable[str] = (),
) -> ExecutionRequest:
    base: dict[str, set[str]] = {
        "plan": {"reasoning", "repo_read"},
        "reconcile_context": {"reasoning", "repo_read"},
        "implement": {"reasoning", "repo_read", "repo_write"},
        "verify": {"deterministic_commands", "test"},
        "repair": {"reasoning", "repo_read", "repo_write"},
        "review": {"reasoning", "repo_read", "review"},
        "deliver": {"github_api", "repo_write"},
        "resolve_blocker": {"reasoning", "repo_read"},
        "request_human": set(),
        "done": set(),
        "inspect_state": {"reasoning", "repo_read"},
    }
    required = set(base.get(action, {"reasoning", "repo_read"}))
    if headless_browser:
        required.add("headless_browser")
    if interactive_shell:
        required.add("interactive_shell")
    if interactive_browser:
        required.add("interactive_browser")
    if live_migration:
        required.add("live_migration")
    required.update(validate_capabilities(extra_capabilities))
    return ExecutionRequest(action=action, required_capabilities=validate_capabilities(required))


def route_execution(
    request: ExecutionRequest,
    *,
    available_backends: Iterable[str] = ("current_agent", "github_ci"),
    failed_backends: Iterable[str] = (),
    backends: dict[str, BackendSpec] | None = None,
) -> RouteDecision:
    registry = backends or default_backends()
    available = tuple(dict.fromkeys(str(value) for value in available_backends))
    failed = set(failed_backends)
    rejected: dict[str, list[str]] = {}

    candidates: list[BackendSpec] = []
    for backend_id in available:
        spec = registry.get(backend_id)
        if spec is None:
            rejected[backend_id] = ["unknown-backend"]
            continue
        if backend_id in failed:
            rejected[backend_id] = ["failure-threshold-reached"]
            continue
        missing = sorted(request.required_capabilities - spec.capabilities)
        if missing:
            rejected[backend_id] = [f"missing:{capability}" for capability in missing]
            continue
        candidates.append(spec)

    if not candidates:
        needed = ", ".join(sorted(request.required_capabilities)) or "none"
        return RouteDecision(
            backend_id=None,
            action=request.action,
            required_capabilities=tuple(sorted(request.required_capabilities)),
            available_backends=available,
            rejected=rejected,
            reason=f"No available backend satisfies required capabilities: {needed}.",
        )

    order_index = {name: index for index, name in enumerate(BACKEND_ORDER)}
    candidates.sort(key=lambda spec: (spec.tier, order_index.get(spec.backend_id, 999), spec.backend_id))
    chosen = candidates[0]
    return RouteDecision(
        backend_id=chosen.backend_id,
        action=request.action,
        required_capabilities=tuple(sorted(request.required_capabilities)),
        available_backends=available,
        rejected=rejected,
        reason=f"Selected {chosen.backend_id}: lightest available backend with all required capabilities.",
    )


def execution_state_path(root: Path | str) -> Path:
    return Path(root).resolve() / ".factory" / "execution.json"


def read_execution_state(root: Path | str) -> dict[str, Any]:
    path = execution_state_path(root)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        value = None
    if not isinstance(value, dict):
        return {"schema_version": EXECUTION_SCHEMA_VERSION, "attempts": []}
    attempts = value.get("attempts")
    if not isinstance(attempts, list):
        value["attempts"] = []
    value["schema_version"] = EXECUTION_SCHEMA_VERSION
    return value


def write_execution_state(root: Path | str, state: dict[str, Any]) -> None:
    path = execution_state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sanitize_summary(summary: str | None) -> str | None:
    if summary is None:
        return None
    compact = " ".join(str(summary).split())
    return compact[:500] or None


def record_execution_attempt(
    root: Path | str,
    *,
    action: str,
    backend_id: str,
    required_capabilities: Iterable[str],
    outcome: str,
    summary: str | None = None,
    duration_ms: int | None = None,
) -> dict[str, Any]:
    if outcome not in {"success", "failure", "blocked", "cancelled"}:
        raise ValueError("outcome must be success, failure, blocked or cancelled")
    registry = default_backends()
    if backend_id not in registry:
        raise ValueError(f"Unknown backend: {backend_id}")
    capabilities = validate_capabilities(required_capabilities)
    attempt = {
        "at": utc_now(),
        "action": action,
        "backend": backend_id,
        "required_capabilities": sorted(capabilities),
        "outcome": outcome,
        "summary": sanitize_summary(summary),
        "duration_ms": max(0, int(duration_ms)) if duration_ms is not None else None,
    }
    state = read_execution_state(root)
    attempts = state.setdefault("attempts", [])
    attempts.append(attempt)
    if len(attempts) > HISTORY_LIMIT:
        del attempts[:-HISTORY_LIMIT]
    state["updated_at"] = utc_now()
    write_execution_state(root, state)
    return state


def failed_backends_for_action(
    root: Path | str,
    action: str,
    *,
    threshold: int = DEFAULT_FAILURE_THRESHOLD,
) -> set[str]:
    threshold = max(1, int(threshold))
    attempts = read_execution_state(root).get("attempts", [])
    counts: dict[str, int] = {}
    resolved: set[str] = set()
    for item in reversed(attempts):
        if not isinstance(item, dict) or item.get("action") != action:
            continue
        backend = item.get("backend")
        if not isinstance(backend, str) or backend in resolved:
            continue
        outcome = item.get("outcome")
        if outcome == "success":
            resolved.add(backend)
            counts.pop(backend, None)
            continue
        if outcome == "failure":
            counts[backend] = counts.get(backend, 0) + 1
    return {backend for backend, count in counts.items() if count >= threshold}


def route_action(
    root: Path | str,
    action: str,
    *,
    available_backends: Iterable[str] = ("current_agent", "github_ci"),
    failure_threshold: int = DEFAULT_FAILURE_THRESHOLD,
    headless_browser: bool = False,
    interactive_shell: bool = False,
    interactive_browser: bool = False,
    live_migration: bool = False,
    extra_capabilities: Iterable[str] = (),
) -> RouteDecision:
    request = request_for_action(
        action,
        headless_browser=headless_browser,
        interactive_shell=interactive_shell,
        interactive_browser=interactive_browser,
        live_migration=live_migration,
        extra_capabilities=extra_capabilities,
    )
    failed = failed_backends_for_action(root, action, threshold=failure_threshold)
    return route_execution(
        request,
        available_backends=available_backends,
        failed_backends=failed,
    )
