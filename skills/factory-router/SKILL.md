---
name: factory-router
description: Use whenever a user asks to create, build, design, improve, modernize, maintain, debug, automate, integrate, migrate, extend, or continue a software project, app, system, website, API, browser extension, internal tool, automation, mobile app, desktop app, or GitHub project. Also use for broad outcome-only requests such as "quero criar um sistema", "quero um app", "melhore este projeto", or "automatize este processo". This is the universal entrypoint that recovers incremental context and autonomous state, classifies architecture/API/risk, selects proportional semantic assurance/verification and independent verification, routes execution capabilities, and activates specialized Skills without requiring the user to mention App Factory explicitly.
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
5. For any existing-code evolution, maintenance, refactor, debugging, modernization or review, apply `core/CHANGE_HYGIENE.md`; load `maintenance` when code/config/styles are being changed. This applies equally to Factory-built and external projects. Preserve stable behavior, not obsolete implementation; a repair loop must end in consolidation, not stacked patches.
6. Classify three independent axes before architecture: process scale with `core/PROJECT_SCALE.md`, risk with `core/RISK_MODEL.md`, and product/system level with `core/SYSTEM_ENGINEERING.md`.
7. For `persistent-app` or above, identify the authoritative data source. Do not let browser-local storage, mocks or static JSON become the final shared persistence by convenience.
8. For `multi-user-system` or above, derive server-side/backend, durable shared persistence, identity/auth, authorization, validation, migrations and recovery needs before choosing a simplified implementation.
9. If there is a meaningful API/integration/webhook/event boundary, apply `core/API_ENGINEERING.md`; classify API governance as `none`, `lightweight`, `contract` or `governed`, then load `api-engineering` when API-specific design/implementation is in scope. Do not formalize an API only because a backend exists.
10. Decide whether Semantic Verification is required before initializing a new autonomy state:
   - require it for new functionality, relevant bugfixes, business rules, data/API contracts, or medium/high-risk structural changes;
   - keep docs/chores and small no-behavior refactors lightweight.
11. If Semantic Verification is required, derive **semantic depth** with `core/SEMANTIC_ASSURANCE.md`:
   - `scenario` for small/isolated behavior where invariants + `given/when/then` are sufficient;
   - `domain` when multiple concepts, relations, roles, states or rules interact;
   - `formal` only when temporal requirements, concurrency/distribution, large combinatorial constraints, policy complexity or criticality justify formal analysis.
12. Load `semantic-assurance` for `domain`/`formal`. Create/update `specs/semantic-assurance.json`, run deterministic consistency/coverage analysis and resolve `blocking` questions before implementation. Select Z3/Alloy/FRET/P/Quint/TLA+/DMN/OPA/Cedar only by problem fit; never install all by default.
13. Derive Independent Verification from risk + system level + API mode using `core/INDEPENDENT_VERIFICATION.md`. Keep simple work `baseline`; load `independent-verification` when the mode becomes `independent`, `adversarial` or `release`.
14. Use `autonomy-engine` to resume existing state or initialize it. When the new state requires semantic proof, initialize/resume with `require_spec`; do not ask the user to choose this technical flag.
15. Select a validated project profile from `profiles/` when the product clearly matches one; do not force a profile when none fits. A profile can provide defaults but cannot reduce `core/SYSTEM_ENGINEERING.md`, applicable `core/API_ENGINEERING.md`, Semantic Assurance/Verification, Independent Verification or Change Hygiene requirements.
16. If semantic proof is required, load `semantic-verification`: create/update the structured contract and acceptance criteria before implementation, then derive verification traceability from it. In `domain`/`formal`, Semantic Assurance must be ready against the current contract fingerprint first.
17. Choose the execution capability with `core/TASK_ROUTER.md`: current agent + GitHub/CI first when they can prove the work; local/Codex only when genuinely needed. Independent/adversarial/formal checks should prefer GitHub CI or an equivalent deterministic free runner when capable.
18. Load only the specialized Skills needed for the current block.
19. Once the routing decision has explicitly selected specialized Skills, record only their installed slugs when the local Factory CLI is available: `python scripts/skill_routing.py --root <project> record --skill <slug> ...`. This is advisory aggregate telemetry only; never include prompt/task text and never block work if local routing telemetry is unavailable.
20. Prefer reuse of mature solutions when appropriate.
21. Execute the largest safe complete functional slice, record the resulting autonomy event, ask the engine for `next`, and continue until done or genuinely blocked.
22. During verification, execute the selected independent/adversarial matrix in addition to implementation-authored tests when applicable.
23. When existing code was changed, run the Change Hygiene consolidation pass after successful repair/verification, remove discarded attempts/orphan residue, review advisories, then rerun applicable regressions before final review.
24. When a semantic model changes, use semantic diff to identify impacted requirements, acceptance criteria, invariants and declared gates before accepting prior evidence as current.
25. For medium/high-risk semantic work, do not let the implementing reasoning self-approve the delivery: prefer an independent reviewer/context; otherwise use the clean-context review packet built from current spec + diff + verification evidence. Deterministic/formal tools are complementary evidence, not a semantic reviewer.

## Common routing examples

### "Quero criar um sistema de patrimônio para a escola"

