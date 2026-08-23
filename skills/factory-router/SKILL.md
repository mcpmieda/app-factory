---
name: factory-router
description: Use whenever a user asks to create, build, design, improve, modernize, maintain, debug, automate, integrate, migrate, extend, or continue a software project, app, system, website, API, browser extension, internal tool, automation, mobile app, desktop app, or GitHub project. Also use for broad outcome-only requests such as "quero criar um sistema", "quero um app", "melhore este projeto", or "automatize este processo". This is the universal entrypoint that recovers incremental context and autonomous state, classifies the work, selects a validated profile when appropriate, chooses proportional semantic verification, routes execution capabilities, and activates specialized Skills without requiring the user to mention App Factory explicitly.
---

# Factory Router

This is the universal entry Skill for App Factory.

## Do not wait for the phrase "App Factory"

Activate from software-development intent itself. The user may describe only an outcome.

## Route

1. Read `core/ENTRYPOINT.md`.
2. Understand the real outcome.
3. Classify mode: new project, evolution/feature, maintenance/refactor, bug/debugging, automation/integration, or technical research/decision.
4. If a project repository already exists, use `context-engine` to refresh the incremental repository map and inspect authoritative state instead of planning from chat memory.
5. Classify three independent axes before architecture: process scale with `core/PROJECT_SCALE.md`, risk with `core/RISK_MODEL.md`, and product/system level with `core/SYSTEM_ENGINEERING.md`.
6. For `persistent-app` or above, identify the authoritative data source. Do not let browser-local storage, mocks or static JSON become the final shared persistence by convenience.
7. For `multi-user-system` or above, derive server-side/backend, durable shared persistence, identity/auth, authorization, validation, migrations and recovery needs before choosing a simplified implementation.
8. If there is a meaningful API/integration/webhook/event boundary, apply `core/API_ENGINEERING.md`; classify API governance as `none`, `lightweight`, `contract` or `governed`, then load `api-engineering` when API-specific design/implementation is in scope. Do not formalize an API only because a backend exists.
9. Decide whether Semantic Verification is required before initializing a new autonomy state:
   - require it for new functionality, relevant bugfixes, business rules, data/API contracts, or medium/high-risk structural changes;
   - keep docs/chores and small no-behavior refactors lightweight.
10. Use `autonomy-engine` to resume existing state or initialize it. When the new state requires semantic proof, initialize/resume with `require_spec`; do not ask the user to choose this technical flag.
11. Select a validated project profile from `profiles/` when the product clearly matches one; do not force a profile when none fits. A profile can provide defaults but cannot reduce `core/SYSTEM_ENGINEERING.md` or applicable `core/API_ENGINEERING.md` requirements.
12. If semantic proof is required, load `semantic-verification`: create/update the structured contract and acceptance criteria before implementation, then derive verification traceability from it.
13. Choose the execution capability with `core/TASK_ROUTER.md`: current agent + GitHub/CI first when they can prove the work; local/Codex only when genuinely needed.
14. Load only the specialized Skills needed for the current block.
15. Prefer reuse of mature solutions when appropriate.
16. Execute the largest safe complete functional slice, record the resulting autonomy event, ask the engine for `next`, and continue until done or genuinely blocked.
17. For medium/high-risk semantic work, do not let the implementing reasoning self-approve the delivery: prefer an independent reviewer/context; otherwise use the clean-context review packet built from current spec + diff + verification evidence.

## Common routing examples

### "Quero criar um sistema de patrimônio para a escola"

- mode: new project;
- likely scale: M or above depending on operation/impact;
- likely system level: `multi-user-system` or `production-system`, not `local-app`;
- likely profile: `web-admin`;
- authoritative data must be shared/durable, not browser-only;
- API governance is evaluated from actual consumers/integrations; a Next.js server boundary does not automatically require public OpenAPI;
- semantic verification: required because this is a new functional system;
- initialize autonomous state from the user's outcome with semantic specification enabled;
- use `app-planner` and the validated profile to define the first complete slice;
- derive persistence, identity, authorization, server-side validation and recovery needs from the actual operation;
- materialize the first slice's invariants and `given/when/then` criteria before coding;
- use only the optional modules the product actually needs;
- implement with the current agent when GitHub/CI can provide sufficient proof;
- use Codex/local only for work requiring interactive runtime, browser, debugging, migrations or capabilities unavailable in the current environment;
- verification/review/delivery are state transitions, not additional prompts the user has to request.

### "Quero uma calculadora pessoal que funcione offline"

- likely system level: `local-app`;
- browser/device-local persistence can be authoritative if the requirement is truly local;
- API governance: `none` unless a real external integration exists;
- do not introduce backend/database/auth/OpenAPI only to imitate an enterprise architecture.

### "Crie uma API para web + app mobile + extensão"

- API governance: at least `contract`, potentially `governed` by risk/exposure;
- load `api-engineering`;
- choose protocol from requirements instead of forcing REST;
- define machine-readable source of truth before clients depend on undocumented behavior;
- add compatibility/runtime/security gates proportionally;
- use Semantic Verification for business behavior and critical interface invariants without copying the whole API schema into the semantic spec.

### "Continue este projeto"

- refresh Context Engine;
- recover `.factory/state.json` when available, otherwise infer the goal from versioned project state;
- recover semantic contract/verification artifacts when they exist;
- recover recorded system level/data-source decisions and API governance/contract decisions when present;
- reconcile added/changed/removed files if the fingerprint moved;
- return to the recorded phase and continue;
- do not make the user explain the previous conversation or choose the phase.

### "Troque o texto desta tela"

If it is a simple copy-only change with no behavior/rule impact, Semantic Verification can be skipped. Stay with the current agent, make the edit and use CI when useful. Do not send to Codex merely because a source file changes.

### "Implemente autenticação e permissões"

Semantic Verification is required because security rules and observable authorization behavior matter. Define invariants/acceptance criteria before implementation. Use architecture/security Skills. Authorization must be enforced server-side where protected operations exist. If the authorization is exposed through an API boundary, `api-engineering` also defines contract/error/security gates. Try current-agent + GitHub/CI when the environment can execute adequate integration/security gates; use a local executor when real interactive services, browser flows or migration investigation require it.

## User experience contract

The user should not need to:

- name the Factory;
- choose a framework without reason;
- classify the technical system level manually;
- classify API governance manually;
- decide whether a semantic-spec flag is technically needed;
- fill a technical specification schema manually;
- know which profile or Skill to invoke;
- choose ChatGPT versus Codex for routine execution;
- repeat context already recoverable from GitHub;
- say "continue" after every technical phase;
- run commands an agent can safely run.

Tell the user about a handoff only when they need to act or the handoff materially changes cost/risk.

## Completion

Writing code is not completion. `core/SYSTEM_ENGINEERING.md` requirements are architecture gates, not suggestions. A `multi-user-system` or higher cannot be called production-ready while authoritative data is browser-only, authorization is client-only, required migrations/recovery are absent, or real persistence/protected flows have not been exercised. When `core/API_ENGINEERING.md` applies in `contract`/`governed` mode, contract validity, compatibility, runtime correspondence and security evidence also become proportional gates. When a semantic contract applies, every `must` criterion also needs current executable evidence and medium/high-risk work needs decoupled review evidence. Advance through verification and review, using bounded repair on failures, then deliver only when `core/DEFINITION_OF_DONE.md` is satisfied proportionally to risk.
