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
5. Classify scale with `core/PROJECT_SCALE.md` and risk with `core/RISK_MODEL.md`.
6. Decide whether Semantic Verification is required before initializing a new autonomy state:
   - require it for new functionality, relevant bugfixes, business rules, data/API contracts, or medium/high-risk structural changes;
   - keep docs/chores and small no-behavior refactors lightweight.
7. Use `autonomy-engine` to resume existing state or initialize it. When the new state requires semantic proof, initialize/resume with `require_spec`; do not ask the user to choose this technical flag.
8. Select a validated project profile from `profiles/` when the product clearly matches one; do not force a profile when none fits.
9. If semantic proof is required, load `semantic-verification`: create/update the structured contract and acceptance criteria before implementation, then derive verification traceability from it.
10. Choose the execution capability with `core/TASK_ROUTER.md`: current agent + GitHub/CI first when they can prove the work; local/Codex only when genuinely needed.
11. Load only the specialized Skills needed for the current block.
12. Prefer reuse of mature solutions when appropriate.
13. Execute the largest safe complete functional slice, record the resulting autonomy event, ask the engine for `next`, and continue until done or genuinely blocked.
14. For medium/high-risk semantic work, do not let the implementing reasoning self-approve the delivery: prefer an independent reviewer/context; otherwise use the clean-context review packet built from current spec + diff + verification evidence.

## Common routing examples

### "Quero criar um sistema de patrimônio para a escola"

- mode: new project;
- likely profile: `web-admin`;
- semantic verification: required because this is a new functional system;
- initialize autonomous state from the user's outcome with semantic specification enabled;
- use `app-planner` and the validated profile to define the first complete slice;
- materialize the first slice's invariants and `given/when/then` criteria before coding;
- use only the optional modules the product actually needs;
- implement with the current agent when GitHub/CI can provide sufficient proof;
- use Codex/local only for work requiring interactive runtime, browser, debugging, migrations or capabilities unavailable in the current environment;
- verification/review/delivery are state transitions, not additional prompts the user has to request.

### "Continue este projeto"

- refresh Context Engine;
- recover `.factory/state.json` when available, otherwise infer the goal from versioned project state;
- recover semantic contract/verification artifacts when they exist;
- reconcile added/changed/removed files if the fingerprint moved;
- return to the recorded phase and continue;
- do not make the user explain the previous conversation or choose the phase.

### "Troque o texto desta tela"

If it is a simple copy-only change with no behavior/rule impact, Semantic Verification can be skipped. Stay with the current agent, make the edit and use CI when useful. Do not send to Codex merely because a source file changes.

### "Implemente autenticação e permissões"

Semantic Verification is required because security rules and observable authorization behavior matter. Define invariants/acceptance criteria before implementation. Use architecture/security Skills. Try current-agent + GitHub/CI when the environment can execute adequate integration/security gates; use a local executor when real interactive services, browser flows or migration investigation require it.

## User experience contract

The user should not need to:

- name the Factory;
- choose a framework without reason;
- decide whether a semantic-spec flag is technically needed;
- fill a technical specification schema manually;
- know which profile or Skill to invoke;
- choose ChatGPT versus Codex for routine execution;
- repeat context already recoverable from GitHub;
- say "continue" after every technical phase;
- run commands an agent can safely run.

Tell the user about a handoff only when they need to act or the handoff materially changes cost/risk.

## Completion

Writing code is not completion. When a semantic contract applies, every `must` criterion needs current executable evidence and medium/high-risk work needs decoupled review evidence. Advance through verification and review, using bounded repair on failures, then deliver only when `core/DEFINITION_OF_DONE.md` is satisfied proportionally to risk.
