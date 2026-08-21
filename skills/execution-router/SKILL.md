---
name: execution-router
description: Select a safe capable execution backend, preferring current-agent/GitHub CI baseline and applying privacy-safe learned evidence only after capability, availability, fallback and risk filters.
---

# Execution Router

Use this Skill whenever work moves from planning into implementation, verification, repair or delivery.

## Contract

1. Express the task as required capabilities, not a preferred product/agent name.
2. Eliminate unavailable, incapable or current-task-failed backends first.
3. Preserve all safety/risk/Definition of Done constraints.
4. If enough local learning evidence exists, allow it to reorder only the remaining lightweight candidates.
5. Otherwise use the baseline order:
   - current agent + connected tools;
   - GitHub Actions / CI;
   - lightweight sandbox when actually available;
   - full local/interactive executor.
6. Do not route to Codex/local merely because multiple files, build or tests exist.
7. Do not keep a lighter backend when it lacks a required capability.
8. Interactive browser/shell/live migration requirements are legitimate reasons to use a full local executor.
9. Record execution outcomes so current-task failures can trigger deterministic fallback and privacy-safe local learning can accumulate across tasks.
10. Never reduce Definition of Done to optimize speed or executor use.

## Learning guard

Learning is optimization, not authority. It cannot:

- resurrect a backend rejected by capability/fallback;
- grant permissions/secrets;
- promote `local_full` over an eligible lightweight backend only because of score;
- use prompt/code/log/file content as training data.

When samples are insufficient, keep the V1.2 baseline. See `core/LEARNING_ENGINE.md` and `skills/learning-engine/SKILL.md`.

## GitHub CI

Treat CI as a real deterministic executor for reproducible work such as lint, typecheck, tests, build, headless browser checks and ephemeral test services.

Use only repository-owned declared/allowlisted gates. Never turn prompt text directly into shell commands.

## Human intervention

Executor failure is not automatically a user decision. Try repair/fallback first. Ask the user only when the existing Human Interaction policy says the missing decision is genuinely human.
