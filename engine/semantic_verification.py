from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .ci_executor import discover_declared_gates
from .context_engine import scan_repository

SCHEMA_VERSION = 1
SPEC_PATH = Path("specs/semantic-contract.json")
PLAN_PATH = Path("specs/verification-plan.json")
REVIEW_PATH = Path("specs/review-evidence.json")

CHANGE_TYPES = {"functional", "bugfix", "refactor", "docs", "infra", "chore"}
RISK_LEVELS = {"low", "medium", "high"}
PRIORITIES = {"must", "should", "may"}
EVIDENCE_KINDS = {"test", "gate", "browser", "visual"}
REVIEW_MODES = {"independent-agent", "clean-context", "deterministic-ci"}
VERDICTS = {"pass", "fail"}

CRITERION_ID_RE = re.compile(r"^AC-\d{3,}$")
INVARIANT_ID_RE = re.compile(r"^INV-\d{3,}$")
SUBJECT_EXCLUDES = {REVIEW_PATH.as_posix()}
OPERATIONAL_PREFIXES = (".factory/",)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def semantic_spec_required(change_type: str, risk: str) -> bool:
    if change_type in {"docs", "chore"}:
        return False
    if change_type == "refactor" and risk == "low":
        return False
    return True


def spec_path(root: Path | str) -> Path:
    return Path(root).resolve() / SPEC_PATH


def plan_path(root: Path | str) -> Path:
    return Path(root).resolve() / PLAN_PATH


def review_path(root: Path | str) -> Path:
    return Path(root).resolve() / REVIEW_PATH


def read_spec(root: Path | str) -> dict[str, Any] | None:
    return _read_json(spec_path(root))


def read_verification_plan(root: Path | str) -> dict[str, Any] | None:
    return _read_json(plan_path(root))


def read_review_evidence(root: Path | str) -> dict[str, Any] | None:
    return _read_json(review_path(root))


def new_spec(goal: str, *, change_type: str = "functional", risk: str = "medium") -> dict[str, Any]:
    if change_type not in CHANGE_TYPES:
        raise ValueError(f"Unsupported change type: {change_type}")
    if risk not in RISK_LEVELS:
        raise ValueError(f"Unsupported risk: {risk}")
    return {
        "schema_version": SCHEMA_VERSION,
        "goal": goal.strip(),
        "change_type": change_type,
        "risk": risk,
        "scope": {"in": [], "out": []},
        "assumptions": [],
        "invariants": [],
        "data_contracts": [],
        "interfaces": [],
        "acceptance_criteria": [],
    }


def _nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value)