- mode: new project;
- likely scale: M or above depending on operation/impact;
- likely system level: `multi-user-system` or `production-system`, not `local-app`;
- likely profile: `web-admin`;
- authoritative data must be shared/durable, not browser-only;
- API governance is evaluated from actual consumers/integrations; a Next.js server boundary does not automatically require public OpenAPI;
- semantic verification: required because this is a new functional system;
- semantic depth: likely `domain`, because assets, users, custody/status/history and authorization rules interact;
- `semantic-assurance` models only domain concepts/relations/rules that affect behavior, not every noun in the UI;
- Independent Verification: normally `adversarial` for a real multi-user institutional system, with only technically applicable motors activated;
- initialize autonomous state from the user's outcome with semantic specification enabled;
- use `app-planner` and the validated profile to define the first complete slice;
- derive persistence, identity, authorization, server-side validation and recovery needs from the actual operation;
- materialize requirements/invariants and `given/when/then` criteria before coding;
- use only the optional modules the product actually needs;
- implement with the current agent when GitHub/CI can provide sufficient proof;
- verification/review/delivery are state transitions, not additional prompts the user has to request.

### "Quero uma calculadora pessoal que funcione offline"

- likely system level: `local-app`;
- browser/device-local persistence can be authoritative if the requirement is truly local;
- API governance: `none` unless a real external integration exists;
- semantic depth: `scenario` if there is meaningful behavior to specify;
- Independent Verification: usually `baseline`;
- do not introduce backend/database/auth/OpenAPI/Alloy/TLA+/SAST/DAST/mutation tooling only to imitate an enterprise architecture.

### "Crie uma API para web + app mobile + extensão"

- API governance: at least `contract`, potentially `governed` by risk/exposure;
- load `api-engineering`;
- choose protocol from requirements instead of forcing REST;
- define machine-readable source of truth before clients depend on undocumented behavior;
- add compatibility/runtime/security gates proportionally;
- semantic depth is independent: a simple resource API may stay `scenario`; interacting authorization/workflow/domain rules may require `domain`;
- Independent Verification can add Schemathesis, security scanning and DAST when applicable without duplicating the API contract;
- use Semantic Verification for business behavior and critical interface invariants without copying the whole API schema into the semantic spec.

### "Continue este projeto"

- refresh Context Engine;
- recover `.factory/state.json` when available, otherwise infer the goal from versioned project state;
- recover semantic contract, semantic-assurance model, verification artifacts and `SEMANTICS.md` when they exist;
- recover recorded system level/data-source decisions, API governance/contract decisions and `VERIFICATION.md`/independent mode when present;
- apply Change Hygiene when the continuation edits existing code, even if the project predates App Factory;
- validate assurance/contract fingerprints before trusting prior analysis;
- reconcile semantic diff and added/changed/removed files if fingerprints moved;
- return to the recorded phase and continue;
- do not make the user explain the previous conversation or choose the phase.

### "Troque o texto desta tela"

If it is a simple copy-only change with no behavior/rule impact, Semantic Assurance/Verification and Independent Verification can remain lightweight/baseline. Stay with the current agent, make the edit and use CI when useful. Do not send to Codex merely because a source file changes. If the edit touches existing code/style structure, Change Hygiene still forbids leaving temporary copies or override residue, but stays lightweight.

### "Corrija este projeto legado que não foi criado pela App Factory"

- recover the real repository baseline and execution path first;
- do not require App Factory historical artifacts to begin;
- load `maintenance` and apply `core/CHANGE_HYGIENE.md` to the touched area;
- characterize the stable behavior that must survive;
- do not rewrite unrelated legacy debt merely to make the repository look new;
- do not imitate existing debt by adding another override/wrapper/shadow function;
- after repair, consolidate to one current implementation unless a real compatibility boundary requires two paths;
- rerun regressions after cleanup.

### "Implemente autenticação e permissões"

Semantic Verification is required because security rules and observable authorization behavior matter. For a few simple roles, `scenario` may suffice; interacting scopes, ownership or policy rules elevate to `domain`. Define invariants/acceptance criteria before implementation. Use architecture/security Skills. Authorization must be enforced server-side where protected operations exist. Complex declarative policy may justify OPA/Rego or Cedar, but neither is mandatory. If the authorization is exposed through an API boundary, `api-engineering` also defines contract/error/security gates. Independent Verification should add appropriate negative/security evidence when technically applicable.

## User experience contract

The user should not need to:

- name the Factory;
- choose a framework without reason;
- classify the technical system level manually;
- classify API governance manually;
- choose semantic depth manually;
- choose Z3/Alloy/FRET/P/TLA+/DMN/policy engines manually;
- choose mutation/SAST/DAST tools manually;
- decide whether a semantic-spec flag is technically needed;
- fill a technical specification schema manually;
- know which profile or Skill to invoke;
- choose ChatGPT versus Codex for routine execution;
- repeat context already recoverable from GitHub;
- say "continue" after every technical phase;
- run commands an agent can safely run.

Tell the user about a handoff only when they need to act or the handoff materially changes cost/risk.

## Completion

Writing code is not completion. `core/SYSTEM_ENGINEERING.md` requirements are architecture gates, not suggestions. A `multi-user-system` or higher cannot be called production-ready while authoritative data is browser-only, authorization is client-only, required migrations/recovery are absent, or real persistence/protected flows have not been exercised. When `core/API_ENGINEERING.md` applies in `contract`/`governed` mode, contract validity, compatibility, runtime correspondence and security evidence also become proportional gates. When Semantic Assurance depth is `domain`/`formal`, unresolved deterministic contradictions, broken refs, `blocking` questions or required formalizations/gates prevent specification readiness. When `core/INDEPENDENT_VERIFICATION.md` selects `required` adversarial checks, those checks must execute successfully or have an explicit justified exception; tool unavailability is not a pass. When a semantic contract applies, every `must` criterion also needs current executable evidence and medium/high-risk work needs decoupled review evidence. Existing-code work additionally must satisfy `core/CHANGE_HYGIENE.md`: a bug disappearing is not completion if the final tree still depends on discarded attempts, shadow implementations, unnecessary override layers or temporary residue. Advance through verification, consolidation and review, using bounded repair on failures, then deliver only when `core/DEFINITION_OF_DONE.md` is satisfied proportionally to risk.
