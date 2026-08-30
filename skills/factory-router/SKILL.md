---
name: factory-router
description: Use only when the user explicitly asks to use App Factory or when the current repository explicitly declares active App Factory governance. Do not activate from software-development intent alone. Route only the App Factory modules that are proportionate and actually needed for the requested change.
---

# Factory Router

The Factory Router is an **opt-in** entry skill.

## Activation

Use it only when:

- the user explicitly asks for App Factory; or
- the repository currently declares `governance: "app-factory"` and the user has not opted out.

Do not infer active governance from historical `.factory` files, old specs, past PRs, or the mere presence of App Factory code.

## Default route

1. Read `core/ENTRYPOINT.md`.
2. Understand the requested result.
3. Inspect only the relevant project context.
4. Classify the **change itself** as trivial, local, domain, or critical.
5. Select only the modules needed for that change.
6. Implement the smallest safe complete solution.
7. Run proportional validation.

## Proportionality

- **trivial**: local checks only when useful;
- **local**: normal lint/typecheck/tests/build for affected code;
- **domain**: add business-rule/API/persistence verification that is actually relevant;
- **critical**: use stronger security, migration, recovery or integration gates for the affected surface.

Do not automatically materialize Project Adoption, Semantic Assurance, Semantic Verification, Independent Verification, formal methods, merge trains, scanner matrices, handoff documents, or autonomy state.

## Existing projects

If a repository says App Factory governance is disabled or optional, follow the repository's normal workflow instead. The latest explicit project/user decision wins over historical Factory artifacts.

## Safety

Opt-in governance does not relax concrete security controls. Preserve secrets, PII boundaries, server-side authorization, safe migrations, and explicit authorization for destructive or production-impacting operations.

## Completion

Finish when the requested behavior is implemented and the checks proportionate to the changed surface pass. Do not add process artifacts solely to satisfy the existence of this skill.
