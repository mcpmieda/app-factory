from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

from .ci_executor import discover_declared_gates
from .semantic_verification import read_spec, read_verification_plan, spec_fingerprint, validate_spec

SCHEMA_VERSION = 1
ASSURANCE_PATH = Path("specs/semantic-assurance.json")
DEPTHS = {"none", "scenario", "domain", "formal"}
PRIORITIES = {"must", "should", "may"}
PATTERNS = {"ubiquitous", "event", "state", "unwanted", "optional", "complex", "decision", "policy"}
QUESTION_SEVERITIES = {"blocking", "advisory"}
FORMAL_STATUSES = {"required", "advisory", "experimental"}
FORMAL_KINDS = {"z3", "alloy", "fret", "p", "quint", "tla+", "dmn", "opa", "cedar", "other"}
CONSTRAINT_KINDS = {"range", "cardinality", "enum", "requires", "forbids", "mutually-exclusive"}

ID_PATTERNS = {
    "glossary": re.compile(r"^TERM-\d{3,}$"),
    "entities": re.compile(r"^ENT-\d{3,}$"),
    "relations": re.compile(r"^REL-\d{3,}$"),
    "states": re.compile(r"^STATE-\d{3,}$"),
    "transitions": re.compile(r"^TRANS-\d{3,}$"),
    "requirements": re.compile(r"^REQ-\d{3,}$"),
    "constraints": re.compile(r"^CON-\d{3,}$"),
    "formalizations": re.compile(r"^FORM-\d{3,}$"),
    "open_questions": re.compile(r"^Q-\d{3,}$"),
}

VAGUE_PATTERNS = (
    re.compile(r"\b(fast|quick|quickly|large|small|appropriate|reasonable|user[- ]friendly|etc\.?|as needed)\b", re.I),
    re.compile(r"\b(r[aá]pid[oa]?|rapidamente|grande|pequen[oa]|adequad[oa]|razo[aá]vel|amig[aá]vel|etc\.?|quando necess[aá]rio|o m[aá]ximo poss[ií]vel)\b", re.I),
)


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def assurance_path(root: Path | str) -> Path:
    return Path(root).resolve() / ASSURANCE_PATH


