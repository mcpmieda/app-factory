# AGENTS.md — Project

This project follows **App Factory** (`mcpmieda/app-factory`).

## Start here

1. If the App Factory plugin is installed, invoke/use `factory-router` for software-development work.
2. Read `PROJECT_STATE.md` before changing an existing project.
3. Read product/architecture documents only as needed for the current task.
4. Preserve local project rules and established architecture unless the task explicitly changes them.
5. Work in complete functional slices, not artificial microtasks.
6. Use the right environment: planning/research/review may stay in ChatGPT; repo execution, terminal, dependencies, build, tests, browser, debugging and migrations normally belong in Codex or an equivalent execution agent.
7. Do not transfer routine technical work to the user when an agent can safely perform it.
8. Reuse mature components/libraries/templates before rebuilding equivalents.
9. For projects with UI, preserve the selected design system and follow App Factory `ui/UI_POLICY.md` + `ui/MOTION_POLICY.md`; record the project Motion Profile instead of inventing ad-hoc animation rules.
10. Verify before declaring completion.
11. Keep state recoverable from GitHub so another agent can continue without the previous chat.

## Project-specific rules

Add only rules that are specific to this project below. Do not duplicate the entire App Factory.

- [project-specific rules]

## Factory fallback

If the App Factory plugin is unavailable but the agent has GitHub access, consult `mcpmieda/app-factory` starting from `AGENTS.md` and `core/ENTRYPOINT.md`. For UI work also consult `ui/UI_POLICY.md` and `ui/MOTION_POLICY.md`. Do not require the user to restate the Factory rules manually.