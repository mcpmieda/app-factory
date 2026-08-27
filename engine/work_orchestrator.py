from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from engine.execution_engine import CAPABILITIES, validate_capabilities

FACTORY_RUN_SCHEMA_VERSION = 1
MAX_AUTOMATIC_PARALLEL = 3
COST_ORDER = {"zero": 0, "free_quota": 1, "included": 2, "metered": 3}
HUMAN_GATES = {
    "product_decision",
    "destructive_operation",
    "production_activation",
    "privilege_change",
    "legal_or_organizational_decision",
}


@dataclass(frozen=True)
class ProviderSpec:
    provider_id: str
    cost_class: str
    execution_mode: str
    capabilities: frozenset[str]
    max_parallel: int
    automatic: bool = True
    requires_local_machine: bool = False
    description: str = ""


@dataclass(frozen=True)
class WorkItem:
    task_id: str
    title: str
    role: str
    depends_on: tuple[str, ...] = ()
    paths: tuple[str, ...] = ()
    required_capabilities: frozenset[str] = frozenset()
    preferred_providers: tuple[str, ...] = ()
    human_gates: frozenset[str] = frozenset()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TaskAssignment:
    task_id: str
    provider_id: str | None
    status: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "provider": self.provider_id,
            "status": self.status,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ExecutionWave:
    index: int
    assignments: tuple[TaskAssignment, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "assignments": [item.to_dict() for item in self.assignments],
        }


@dataclass(frozen=True)
class FactoryRunPlan:
    run_id: str
    goal: str
    waves: tuple[ExecutionWave, ...]
    blocked: tuple[TaskAssignment, ...]
    providers: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": FACTORY_RUN_SCHEMA_VERSION,
            "run_id": self.run_id,
            "goal": self.goal,
            "providers": list(self.providers),
            "waves": [wave.to_dict() for wave in self.waves],
            "blocked": [item.to_dict() for item in self.blocked],
        }


def default_worker_providers() -> dict[str, ProviderSpec]:
    common = frozenset({"reasoning", "repo_read", "repo_write", "build", "test", "review"})
    return {
        "opencode_ollama": ProviderSpec(
            provider_id="opencode_ollama",
            cost_class="zero",
            execution_mode="local_headless",
            capabilities=common | frozenset({"deterministic_commands", "headless_browser"}),
            max_parallel=2,
            requires_local_machine=True,
            description="OpenCode backed by a local Ollama model. Zero API cost and machine-dependent.",
        ),
        "jules": ProviderSpec(
            provider_id="jules",
            cost_class="free_quota",
            execution_mode="remote_github",
            capabilities=common | frozenset({"github_api", "deterministic_commands"}),
            max_parallel=3,
            description="Remote GitHub coding worker. Prefer issue/API dispatch with isolated branch/PR output.",
        ),
        "antigravity": ProviderSpec(
            provider_id="antigravity",
            cost_class="free_quota",
            execution_mode="headless_agent",
            capabilities=common | frozenset({"deterministic_commands", "headless_browser"}),
            max_parallel=3,
            description="Headless agent worker. Requires a pre-authenticated or explicitly configured environment.",
        ),
        "codex": ProviderSpec(
            provider_id="codex",
            cost_class="metered",
            execution_mode="premium_escalation",
            capabilities=frozenset(CAPABILITIES),
            max_parallel=1,
            automatic=False,
            requires_local_machine=True,
            description="Premium/manual escalation only. Never selected automatically by the zero-first policy.",
        ),
    }