def validate_spec(spec: dict[str, Any] | None) -> list[str]:
    errors: list[str] = []
    if not isinstance(spec, dict):
        return ["spec must be a JSON object"]
    if spec.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    goal = spec.get("goal")
    if not isinstance(goal, str) or len(goal.strip()) < 8:
        errors.append("goal must be a meaningful non-empty string")

    change_type = spec.get("change_type")
    if change_type not in CHANGE_TYPES:
        errors.append(f"change_type must be one of {sorted(CHANGE_TYPES)}")
    risk = spec.get("risk")
    if risk not in RISK_LEVELS:
        errors.append(f"risk must be one of {sorted(RISK_LEVELS)}")

    scope = spec.get("scope")
    if not isinstance(scope, dict) or not _nonempty_strings(scope.get("in", [])) or not _nonempty_strings(scope.get("out", [])):
        errors.append("scope.in and scope.out must be arrays of non-empty strings")

    invariants = spec.get("invariants", [])
    if not isinstance(invariants, list):
        errors.append("invariants must be an array")
        invariants = []
    invariant_ids: set[str] = set()
    for index, item in enumerate(invariants):
        if not isinstance(item, dict):
            errors.append(f"invariants[{index}] must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not INVARIANT_ID_RE.fullmatch(item_id):
            errors.append(f"invariants[{index}].id must match INV-###")
        elif item_id in invariant_ids:
            errors.append(f"duplicate invariant id: {item_id}")
        else:
            invariant_ids.add(item_id)
        statement = item.get("statement")
        if not isinstance(statement, str) or not statement.strip():
            errors.append(f"invariants[{index}].statement is required")

    criteria = spec.get("acceptance_criteria", [])
    if not isinstance(criteria, list):
        errors.append("acceptance_criteria must be an array")
        criteria = []
    if semantic_spec_required(str(change_type), str(risk)) and not criteria:
        errors.append("functional/relevant work requires at least one acceptance criterion")

    criterion_ids: set[str] = set()
    for index, item in enumerate(criteria):
        if not isinstance(item, dict):
            errors.append(f"acceptance_criteria[{index}] must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not CRITERION_ID_RE.fullmatch(item_id):
            errors.append(f"acceptance_criteria[{index}].id must match AC-###")
        elif item_id in criterion_ids:
            errors.append(f"duplicate acceptance criterion id: {item_id}")
        else:
            criterion_ids.add(item_id)
        if item.get("priority") not in PRIORITIES:
            errors.append(f"acceptance_criteria[{index}].priority must be one of {sorted(PRIORITIES)}")
        for key in ("given", "when"):
            value = item.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"acceptance_criteria[{index}].{key} is required")
        then = item.get("then")
        if not isinstance(then, list) or not then or not _nonempty_strings(then):
            errors.append(f"acceptance_criteria[{index}].then must contain at least one expected result")
        preferred = item.get("verification", [])
        if preferred and (not isinstance(preferred, list) or not all(kind in EVIDENCE_KINDS for kind in preferred)):
            errors.append(f"acceptance_criteria[{index}].verification contains unsupported evidence kind")

    for key in ("assumptions", "data_contracts", "interfaces"):
        if not isinstance(spec.get(key, []), list):
            errors.append(f"{key} must be an array")
    return errors


def write_spec(root: Path | str, spec: dict[str, Any]) -> None:
    errors = validate_spec(spec)
    if errors:
        raise ValueError("Invalid semantic spec: " + "; ".join(errors))
    _write_json(spec_path(root), spec)


def spec_fingerprint(spec: dict[str, Any]) -> str:
    return _canonical_hash(spec)


def create_verification_plan(spec: dict[str, Any]) -> dict[str, Any]:
    errors = validate_spec(spec)
    if errors:
        raise ValueError("Invalid semantic spec: " + "; ".join(errors))
    return {
        "schema_version": SCHEMA_VERSION,
        "spec_fingerprint": spec_fingerprint(spec),
        "criteria": [
            {
                "id": item["id"],
                "priority": item["priority"],
                "preferred_evidence": list(item.get("verification", [])),
                "evidence": [],
            }
            for item in spec.get("acceptance_criteria", [])
        ],
    }


def write_verification_plan(root: Path | str, plan: dict[str, Any]) -> None:
    _write_json(plan_path(root), plan)


def validate_verification_plan(root: Path | str, *, spec: dict[str, Any] | None = None, plan: dict[str, Any] | None = None) -> list[str]:
    root = Path(root).resolve()
    spec = spec if spec is not None else read_spec(root)
    plan = plan if plan is not None else read_verification_plan(root)
    spec_errors = validate_spec(spec)
    if spec_errors:
        return ["spec: " + error for error in spec_errors]
    assert spec is not None

    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["verification plan is missing or invalid JSON"]
    if plan.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"verification plan schema_version must be {SCHEMA_VERSION}")
    if plan.get("spec_fingerprint") != spec_fingerprint(spec):
        errors.append("verification plan is stale: spec_fingerprint does not match current spec")

    rows = plan.get("criteria", [])
    if not isinstance(rows, list):
        return errors + ["verification plan criteria must be an array"]
    row_by_id = {row.get("id"): row for row in rows if isinstance(row, dict) and isinstance(row.get("id"), str)}
    known_gate_ids = {gate.gate_id for gate in discover_declared_gates(root)}

    for criterion in spec.get("acceptance_criteria", []):
        criterion_id = criterion["id"]
        row = row_by_id.get(criterion_id)
        if not isinstance(row, dict):
            if criterion["priority"] == "must":
                errors.append(f"{criterion_id} has no verification-plan row")
            continue
        evidence = row.get("evidence", [])
        if not isinstance(evidence, list):
            errors.append(f"{criterion_id}.evidence must be an array")
            evidence = []

        executable = 0
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"{criterion_id}.evidence[{index}] must be an object")
                continue
            kind = item.get("kind")
            if kind not in EVIDENCE_KINDS:
                errors.append(f"{criterion_id}.evidence[{index}].kind is unsupported")
                continue
            gate = item.get("gate")
            if not isinstance(gate, str) or not gate.strip():
                errors.append(f"{criterion_id}.evidence[{index}] must reference a declared gate")
            elif gate not in known_gate_ids:
                errors.append(f"{criterion_id}.evidence[{index}] references undeclared gate {gate}")
            else:
                executable += 1
            ref = item.get("ref")
            if kind in {"test", "browser", "visual"}:
                if not isinstance(ref, str) or not ref.strip():
                    errors.append(f"{criterion_id}.evidence[{index}] requires a file ref")
                elif not (root / ref).is_file():
                    errors.append(f"{criterion_id}.evidence[{index}] ref does not exist: {ref}")

        if criterion["priority"] == "must" and executable == 0:
            errors.append(f"{criterion_id} must have at least one executable declared-gate evidence")
    return errors