def read_assurance(root: Path | str) -> dict[str, Any] | None:
    path = assurance_path(root)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def write_assurance(root: Path | str, assurance: dict[str, Any]) -> None:
    path = assurance_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(assurance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def new_assurance(spec: dict[str, Any], *, depth: str = "domain") -> dict[str, Any]:
    if depth not in DEPTHS:
        raise ValueError(f"Unsupported semantic depth: {depth}")
    errors = validate_spec(spec)
    if errors:
        raise ValueError("Invalid semantic spec: " + "; ".join(errors))
    return {
        "schema_version": SCHEMA_VERSION,
        "depth": depth,
        "source_contract_fingerprint": spec_fingerprint(spec),
        "glossary": [],
        "entities": [],
        "relations": [],
        "states": [],
        "transitions": [],
        "requirements": [],
        "constraints": [],
        "formalizations": [],
        "open_questions": [],
        "coverage_exceptions": [],
    }


def recommend_semantic_depth(
    *,
    semantic_required: bool,
    system_level: str = "local-app",
    risk: str = "low",
    interacting_rules: bool = False,
    domain_entities: bool = False,
    roles_or_permissions: bool = False,
    stateful_workflow: bool = False,
    temporal_requirements: bool = False,
    concurrency_or_distribution: bool = False,
    safety_critical: bool = False,
) -> str:
    if not semantic_required:
        return "none"
    if safety_critical or (risk == "high" and (temporal_requirements or concurrency_or_distribution)):
        return "formal"
    if (
        interacting_rules
        or domain_entities
        or roles_or_permissions
        or stateful_workflow
        or system_level in {"multi-user-system", "production-system", "critical-system"}
    ):
        return "domain"
    return "scenario"


def _list_of_objects(value: Any, label: str, errors: list[str]) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return []
    result: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{label}[{index}] must be an object")
            continue
        result.append(item)
    return result


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and all(_nonempty_string(item) for item in value)


def _collect_ids(items: list[dict[str, Any]], label: str, errors: list[str]) -> set[str]:
    pattern = ID_PATTERNS[label]
    found: set[str] = set()
    for index, item in enumerate(items):
        item_id = item.get("id")
        if not isinstance(item_id, str) or not pattern.fullmatch(item_id):
            errors.append(f"{label}[{index}].id must match {pattern.pattern}")
            continue
        if item_id in found:
            errors.append(f"duplicate {label} id: {item_id}")
        found.add(item_id)
    return found


def _coverage_exception_ids(assurance: dict[str, Any]) -> set[str]:
    value = assurance.get("coverage_exceptions", [])
    if not isinstance(value, list):
        return set()
    result: set[str] = set()
    for item in value:
        if isinstance(item, dict) and _nonempty_string(item.get("criterion")) and _nonempty_string(item.get("reason")):
            result.add(item["criterion"])
    return result


def _vague_findings(requirement: dict[str, Any]) -> list[str]:
    texts: list[str] = []
    for key in ("component", "trigger", "timing"):
        value = requirement.get(key)
        if isinstance(value, str):
            texts.append(value)
    for key in ("scope", "preconditions", "response"):
        value = requirement.get(key)
        if isinstance(value, list):
            texts.extend(str(item) for item in value if isinstance(item, str))
    joined = " ".join(texts)
    hits: set[str] = set()
    for pattern in VAGUE_PATTERNS:
        for match in pattern.finditer(joined):
            hits.add(match.group(0))
    req_id = requirement.get("id", "unknown")
    return [f"{req_id}: vague term requires review: {term}" for term in sorted(hits, key=str.lower)]


def validate_assurance(
    root: Path | str,
    *,
    assurance: dict[str, Any] | None = None,
    spec: dict[str, Any] | None = None,
) -> tuple[list[str], list[str]]:
    root = Path(root).resolve()
    assurance = assurance if assurance is not None else read_assurance(root)
    spec = spec if spec is not None else read_spec(root)
    errors: list[str] = []
    warnings: list[str] = []

    spec_errors = validate_spec(spec)
    if spec_errors:
        return ["spec: " + error for error in spec_errors], warnings
    assert spec is not None

    if not isinstance(assurance, dict):
        return ["semantic assurance is missing or invalid JSON"], warnings
    if assurance.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    depth = assurance.get("depth")
    if depth not in DEPTHS:
        errors.append(f"depth must be one of {sorted(DEPTHS)}")
    if assurance.get("source_contract_fingerprint") != spec_fingerprint(spec):
        errors.append("semantic assurance is stale: source_contract_fingerprint does not match current semantic contract")

    collections: dict[str, list[dict[str, Any]]] = {}
    ids: dict[str, set[str]] = {}
    for label in ID_PATTERNS:
        collections[label] = _list_of_objects(assurance.get(label, []), label, errors)
        ids[label] = _collect_ids(collections[label], label, errors)

    glossary_terms: dict[str, str] = {}
    for index, item in enumerate(collections["glossary"]):
        term = item.get("term")
        definition = item.get("definition")
        if not _nonempty_string(term):
            errors.append(f"glossary[{index}].term is required")
        if not _nonempty_string(definition):
            errors.append(f"glossary[{index}].definition is required")
        aliases = item.get("aliases", [])
        if not _string_list(aliases):
            errors.append(f"glossary[{index}].aliases must be an array of non-empty strings")
        if isinstance(term, str):
            canonical = term.casefold().strip()
            if canonical in glossary_terms:
                errors.append(f"duplicate glossary term: {term} conflicts with {glossary_terms[canonical]}")
            glossary_terms[canonical] = str(item.get("id", term))

    for index, item in enumerate(collections["entities"]):
        if not _nonempty_string(item.get("name")):
            errors.append(f"entities[{index}].name is required")
        if not _nonempty_string(item.get("definition")):
            errors.append(f"entities[{index}].definition is required")
        attributes = item.get("attributes", [])
        if not isinstance(attributes, list):
            errors.append(f"entities[{index}].attributes must be an array")

    for index, item in enumerate(collections["relations"]):
        source = item.get("from")
        target = item.get("to")
        if source not in ids["entities"]:
            errors.append(f"relations[{index}].from references unknown entity: {source}")
        if target not in ids["entities"]:
            errors.append(f"relations[{index}].to references unknown entity: {target}")
        if not _nonempty_string(item.get("name")):
            errors.append(f"relations[{index}].name is required")
        min_value = item.get("min")
        max_value = item.get("max")
        if min_value is not None and (not isinstance(min_value, int) or min_value < 0):
            errors.append(f"relations[{index}].min must be a non-negative integer or null")
        if max_value is not None and (not isinstance(max_value, int) or max_value < 0):
            errors.append(f"relations[{index}].max must be a non-negative integer or null")
        if isinstance(min_value, int) and isinstance(max_value, int) and min_value > max_value:
            errors.append(f"{item.get('id')}: impossible cardinality min {min_value} > max {max_value}")

    for index, item in enumerate(collections["states"]):
        if not _nonempty_string(item.get("name")):
            errors.append(f"states[{index}].name is required")

    for index, item in enumerate(collections["transitions"]):
        if item.get("from") not in ids["states"]:
            errors.append(f"transitions[{index}].from references unknown state: {item.get('from')}")
        if item.get("to") not in ids["states"]:
            errors.append(f"transitions[{index}].to references unknown state: {item.get('to')}")
        refs = item.get("requirement_refs", [])
        if not _string_list(refs):
            errors.append(f"transitions[{index}].requirement_refs must be an array of requirement ids")
        else:
            for ref in refs:
                if ref not in ids["requirements"]:
                    errors.append(f"transitions[{index}] references unknown requirement: {ref}")

    acceptance_ids = {
        item.get("id")
        for item in spec.get("acceptance_criteria", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    must_acceptance_ids = {
        item.get("id")
        for item in spec.get("acceptance_criteria", [])
        if isinstance(item, dict) and item.get("priority") == "must" and isinstance(item.get("id"), str)
    }
    invariant_ids = {
        item.get("id")
        for item in spec.get("invariants", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    concept_ids = ids["glossary"] | ids["entities"] | ids["states"]

    acceptance_to_requirements: dict[str, set[str]] = {}
    invariant_to_requirements: dict[str, set[str]] = {}
    concept_to_requirements: dict[str, set[str]] = {}

    for index, item in enumerate(collections["requirements"]):
        req_id = item.get("id")
        if item.get("priority") not in PRIORITIES:
            errors.append(f"requirements[{index}].priority must be one of {sorted(PRIORITIES)}")
        if item.get("pattern") not in PATTERNS:
            errors.append(f"requirements[{index}].pattern must be one of {sorted(PATTERNS)}")
        if not _nonempty_string(item.get("component")):
            errors.append(f"requirements[{index}].component is required")
        for key in ("scope", "preconditions", "response", "concept_refs", "acceptance_refs", "invariant_refs", "formalization_refs"):
            if not _string_list(item.get(key, [])):
                errors.append(f"requirements[{index}].{key} must be an array of non-empty strings")
        response = item.get("response", [])
        if not isinstance(response, list) or not response:
            errors.append(f"requirements[{index}].response must contain at least one expected response")
        if item.get("pattern") in {"event", "unwanted", "complex", "decision", "policy"} and not _nonempty_string(item.get("trigger")):
            errors.append(f"requirements[{index}].trigger is required for pattern {item.get('pattern')}")

        for ref in item.get("concept_refs", []) if isinstance(item.get("concept_refs"), list) else []:
            if ref not in concept_ids:
                errors.append(f"{req_id}: unknown concept ref {ref}")
            else:
                concept_to_requirements.setdefault(ref, set()).add(str(req_id))
        for ref in item.get("acceptance_refs", []) if isinstance(item.get("acceptance_refs"), list) else []:
            if ref not in acceptance_ids:
                errors.append(f"{req_id}: unknown acceptance ref {ref}")
            else:
                acceptance_to_requirements.setdefault(ref, set()).add(str(req_id))
        for ref in item.get("invariant_refs", []) if isinstance(item.get("invariant_refs"), list) else []:
            if ref not in invariant_ids:
                errors.append(f"{req_id}: unknown invariant ref {ref}")
            else:
                invariant_to_requirements.setdefault(ref, set()).add(str(req_id))
        for ref in item.get("formalization_refs", []) if isinstance(item.get("formalization_refs"), list) else []:
            if ref not in ids["formalizations"]:
                errors.append(f"{req_id}: unknown formalization ref {ref}")
        if depth in {"domain", "formal"} and item.get("priority") == "must" and not item.get("acceptance_refs"):
            errors.append(f"{req_id}: must requirement needs at least one acceptance_ref")
        warnings.extend(_vague_findings(item))

    exceptions = _coverage_exception_ids(assurance)
    if depth in {"domain", "formal"}:
        for criterion_id in sorted(must_acceptance_ids):
            if criterion_id not in acceptance_to_requirements and criterion_id not in exceptions:
                errors.append(f"{criterion_id}: must acceptance criterion has no requirement origin")

    requirement_pairs: dict[tuple[str, str], set[str]] = {}
    for index, item in enumerate(collections["constraints"]):
        kind = item.get("kind")
        if kind not in CONSTRAINT_KINDS:
            errors.append(f"constraints[{index}].kind must be one of {sorted(CONSTRAINT_KINDS)}")
            continue
        con_id = item.get("id")
        if kind == "range":
            min_value = item.get("min")
            max_value = item.get("max")
            if min_value is None and max_value is None:
                errors.append(f"{con_id}: range needs min and/or max")
            if min_value is not None and not isinstance(min_value, (int, float)):
                errors.append(f"{con_id}: range min must be numeric")
            if max_value is not None and not isinstance(max_value, (int, float)):
                errors.append(f"{con_id}: range max must be numeric")
            if isinstance(min_value, (int, float)) and isinstance(max_value, (int, float)) and min_value > max_value:
                errors.append(f"{con_id}: impossible range min {min_value} > max {max_value}")
        elif kind == "cardinality":
            relation = item.get("relation")
            if relation not in ids["relations"]:
                errors.append(f"{con_id}: cardinality references unknown relation {relation}")
            min_value = item.get("min")
            max_value = item.get("max")
            if min_value is not None and (not isinstance(min_value, int) or min_value < 0):
                errors.append(f"{con_id}: cardinality min must be non-negative integer or null")
            if max_value is not None and (not isinstance(max_value, int) or max_value < 0):
                errors.append(f"{con_id}: cardinality max must be non-negative integer or null")
            if isinstance(min_value, int) and isinstance(max_value, int) and min_value > max_value:
                errors.append(f"{con_id}: impossible cardinality min {min_value} > max {max_value}")
        elif kind == "enum":
            allowed = item.get("allowed", [])
            forbidden = item.get("forbidden", [])
            if not isinstance(allowed, list) or not isinstance(forbidden, list):
                errors.append(f"{con_id}: enum allowed/forbidden must be arrays")
            elif allowed and set(map(str, allowed)).issubset(set(map(str, forbidden))):
                errors.append(f"{con_id}: enum forbids every allowed value")
        elif kind in {"requires", "forbids", "mutually-exclusive"}:
            source = item.get("source")
            target = item.get("target")
            if source not in ids["requirements"]:
                errors.append(f"{con_id}: constraint source references unknown requirement {source}")
            if target not in ids["requirements"]:
                errors.append(f"{con_id}: constraint target references unknown requirement {target}")
            if isinstance(source, str) and isinstance(target, str):
                pair = (source, target)
                requirement_pairs.setdefault(pair, set()).add(str(kind))

    for pair, kinds in requirement_pairs.items():
        if "requires" in kinds and ("forbids" in kinds or "mutually-exclusive" in kinds):
            errors.append(f"requirements {pair[0]} -> {pair[1]} are simultaneously required and forbidden/exclusive")

    known_gates = {gate.gate_id for gate in discover_declared_gates(root)}
    all_source_ids = ids["requirements"] | invariant_ids | acceptance_ids
    formal_kinds_present: set[str] = set()
    for index, item in enumerate(collections["formalizations"]):
        kind = item.get("kind")
        if kind not in FORMAL_KINDS:
            errors.append(f"formalizations[{index}].kind must be one of {sorted(FORMAL_KINDS)}")
        else:
            formal_kinds_present.add(str(kind))
        status = item.get("status")
        if status not in FORMAL_STATUSES:
            errors.append(f"formalizations[{index}].status must be one of {sorted(FORMAL_STATUSES)}")
        source_refs = item.get("source_refs", [])
        if not _string_list(source_refs) or not source_refs:
            errors.append(f"formalizations[{index}].source_refs must contain requirement/invariant/acceptance refs")
        else:
            for ref in source_refs:
                if ref not in all_source_ids:
                    errors.append(f"formalizations[{index}] references unknown source {ref}")
        artifact = item.get("artifact")
        if not _nonempty_string(artifact):
            errors.append(f"formalizations[{index}].artifact is required")
        elif not (root / artifact).is_file():
            errors.append(f"formalizations[{index}].artifact does not exist: {artifact}")
        gate = item.get("gate")
        if status == "required":
            if not _nonempty_string(gate):
                errors.append(f"formalizations[{index}] required formalization needs a declared gate")
            elif gate not in known_gates:
                errors.append(f"formalizations[{index}] references undeclared gate {gate}")

    for index, item in enumerate(collections["open_questions"]):
        if item.get("severity") not in QUESTION_SEVERITIES:
            errors.append(f"open_questions[{index}].severity must be one of {sorted(QUESTION_SEVERITIES)}")
        if not _nonempty_string(item.get("text")):
            errors.append(f"open_questions[{index}].text is required")
        refs = item.get("requirement_refs", [])
        if not _string_list(refs):
            errors.append(f"open_questions[{index}].requirement_refs must be an array")
        else:
            for ref in refs:
                if ref not in ids["requirements"]:
                    errors.append(f"open_questions[{index}] references unknown requirement {ref}")
        if item.get("severity") == "blocking":
            errors.append(f"{item.get('id')}: blocking semantic question unresolved: {item.get('text')}")

    if depth == "formal" and not formal_kinds_present:
        warnings.append("formal depth selected but no formalization artifact is registered yet")

    return errors, sorted(set(warnings))


def _plan_gate_map(plan: dict[str, Any] | None) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    if not isinstance(plan, dict):
        return result
    rows = plan.get("criteria", [])
    if not isinstance(rows, list):
        return result
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            continue
        gates: set[str] = set()
        evidence = row.get("evidence", [])
        if isinstance(evidence, list):
            for item in evidence:
                if isinstance(item, dict) and isinstance(item.get("gate"), str):
                    gates.add(item["gate"])
        result[row["id"]] = gates
    return result


def coverage_report(root: Path | str, *, assurance: dict[str, Any] | None = None, spec: dict[str, Any] | None = None) -> dict[str, Any]:
    root = Path(root).resolve()
    assurance = assurance if assurance is not None else read_assurance(root)
    spec = spec if spec is not None else read_spec(root)
    if not isinstance(assurance, dict) or not isinstance(spec, dict):
        return {"available": False}

    requirements = [item for item in assurance.get("requirements", []) if isinstance(item, dict)]
    must_requirements = [item for item in requirements if item.get("priority") == "must"]
    must_criteria = [item for item in spec.get("acceptance_criteria", []) if isinstance(item, dict) and item.get("priority") == "must"]
    invariants = [item for item in spec.get("invariants", []) if isinstance(item, dict)]

    req_with_acceptance = [item for item in must_requirements if item.get("acceptance_refs")]
    criterion_refs = {
        ref
        for req in requirements
        for ref in req.get("acceptance_refs", [])
        if isinstance(ref, str)
    }
    invariant_refs = {
        ref
        for req in requirements
        for ref in req.get("invariant_refs", [])
        if isinstance(ref, str)
    }
    plan_map = _plan_gate_map(read_verification_plan(root))
    criteria_with_evidence = [item for item in must_criteria if plan_map.get(item.get("id"))]

    return {
        "available": True,
        "must_requirements": {
            "total": len(must_requirements),
            "with_acceptance_refs": len(req_with_acceptance),
        },
        "must_acceptance_criteria": {
            "total": len(must_criteria),
            "with_requirement_origin": sum(1 for item in must_criteria if item.get("id") in criterion_refs),
            "with_executable_gate": len(criteria_with_evidence),
        },
        "invariants": {
            "total": len(invariants),
            "referenced_by_requirements": sum(1 for item in invariants if item.get("id") in invariant_refs),
        },
        "note": "Structural traceability coverage; 100% does not prove semantic correctness.",
    }


def formal_method_recommendations(assurance: dict[str, Any]) -> list[dict[str, str]]:
    requirements = [item for item in assurance.get("requirements", []) if isinstance(item, dict)]
    constraints = [item for item in assurance.get("constraints", []) if isinstance(item, dict)]
    relations = [item for item in assurance.get("relations", []) if isinstance(item, dict)]
    transitions = [item for item in assurance.get("transitions", []) if isinstance(item, dict)]
    depth = assurance.get("depth")
    recommendations: list[dict[str, str]] = []

    if constraints:
        recommendations.append({"kind": "z3", "reason": "structured business constraints can benefit from satisfiability/counterexample checking"})
    if relations and any(item.get("min") is not None or item.get("max") is not None for item in relations):
        recommendations.append({"kind": "alloy", "reason": "relational/cardinality domain model can benefit from bounded counterexample search"})
    if any(item.get("timing") for item in requirements):
        recommendations.append({"kind": "fret", "reason": "temporal requirement detected; FRET-style formalization can clarify timing semantics"})
    if transitions:
        recommendations.append({"kind": "stateful-property", "reason": "state transitions detected; generate operation sequences and check invariants"})
        if depth == "formal":
            recommendations.append({"kind": "p-or-quint", "reason": "formal state-machine exploration is appropriate at formal depth"})
    if any(item.get("pattern") == "decision" for item in requirements):
        recommendations.append({"kind": "dmn", "reason": "decision-oriented requirements may be clearer as executable decision tables"})
    access_policy_signal = re.compile(
        r"\b(authorization|authorisation|autorização|autorizacao|permission|permissão|permissao|"
        r"access control|controle de acesso|rbac|abac|role|roles|papel|papéis|papeis|tenant|"
        r"least privilege|menor privilégio|menor privilegio|escopo de acesso)\b",
        re.I,
    )
    policy_requirements = [item for item in requirements if item.get("pattern") == "policy"]
    policy_texts: list[str] = []
    for item in policy_requirements:
        pieces: list[str] = []
        for key in ("component", "trigger", "timing"):
            value = item.get(key)
            if isinstance(value, str):
                pieces.append(value)
        for key in ("scope", "preconditions", "response"):
            value = item.get(key)
            if isinstance(value, list):
                pieces.extend(str(entry) for entry in value if isinstance(entry, str))
        policy_texts.append(" ".join(pieces))
    if any(access_policy_signal.search(value) for value in policy_texts):
        recommendations.append({
            "kind": "opa-or-cedar",
            "reason": "explicit authorization/access-control policy signals detected; policy-as-code may improve reviewability",
        })
    return recommendations


def analyze_assurance(root: Path | str) -> dict[str, Any]:
    root = Path(root).resolve()
    assurance = read_assurance(root)
    spec = read_spec(root)
    errors, warnings = validate_assurance(root, assurance=assurance, spec=spec)
    return {
        "schema_version": SCHEMA_VERSION,
        "ready": not errors,
        "errors": errors,
        "warnings": warnings,
        "coverage": coverage_report(root, assurance=assurance, spec=spec),
        "formal_method_recommendations": formal_method_recommendations(assurance or {}),
        "assurance_fingerprint": _canonical_hash(assurance) if assurance is not None else None,
        "contract_fingerprint": spec_fingerprint(spec) if isinstance(spec, dict) and not validate_spec(spec) else None,
    }


def _indexed(items: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(items, list):
        return {}
    return {
        item["id"]: item
        for item in items
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _changed_ids(old_items: Any, new_items: Any) -> dict[str, list[str]]:
    old = _indexed(old_items)
    new = _indexed(new_items)
    old_ids = set(old)
    new_ids = set(new)
    changed = sorted(item_id for item_id in old_ids & new_ids if _canonical_hash(old[item_id]) != _canonical_hash(new[item_id]))
    return {
        "added": sorted(new_ids - old_ids),
        "removed": sorted(old_ids - new_ids),
        "changed": changed,
    }


def semantic_diff(
    old: dict[str, Any],
    new: dict[str, Any],
    *,
    verification_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    sections = ("glossary", "entities", "relations", "states", "transitions", "requirements", "constraints", "formalizations")
    changes = {section: _changed_ids(old.get(section, []), new.get(section, [])) for section in sections}

    impacted_requirements: set[str] = set(changes["requirements"]["added"] + changes["requirements"]["removed"] + changes["requirements"]["changed"])
    changed_concepts = set()
    for section in ("glossary", "entities", "states"):
        changed_concepts.update(changes[section]["added"] + changes[section]["removed"] + changes[section]["changed"])

    old_requirements = _indexed(old.get("requirements", []))
    new_requirements = _indexed(new.get("requirements", []))
    for req_id, item in {**old_requirements, **new_requirements}.items():
        refs = set(item.get("concept_refs", [])) if isinstance(item.get("concept_refs"), list) else set()
        if refs & changed_concepts:
            impacted_requirements.add(req_id)

    changed_relations = set(changes["relations"]["added"] + changes["relations"]["removed"] + changes["relations"]["changed"])
    for con in list(_indexed(old.get("constraints", [])).values()) + list(_indexed(new.get("constraints", [])).values()):
        if con.get("relation") in changed_relations:
            for key in ("source", "target"):
                if isinstance(con.get(key), str):
                    impacted_requirements.add(con[key])

    impacted_acceptance: set[str] = set()
    impacted_invariants: set[str] = set()
    for req_id in impacted_requirements:
        for source in (old_requirements.get(req_id), new_requirements.get(req_id)):
            if not isinstance(source, dict):
                continue
            impacted_acceptance.update(ref for ref in source.get("acceptance_refs", []) if isinstance(ref, str))
            impacted_invariants.update(ref for ref in source.get("invariant_refs", []) if isinstance(ref, str))

    gate_map = _plan_gate_map(verification_plan)
    impacted_gates = sorted({gate for criterion in impacted_acceptance for gate in gate_map.get(criterion, set())})

    return {
        "changed": any(any(bucket for bucket in value.values()) for value in changes.values()),
        "sections": changes,
        "impact": {
            "requirements": sorted(impacted_requirements),
            "acceptance_criteria": sorted(impacted_acceptance),
            "invariants": sorted(impacted_invariants),
            "gates": impacted_gates,
        },
        "old_fingerprint": _canonical_hash(old),
        "new_fingerprint": _canonical_hash(new),
    }


def load_json(path: Path | str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("expected a JSON object")
    return value


def save_json(path: Path | str, value: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