def _clean_id(value: Any, *, label: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{label} is required")
    if len(text) > 120:
        raise ValueError(f"{label} is too long")
    return text


def _string_tuple(values: Any) -> tuple[str, ...]:
    if values is None:
        return ()
    if not isinstance(values, list):
        raise ValueError("expected an array of strings")
    result: list[str] = []
    for value in values:
        text = str(value).strip()
        if text and text not in result:
            result.append(text)
    return tuple(result)


def normalize_path_scope(value: str) -> str:
    path = str(value).strip().replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    path = path.strip("/")
    return path or "*"


def path_scopes_conflict(left: Iterable[str], right: Iterable[str]) -> bool:
    left_scopes = tuple(normalize_path_scope(item) for item in left)
    right_scopes = tuple(normalize_path_scope(item) for item in right)
    if not left_scopes or not right_scopes:
        return True
    for first in left_scopes:
        for second in right_scopes:
            if "*" in {first, second}:
                return True
            if first == second or first.startswith(second + "/") or second.startswith(first + "/"):
                return True
    return False


def parse_work_item(raw: Mapping[str, Any]) -> WorkItem:
    task_id = _clean_id(raw.get("id"), label="task id")
    title = _clean_id(raw.get("title"), label=f"title for {task_id}")
    role = str(raw.get("role") or "implementation").strip() or "implementation"
    depends_on = _string_tuple(raw.get("depends_on"))
    paths = tuple(normalize_path_scope(item) for item in _string_tuple(raw.get("paths")))
    required = validate_capabilities(_string_tuple(raw.get("required_capabilities")))
    preferred = _string_tuple(raw.get("preferred_providers"))
    human_gates = frozenset(_string_tuple(raw.get("human_gates")))
    unknown_gates = human_gates - HUMAN_GATES
    if unknown_gates:
        raise ValueError(f"Unknown human gates for {task_id}: {', '.join(sorted(unknown_gates))}")
    metadata = raw.get("metadata") or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"metadata for {task_id} must be an object")
    return WorkItem(
        task_id=task_id,
        title=title,
        role=role,
        depends_on=depends_on,
        paths=paths,
        required_capabilities=required,
        preferred_providers=preferred,
        human_gates=human_gates,
        metadata=dict(metadata),
    )


def load_factory_run(source: Path | str | Mapping[str, Any]) -> tuple[str, str, list[WorkItem]]:
    if isinstance(source, Mapping):
        raw = dict(source)
    else:
        path = Path(source)
        raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Factory Run must be a JSON object")
    version = raw.get("schema_version", FACTORY_RUN_SCHEMA_VERSION)
    if version != FACTORY_RUN_SCHEMA_VERSION:
        raise ValueError(f"Unsupported Factory Run schema_version: {version}")
    run_id = _clean_id(raw.get("run_id"), label="run_id")
    goal = _clean_id(raw.get("goal"), label="goal")
    items_raw = raw.get("tasks")
    if not isinstance(items_raw, list) or not items_raw:
        raise ValueError("Factory Run requires a non-empty tasks array")
    items = [parse_work_item(item) for item in items_raw if isinstance(item, dict)]
    if len(items) != len(items_raw):
        raise ValueError("Every task must be an object")
    validate_work_graph(items)
    return run_id, goal, items


def validate_work_graph(items: Iterable[WorkItem]) -> None:
    values = list(items)
    ids = [item.task_id for item in values]
    if len(ids) != len(set(ids)):
        raise ValueError("Factory Run task ids must be unique")
    known = set(ids)
    for item in values:
        unknown = set(item.depends_on) - known
        if unknown:
            raise ValueError(f"Task {item.task_id} depends on unknown tasks: {', '.join(sorted(unknown))}")
        if item.task_id in item.depends_on:
            raise ValueError(f"Task {item.task_id} cannot depend on itself")

    visiting: set[str] = set()
    visited: set[str] = set()
    by_id = {item.task_id: item for item in values}

    def visit(task_id: str) -> None:
        if task_id in visited:
            return
        if task_id in visiting:
            raise ValueError("Factory Run dependency graph contains a cycle")
        visiting.add(task_id)
        for dependency in by_id[task_id].depends_on:
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in ids:
        visit(task_id)


def eligible_providers(
    item: WorkItem,
    *,
    available_provider_ids: Iterable[str],
    providers: Mapping[str, ProviderSpec] | None = None,
    allow_metered: bool = False,
) -> list[ProviderSpec]:
    registry = dict(providers or default_worker_providers())
    available = list(dict.fromkeys(str(value).strip() for value in available_provider_ids if str(value).strip()))
    candidates: list[ProviderSpec] = []
    for provider_id in available:
        spec = registry.get(provider_id)
        if spec is None or not spec.automatic:
            continue
        if spec.cost_class == "metered" and not allow_metered:
            continue
        if not item.required_capabilities.issubset(spec.capabilities):
            continue
        candidates.append(spec)

    preference = {provider_id: index for index, provider_id in enumerate(item.preferred_providers)}
    candidates.sort(
        key=lambda spec: (
            COST_ORDER.get(spec.cost_class, 99),
            preference.get(spec.provider_id, 999),
            spec.requires_local_machine,
            spec.provider_id,
        )
    )
    return candidates


