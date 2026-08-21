---
name: factory-router
description: Use whenever a user asks to create, build, design, improve, modernize, maintain, debug, automate, integrate, migrate, extend, or continue a software project, app, system, website, API, browser extension, internal tool, automation, mobile app, desktop app, or GitHub project. Also use for broad outcome-only requests such as "quero criar um sistema", "quero um app", "melhore este projeto", or "automatize este processo". This is the universal entrypoint that classifies the work, chooses the minimum necessary App Factory process, routes between ChatGPT/Codex/other agents, and activates specialized Skills without requiring the user to mention App Factory explicitly.
---

# Factory Router

This is the universal entry Skill for App Factory.

## Do not wait for the phrase "App Factory"

Activate from software-development intent itself. The user may describe only an outcome.

## Route

1. Read `core/ENTRYPOINT.md`.
2. Understand the real outcome.
3. Classify mode:
   - new project;
   - evolution/feature;
   - maintenance/refactor;
   - bug/debugging;
   - automation/integration;
   - technical research/decision.
4. If a project repository already exists, inspect its versioned state before planning from memory.
5. Classify scale with `core/PROJECT_SCALE.md`.
6. Apply `core/RISK_MODEL.md`.
7. Choose the execution environment with `core/TASK_ROUTER.md`.
8. Load only the specialized Skills needed for the current block.
9. Prefer reuse of mature solutions when appropriate.
10. Define and execute the largest safe complete functional slice possible in the current environment.

## Common routing examples

### "Quero criar um sistema de patrimônio para a escola"

- mode: new project;
- start with `app-planner`;
- determine scale and product requirements;
- make routine technical choices autonomously;
- use `ui-builder`, `architecture`, `database`, `security-review` and others only as needed;
- move to Codex when implementation requires local repo, terminal, dependencies, tests or browser verification.

### "Troque o texto desta tela"

If it is a small GitHub-verifiable edit, stay in ChatGPT when possible. Do not send to Codex just because code is involved.

### "Implemente autenticação e permissões"

Use architecture/security Skills and route implementation to Codex when executable verification is required.

## User experience contract

The user should not need to:

- name the Factory;
- choose a framework without reason;
- know which Skill to invoke;
- know whether ChatGPT or Codex is appropriate;
- repeat context already stored in GitHub;
- run commands an agent can safely run.

Tell the user when a real handoff is needed and why, in one short explanation.

## Completion

Before declaring a block complete, invoke `verification` and apply `core/DEFINITION_OF_DONE.md` proportionally to risk.