# AGENTS.md — Project

This project follows **App Factory** (`mcpmieda/app-factory`).

## Start here

1. If the App Factory plugin is installed, invoke/use `factory-router` for software-development work.
2. Read `PROJECT_STATE.md` before changing an existing project.
3. Refresh/resume Context + Autonomy state before planning from conversation memory when the runtime is available.
4. Read product/architecture documents only as needed for the current task; use the context map for navigation, never as authority over real files.
5. Preserve local project rules and established architecture unless the task explicitly changes them.
6. Work in complete functional slices, not artificial microtasks.
7. Classify the product with App Factory `core/SYSTEM_ENGINEERING.md`. For `persistent-app` or above, keep the authoritative data source durable and explicit. For `multi-user-system` or above, do not substitute browser-only persistence/client-only authorization for the required shared/server-side architecture.
8. For new functionality, relevant bugfixes, business rules, data/API contracts or medium/high-risk structural changes, follow App Factory `core/SEMANTIC_VERIFICATION.md`: create/update the semantic contract before implementation, derive verification traceability from its acceptance criteria, and require current review evidence before delivery. Keep docs/chores and tiny no-behavior refactors lightweight.
9. Use Execution Fabric / `execution-router`: eliminate incapable/unavailable backends first, prefer the current agent when capable, use GitHub/CI for deterministic verification, and use a local/full executor only when a missing interactive/local capability or bounded fallback genuinely requires it.
10. If `.factory/learning.json` exists, Learning Engine may optimize only among already-eligible lightweight backends and only with enough samples. Capability, safety, current-task fallback, system architecture contract, semantic contract and Definition of Done always win.
11. Do not transfer routine technical work, executor choice or next-step decisions to the user when an agent can safely perform them.
12. Reuse mature components/libraries/templates before rebuilding equivalents.
13. For projects with UI, preserve the selected design system and follow App Factory `ui/UI_POLICY.md` + `ui/MOTION_POLICY.md`; record the project Motion Profile instead of inventing ad-hoc animation rules. Use screenshot regression when a stable visual baseline exists and accidental visual change is a material risk.
14. Verify before declaring completion. Failed verification should enter bounded repair/fallback, not an unlimited retry loop.
15. For medium/high-risk semantic work, prefer a separate reviewer/context; when unavailable use a clean-context review that only receives the spec, current content/diff needed and executable evidence, not the implementation reasoning.
16. Keep durable state recoverable from GitHub so another agent can continue without the previous chat. `.factory/state.json` may be versioned at important handoffs; `.factory/context/`, `.factory/execution.json` and `.factory/learning.json` are local/regenerable operational data and should stay outside Git by default. Semantic artifacts under `specs/` are durable/versionable when applicable. System level and authoritative data/persistence/identity/recovery decisions should also be recoverable when relevant.

## Project-specific rules

Add only rules that are specific to this project below. Do not duplicate the entire App Factory.

- [project-specific rules]

## Factory fallback

If the App Factory plugin is unavailable but the agent has GitHub access, consult `mcpmieda/app-factory` starting from `AGENTS.md` and `core/ENTRYPOINT.md`. For architecture/autonomy/execution/learning/semantic verification also consult `core/SYSTEM_ENGINEERING.md`, `core/CONTEXT_ENGINE.md`, `core/AUTONOMY_ENGINE.md`, `core/EXECUTION_FABRIC.md`, `core/LEARNING_ENGINE.md`, `core/SEMANTIC_VERIFICATION.md` and `core/TASK_ROUTER.md`. For UI work also consult `ui/UI_POLICY.md` and `ui/MOTION_POLICY.md`. Do not require the user to restate the Factory rules manually.
