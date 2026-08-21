---
name: execution-router
description: Select the lightest execution backend that can safely implement or verify a software task, preferring the current agent and GitHub CI before escalating to a full local executor.
---

# Execution Router

Use this Skill whenever work moves from planning into implementation, verification, repair or delivery.

## Contract

1. Express the task as required capabilities, not a preferred product/agent name.
2. Ask the Execution Fabric for the lightest available capable backend.
3. Default order:
   - current agent + connected tools;
   - GitHub Actions / CI;
   - lightweight sandbox when actually available;
   - full local/interactive executor.
4. Do not route to Codex/local merely because multiple files, build or tests exist.
5. Do not keep a lighter backend when it lacks a required capability.
6. Interactive browser/shell/live migration requirements are legitimate reasons to use a full local executor.
7. Record execution outcomes so repeated backend failures can trigger a deterministic fallback.
8. Never reduce Definition of Done to avoid a more capable executor.

## GitHub CI

Treat CI as a real deterministic executor for reproducible work such as lint, typecheck, tests, build, headless browser checks and ephemeral test services.

Use only repository-owned declared/allowlisted gates. Never turn prompt text directly into shell commands.

## Human intervention

Executor failure is not automatically a user decision. Try repair/fallback first. Ask the user only when the existing Human Interaction policy says the missing decision is genuinely human.