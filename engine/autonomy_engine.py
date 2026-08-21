from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .context_engine import ScanResult, load_json, scan_repository

STATE_SCHEMA_VERSION = 1
DEFAULT_MAX_REPAIRS = 3
HISTORY_LIMIT = 60

PHASES = {
    "context", "planning", "implementation", "verification", "repair",
    "review", "delivery", "blocked", "done",
}

EVENTS = {
    "plan-ready",
    "implementation-started",
    "implementation-ready",
    "verification-pass",
    "verification-fail",
    "repair-ready",
    "review-pass",
    "review-fail",
    "delivered",
    "blocked",
    "human-needed",
    "resolved",
    "context-reconciled",
    "note",
}

HUMAN_CATEGORIES = {"product", "cost", "risk", "credential", "data", "legal", "organizational"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def state_path(root: Path) -> Path:
    return root / ".factory" / "state.json"


def read_state(root: Path) -> dict[str, Any] | None:
    return load_json(state_path(root))


def write_state(root: Path, state: dict[str, Any]) -> None:
    path = state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_history(state: dict[str, Any], event: str, summary: str | None = None) -> None:
    history = state.setdefault("history", [])
    history.append({"at": utc_now(), "event": event, "summary": summary})
    if len(history) > HISTORY_LIMIT:
        del history[:-HISTORY_LIMIT]
    state["updated_at"] = utc_now()


def infer_goal(root: Path) -> str:
    for name in ("PROJECT_STATE.md", "README.md"):
        path = root / name
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if name == "PROJECT_STATE.md":
            match = re.search(r"##\s+Objetivo atual\s*\n+(.+?)(?:\n##|\Z)", text, re.DOTALL | re.IGNORECASE)
            if match:
                paragraph = " ".join(line.strip() for line in match.group(1).splitlines() if line.strip() and not line.lstrip().startswith(">"))
                if paragraph:
                    return paragraph[:800]
        for line in text.splitlines():
            cleaned = line.strip()
            if cleaned and not cleaned.startswith("#") and not cleaned.startswith(">"):
                return cleaned[:800]
    return "Continuar o projeto a partir do estado versionado atual."


def new_state(goal: str, context: ScanResult, max_repairs: int = DEFAULT_MAX_REPAIRS) -> dict[str, Any]:
    now = utc_now()
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "goal": goal.strip(),
        "status": "active",
        "phase": "planning",
        "previous_phase": None,
        "context_fingerprint": context.repo_map["fingerprint"],
        "context_generated_at": context.repo_map["generated_at"],
        "context_delta": context.repo_map["delta"],
        "plan_summary": None,
        "implementation_summary": None,
        "verification": {"status": "unknown", "summary": None},
        "repair_attempts": 0,
        "max_repair_attempts": max(1, int(max_repairs)),
        "review": {"status": "unknown", "summary": None},
        "blockers": [],
        "human_needed": None,
        "created_at": now,
        "updated_at": now,
        "history": [{"at": now, "event": "initialized", "summary": goal.strip()}],
    }


def init_project(root: Path | str, goal: str | None = None, max_repairs: int = DEFAULT_MAX_REPAIRS) -> dict[str, Any]:
    root = Path(root).resolve()
    context = scan_repository(root)
    actual_goal = (goal or infer_goal(root)).strip()
    state = new_state(actual_goal, context, max_repairs=max_repairs)
    write_state(root, state)
    return state


def refresh_context(root: Path, state: dict[str, Any] | None = None) -> tuple[ScanResult, bool]:
    context = scan_repository(root)
    changed = bool(state and state.get("context_fingerprint") and state.get("context_fingerprint") != context.repo_map["fingerprint"])
    return context, changed


def reconcile_if_needed(root: Path, state: dict[str, Any], context: ScanResult) -> bool:
    old = state.get("context_fingerprint")
    new = context.repo_map["fingerprint"]
    if old and old != new and state.get("phase") not in {"context", "planning", "done", "blocked"}:
        if state.get("phase") != "context":
            state["previous_phase"] = state.get("phase")
        state["phase"] = "context"
        state["context_delta"] = context.repo_map["delta"]
        append_history(state, "context-changed", f"{old[:12]} -> {new[:12]}")
        write_state(root, state)
        return True
    state["context_fingerprint"] = new
    state["context_generated_at"] = context.repo_map["generated_at"]
    state["context_delta"] = context.repo_map["delta"]
    write_state(root, state)
    return False