def subject_fingerprint(root: Path | str) -> str:
    root = Path(root).resolve()
    context = scan_repository(root)
    material: list[str] = []
    for path, meta in sorted(context.repo_map.get("files", {}).items()):
        if path in SUBJECT_EXCLUDES or path.startswith(OPERATIONAL_PREFIXES):
            continue
        digest = meta.get("sha256") if isinstance(meta, dict) else None
        if isinstance(digest, str):
            material.append(f"{path}:{digest}")
    return hashlib.sha256("\n".join(material).encode("utf-8")).hexdigest()


def required_review_mode(spec: dict[str, Any]) -> str:
    return "decoupled" if spec.get("risk") in {"medium", "high"} else "any"


def write_review_evidence(root: Path | str, *, mode: str, verdict: str, criterion_results: dict[str, str], findings: Iterable[str] = ()) -> dict[str, Any]:
    root = Path(root).resolve()
    spec = read_spec(root)
    plan = read_verification_plan(root)
    spec_errors = validate_spec(spec)
    if spec_errors:
        raise ValueError("Invalid semantic spec: " + "; ".join(spec_errors))
    plan_errors = validate_verification_plan(root, spec=spec, plan=plan)
    if plan_errors:
        raise ValueError("Invalid verification plan: " + "; ".join(plan_errors))
    assert spec is not None and plan is not None
    if mode not in REVIEW_MODES:
        raise ValueError(f"Unsupported review mode: {mode}")
    if verdict not in VERDICTS:
        raise ValueError(f"Unsupported verdict: {verdict}")
    if required_review_mode(spec) == "decoupled" and mode == "deterministic-ci":
        raise ValueError("medium/high risk requires independent-agent or clean-context review")

    must_ids = {item["id"] for item in spec.get("acceptance_criteria", []) if item.get("priority") == "must"}
    missing = sorted(criterion_id for criterion_id in must_ids if criterion_results.get(criterion_id) != "pass")
    if verdict == "pass" and missing:
        raise ValueError("passing review must mark every must criterion pass: " + ", ".join(missing))

    value = {
        "schema_version": SCHEMA_VERSION,
        "created_at": utc_now(),
        "mode": mode,
        "verdict": verdict,
        "spec_fingerprint": spec_fingerprint(spec),
        "verification_plan_fingerprint": _canonical_hash(plan),
        "subject_fingerprint": subject_fingerprint(root),
        "criteria": dict(sorted(criterion_results.items())),
        "findings": [str(item) for item in findings if str(item).strip()],
    }
    _write_json(review_path(root), value)
    return value


