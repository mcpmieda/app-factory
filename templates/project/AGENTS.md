# AGENTS.md — Project

This project follows **App Factory** (`mcpmieda/app-factory`).

## Start here

1. If the App Factory plugin is installed, invoke/use `factory-router` for software-development work.
2. Read `PROJECT_STATE.md` before changing an existing project.
3. If the V1.2 runtime is available, refresh/resume Context + Autonomy state before planning from conversation memory.
4. Read product/architecture documents only as needed for the current task; use the context map for navigation, never as authority over real files.
5. Preserve local project rules and established architecture unless the task explicitly changes them.
6. Work in complete functional slices, not artificial microtasks.
7. Use Execution Fabric / `execution-router`: prefer the current agent when capable, GitHub/CI for deterministic verification, and a local/full executor only when an unavailable interactive/local capability is genuinely required.
8. Do not transfer routine technical work, executor choice or next-step decisions to the user when an agent can safely perform them.
9. Reuse mature components/libraries/templates before rebuilding equivalents.
10. For projects with UI, preserve the selected design system and follow App Factory `ui/UI_POLICY.md` + `ui/MOTION_POLICY.md`; record the project Motion Profile instead of inventing ad-hoc animation rules.
11. Verify before declaring completion. Failed verification should enter bounded repair/fallback, not an unlimited retry loop.
12. Keep state recoverable from GitHub so another agent can continue without the previous chat. Version `.factory/state.json` at important handoffs when useful; `.factory/context/` is regenerable cache and `.factory/execution.json` is bounded execution metadata.

## Project-specific rules

Add only rules that are specific to this project below. Do not duplicate the entire App Factory.

- [project-specific rules]

## Factory fallback

If the App Factory plugin is unavailable but the agent has GitHub access, consult `mcpmieda/app-factory` starting from `AGENTS.md` and `core/ENTRYPOINT.md`. For V1.2 autonomy/execution also consult `core/CONTEXT_ENGINE.md`, `core/AUTONOMY_ENGINE.md`, `core/EXECUTION_FABRIC.md` and `core/TASK_ROUTER.md`. For UI work also consult `ui/UI_POLICY.md` and `ui/MOTION_POLICY.md`. Do not require the user to restate the Factory rules manually.
