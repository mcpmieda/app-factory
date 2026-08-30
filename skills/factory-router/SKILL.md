---
name: factory-router
description: Use only when the user explicitly asks to use App Factory or when the current repository explicitly declares active App Factory governance. Do not activate from software-development intent alone. Route only the modules proportionate to the requested change.
---

# Factory Router

The Factory Router is opt-in.

## Activation

Use it only when the user explicitly requests App Factory or the repository currently declares `governance: "app-factory"` without a later opt-out. Historical Factory files do not reactivate governance.

## Route

1. Read `core/ENTRYPOINT.md`.
2. Understand the requested result.
3. Inspect only relevant context.
4. Classify the change itself as trivial, local, domain, or critical.
5. Select only the modules needed for that change.
6. Implement the smallest safe complete solution.
7. Run proportional validation.

Do not automatically create adoption state, semantic specs, verification matrices, merge trains, handoffs, or autonomy artifacts.

## Optional modules retained for compatibility

The `project-adoption` module and `core/PROJECT_ADOPTION_GATE.md` remain available when explicitly selected. Its `pre-implementation` and `delivery` phases are not universal requirements. The historical `React + custom/native CSS` rule belongs only to that optional module.

Optional routing metrics continue to use `scripts/skill_routing.py` as advisory aggregate telemetry; the existing privacy rule is: never include prompt/task text.

## Existing projects

If a repository declares Factory governance disabled or optional, follow the repository's normal workflow. The latest explicit project/user decision wins over historical artifacts.

## Completion

Finish when the requested behavior is implemented and checks proportionate to the affected surface pass. Do not add process artifacts just because this skill exists.