def validate_review_evidence(root: Path | str) -> list[str]:
    root = Path(root).resolve()
    spec = read_spec(root)
    plan = read_verification_plan(root)
    review = read_review_evidence(root)
    spec_errors = validate_spec(spec)
    if spec_errors:
        return ["spec: " + error for error in spec_errors]
    plan_errors = validate_verification_plan(root, spec=spec, plan=plan)
    if plan_errors:
        return ["verification: " + error for error in plan_errors]
    assert spec is not None and plan is not None

    if not isinstance(review, dict):
        return ["review evidence is missing or invalid JSON"]
    errors: list[str] = []
    if review.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"review schema_version must be {SCHEMA_VERSION}")
    mode = review.get("mode")
    if mode not in REVIEW_MODES:
        errors.append("review mode is invalid")
    elif required_review_mode(spec) == "decoupled" and mode == "deterministic-ci":
        errors.append("medium/high risk review is not decoupled")
    if review.get("verdict") != "pass":
        errors.append("review verdict is not pass")
    if review.get("spec_fingerprint") != spec_fingerprint(spec):
        errors.append("review is stale: spec fingerprint changed")
    if review.get("verification_plan_fingerprint") != _canonical_hash(plan):
        errors.append("review is stale: verification plan changed")
    if review.get("subject_fingerprint") != subject_fingerprint(root):
        errors.append("review is stale: reviewed subject changed")

    criterion_results = review.get("criteria", {})
    if not isinstance(criterion_results, dict):
        errors.append("review criteria must be an object")
        criterion_results = {}
    for item in spec.get("acceptance_criteria", []):
        if item.get("priority") == "must" and criterion_results.get(item["id"]) != "pass":
            errors.append(f"review does not pass must criterion {item['id']}")
    return errors


@dataclass(frozen=True)
class SemanticStatus:
    spec_valid: bool
    verification_valid: bool
    review_valid: bool
    spec_errors: tuple[str, ...]
    verification_errors: tuple[str, ...]
    review_errors: tuple[str, ...]

    @property
    def ready_for_delivery(self) -> bool:
        return self.spec_valid and self.verification_valid and self.review_valid

    def to_dict(self) -> dict[str, Any]:
        return {
            "spec_valid": self.spec_valid,
            "verification_valid": self.verification_valid,
            "review_valid": self.review_valid,
            "ready_for_delivery": self.ready_for_delivery,
            "errors": {
                "spec": list(self.spec_errors),
                "verification": list(self.verification_errors),
                "review": list(self.review_errors),
            },
        }


def semantic_status(root: Path | str) -> SemanticStatus:
    root = Path(root).resolve()
    spec = read_spec(root)
    spec_errors = tuple(validate_spec(spec))
    verification_errors = tuple(validate_verification_plan(root, spec=spec)) if not spec_errors else ("spec invalid",)
    review_errors = tuple(validate_review_evidence(root)) if not spec_errors and not verification_errors else ("prerequisite invalid",)
    return SemanticStatus(
        spec_valid=not spec_errors,
        verification_valid=not verification_errors,
        review_valid=not review_errors,
        spec_errors=spec_errors,
        verification_errors=verification_errors,
        review_errors=review_errors,
    )


def build_clean_review_packet(root: Path | str) -> dict[str, Any]:
    root = Path(root).resolve()
    return {
        "review_contract": (
            "Review only the semantic contract, repository subject and verification traceability. "
            "Do not rely on implementation reasoning or prior claims."
        ),
        "spec": read_spec(root),
        "verification_plan": read_verification_plan(root),
        "subject_fingerprint": subject_fingerprint(root),
        "current_review": read_review_evidence(root),
    }