def action_for(state: dict[str, Any]) -> dict[str, Any]:
    status = state.get("status")
    phase = state.get("phase")
    base = {
        "status": status,
        "phase": phase,
        "goal": state.get("goal"),
        "requires_human": False,
        "context_fingerprint": state.get("context_fingerprint"),
    }

    if status == "done" or phase == "done":
        return {**base, "action": "done", "reason": "A entrega foi registrada como concluída.", "recommended_executor": "none"}
    if status == "blocked" or phase == "blocked":
        human = state.get("human_needed")
        requires_human = bool(human)
        return {
            **base,
            "action": "request_human" if requires_human else "resolve_blocker",
            "reason": human.get("reason") if isinstance(human, dict) else (state.get("blockers") or ["Bloqueio não resolvido."])[-1],
            "requires_human": requires_human,
            "recommended_executor": "human" if requires_human else "stronger_executor_or_current_agent",
        }
    if phase == "context":
        return {
            **base,
            "action": "reconcile_context",
            "reason": "O repositório mudou desde o último estado conhecido; reconciliar o delta antes de continuar.",
            "recommended_executor": "current_agent",
            "delta": state.get("context_delta", {}),
        }
    if phase == "planning":
        return {**base, "action": "plan", "reason": "Transformar o objetivo em uma fatia funcional verificável.", "recommended_executor": "current_agent"}
    if phase == "implementation":
        return {**base, "action": "implement", "reason": "Executar a maior fatia segura do plano atual.", "recommended_executor": "current_agent_first"}
    if phase == "verification":
        return {**base, "action": "verify", "reason": "Provar comportamento e regressão proporcionalmente ao risco.", "recommended_executor": "ci_or_current_agent"}
    if phase == "repair":
        return {
            **base,
            "action": "repair",
            "reason": f"Corrigir a falha verificada; tentativa {state.get('repair_attempts', 0)}/{state.get('max_repair_attempts', DEFAULT_MAX_REPAIRS)}.",
            "recommended_executor": "current_agent_then_ci",
        }
    if phase == "review":
        return {**base, "action": "review", "reason": "Revisar especificação, diff, segurança e qualidade antes da entrega.", "recommended_executor": "current_agent_or_independent_reviewer"}
    if phase == "delivery":
        return {**base, "action": "deliver", "reason": "Integrar/entregar somente com gates aprovados.", "recommended_executor": "github_or_current_agent"}
    return {**base, "action": "inspect_state", "reason": f"Fase desconhecida: {phase!r}.", "recommended_executor": "current_agent"}


def next_action(root: Path | str, auto_refresh: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    root = Path(root).resolve()
    state = read_state(root)
    if state is None:
        state = init_project(root)
    if auto_refresh:
        context, _ = refresh_context(root, state)
        reconcile_if_needed(root, state, context)
        state = read_state(root) or state
    return action_for(state), state


def record_event(
    root: Path | str,
    event: str,
    summary: str | None = None,
    category: str | None = None,
) -> dict[str, Any]:
    root = Path(root).resolve()
    if event not in EVENTS:
        raise ValueError(f"Unsupported event: {event}")
    state = read_state(root)
    if state is None:
        state = init_project(root)

    if event == "plan-ready":
        state["plan_summary"] = summary
        state["phase"] = "implementation"
    elif event == "implementation-started":
        state["phase"] = "implementation"
    elif event == "implementation-ready":
        state["implementation_summary"] = summary
        state["phase"] = "verification"
        state["verification"] = {"status": "unknown", "summary": None}
    elif event == "verification-pass":
        state["verification"] = {"status": "pass", "summary": summary}
        state["phase"] = "review"
        state["repair_attempts"] = 0
    elif event == "verification-fail":
        attempts = int(state.get("repair_attempts", 0)) + 1
        state["repair_attempts"] = attempts
        state["verification"] = {"status": "fail", "summary": summary}
        if attempts >= int(state.get("max_repair_attempts", DEFAULT_MAX_REPAIRS)):
            state["previous_phase"] = "repair"
            state["status"] = "blocked"
            state["phase"] = "blocked"
            state.setdefault("blockers", []).append(summary or "Repair loop reached its configured limit.")
        else:
            state["phase"] = "repair"
    elif event == "repair-ready":
        state["phase"] = "verification"
    elif event == "review-pass":
        state["review"] = {"status": "pass", "summary": summary}
        state["phase"] = "delivery"
    elif event == "review-fail":
        state["review"] = {"status": "fail", "summary": summary}
        state["phase"] = "implementation"
    elif event == "delivered":
        state["status"] = "done"
        state["phase"] = "done"
    elif event == "blocked":
        state["previous_phase"] = state.get("phase")
        state["status"] = "blocked"
        state["phase"] = "blocked"
        state.setdefault("blockers", []).append(summary or "Blocked")
    elif event == "human-needed":
        if category not in HUMAN_CATEGORIES:
            raise ValueError(f"human-needed requires category in {sorted(HUMAN_CATEGORIES)}")
        state["previous_phase"] = state.get("phase")
        state["human_needed"] = {"category": category, "reason": summary or "Human decision required."}
        state["status"] = "blocked"
        state["phase"] = "blocked"
    elif event == "resolved":
        state["status"] = "active"
        state["human_needed"] = None
        state["blockers"] = []
        state["phase"] = state.get("previous_phase") or "planning"
        state["previous_phase"] = None
    elif event == "context-reconciled":
        context = scan_repository(root)
        state["context_fingerprint"] = context.repo_map["fingerprint"]
        state["context_generated_at"] = context.repo_map["generated_at"]
        state["context_delta"] = context.repo_map["delta"]
        state["phase"] = state.get("previous_phase") or "planning"
        state["previous_phase"] = None

    if state.get("phase") not in PHASES:
        raise ValueError(f"Invalid phase: {state.get('phase')}")
    append_history(state, event, summary)
    write_state(root, state)
    return state


@dataclass(frozen=True)
class ResumeResult:
    state: dict[str, Any]
    action: dict[str, Any]
    context: ScanResult


def resume_project(root: Path | str, goal: str | None = None, max_repairs: int = DEFAULT_MAX_REPAIRS) -> ResumeResult:
    root = Path(root).resolve()
    state = read_state(root)
    context = scan_repository(root)
    if state is None:
        state = new_state((goal or infer_goal(root)).strip(), context, max_repairs=max_repairs)
        write_state(root, state)
    else:
        reconcile_if_needed(root, state, context)
        state = read_state(root) or state
    return ResumeResult(state=state, action=action_for(state), context=context)