def _select_provider(
    item: WorkItem,
    *,
    available_provider_ids: Iterable[str],
    provider_usage: Mapping[str, int],
    providers: Mapping[str, ProviderSpec],
    allow_metered: bool,
) -> ProviderSpec | None:
    for provider in eligible_providers(
        item,
        available_provider_ids=available_provider_ids,
        providers=providers,
        allow_metered=allow_metered,
    ):
        if provider_usage.get(provider.provider_id, 0) < provider.max_parallel:
            return provider
    return None


def build_execution_plan(
    source: Path | str | Mapping[str, Any],
    *,
    available_provider_ids: Iterable[str],
    max_parallel: int = MAX_AUTOMATIC_PARALLEL,
    allow_metered: bool = False,
    providers: Mapping[str, ProviderSpec] | None = None,
) -> FactoryRunPlan:
    run_id, goal, items = load_factory_run(source)
    registry = dict(providers or default_worker_providers())
    available = tuple(dict.fromkeys(str(value).strip() for value in available_provider_ids if str(value).strip()))
    max_parallel = int(max_parallel)
    if not 1 <= max_parallel <= MAX_AUTOMATIC_PARALLEL:
        raise ValueError(f"max_parallel must be between 1 and {MAX_AUTOMATIC_PARALLEL}")
    remaining = {item.task_id: item for item in items}
    completed: set[str] = set()
    blocked: list[TaskAssignment] = []
    waves: list[ExecutionWave] = []

    while remaining:
        human_blocked_ids = [
            task_id
            for task_id, item in remaining.items()
            if item.human_gates and set(item.depends_on).issubset(completed)
        ]
        for task_id in human_blocked_ids:
            item = remaining.pop(task_id)
            blocked.append(TaskAssignment(
                task_id=item.task_id,
                provider_id=None,
                status="human-required",
                reason="Human gate required: " + ", ".join(sorted(item.human_gates)),
            ))

        ready = [item for item in remaining.values() if set(item.depends_on).issubset(completed)]
        if not ready:
            for item in remaining.values():
                blocked.append(TaskAssignment(
                    task_id=item.task_id,
                    provider_id=None,
                    status="blocked",
                    reason="Dependency is blocked or requires human resolution.",
                ))
            break

        provider_usage: dict[str, int] = {}
        selected_items: list[WorkItem] = []
        assignments: list[TaskAssignment] = []

        for item in ready:
            if len(assignments) >= max_parallel:
                break
            if any(path_scopes_conflict(item.paths, selected.paths) for selected in selected_items):
                continue
            provider = _select_provider(
                item,
                available_provider_ids=available,
                provider_usage=provider_usage,
                providers=registry,
                allow_metered=allow_metered,
            )
            if provider is None:
                continue
            provider_usage[provider.provider_id] = provider_usage.get(provider.provider_id, 0) + 1
            selected_items.append(item)
            assignments.append(TaskAssignment(
                task_id=item.task_id,
                provider_id=provider.provider_id,
                status="routed",
                reason=f"Selected {provider.provider_id} using zero-first eligible-provider routing.",
            ))

        if not assignments:
            unroutable = ready[0]
            remaining.pop(unroutable.task_id)
            blocked.append(TaskAssignment(
                task_id=unroutable.task_id,
                provider_id=None,
                status="no-provider",
                reason="No automatic available provider satisfies the task capabilities/cost policy.",
            ))
            continue

        waves.append(ExecutionWave(index=len(waves) + 1, assignments=tuple(assignments)))
        for item in selected_items:
            remaining.pop(item.task_id, None)
            completed.add(item.task_id)

    return FactoryRunPlan(
        run_id=run_id,
        goal=goal,
        waves=tuple(waves),
        blocked=tuple(blocked),
        providers=available,
    )


def factory_run_template() -> dict[str, Any]:
    return {
        "schema_version": FACTORY_RUN_SCHEMA_VERSION,
        "run_id": "project-phase-001",
        "goal": "Deliver one large functional phase without touching production.",
        "tasks": [
            {
                "id": "implementation-a",
                "title": "Implement independent functional slice A",
                "role": "implementation",
                "depends_on": [],
                "paths": ["src/feature-a"],
                "required_capabilities": ["reasoning", "repo_read", "repo_write", "test"],
                "preferred_providers": ["jules", "antigravity", "opencode_ollama"],
                "human_gates": [],
            },
            {
                "id": "verification-a",
                "title": "Verify slice A independently",
                "role": "verification",
                "depends_on": ["implementation-a"],
                "paths": ["tests/feature-a"],
                "required_capabilities": ["repo_read", "repo_write", "test"],
                "preferred_providers": ["opencode_ollama", "jules"],
                "human_gates": [],
            },
        ],
    }
