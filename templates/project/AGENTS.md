# AGENTS.md — Project

This project follows **App Factory** (`mcpmieda/app-factory`).

## Start here

1. If the App Factory plugin is installed, invoke/use `factory-router` for software-development work.
2. Before the first functional/visual implementation of a material block, read `core/PROJECT_ADOPTION_GATE.md`, load `project-adoption`, materialize/update `.app-factory.json`, and require the `pre-implementation` gate to be green.
3. Read `PROJECT_STATE.md` before changing an existing project.
4. Refresh/resume Context + Autonomy state before planning from conversation memory when the runtime is available.
5. Read product/architecture documents only as needed for the current task; use the context map for navigation, never as authority over real files.
6. Preserve local project rules and established architecture unless the task explicitly changes them.
7. Work in complete functional slices, not artificial microtasks.
8. Classify the product with App Factory `core/SYSTEM_ENGINEERING.md`. For `persistent-app` or above, keep the authoritative data source durable and explicit. For `multi-user-system` or above, do not substitute browser-only persistence/client-only authorization for the required shared/server-side architecture.
9. For `persistent-app` or above, identify operations whose interruption could cause partial effects, duplicate writes, inconsistent state or lost progress. Once such a command is accepted server-side, its critical state must not depend on the browser remaining open; use proportional durable status, checkpoint, idempotency, reconciliation or retomada according to `core/SYSTEM_ENGINEERING.md`.
10. When a meaningful API/integration/webhook/event boundary exists, follow App Factory `core/API_ENGINEERING.md` with proportional governance.
11. For semantic work, follow App Factory `core/SEMANTIC_ASSURANCE.md` + `core/SEMANTIC_VERIFICATION.md`. Use proportional semantic depth and materialize required specifications before implementation.
12. Derive Independent Verification with App Factory `core/INDEPENDENT_VERIFICATION.md`; keep simple work `baseline` and use only applicable checks above baseline.
13. Use Execution Fabric / `execution-router` to select a capable executor without transferring routine technical choices to the user.
14. Reuse mature components/libraries/templates before rebuilding equivalents.
15. For projects with UI, preserve the selected design system and follow `ui/UI_POLICY.md`, `ui/PROFESSIONAL_UI_PROFILE.md` and `ui/MOTION_POLICY.md`. The design system must be recorded in `.app-factory.json` before UI code. In `web-admin`, shadcn/ui is the validated default; React + CSS/custom/native UI as the visual foundation requires an explicit documented deviation. HeroUI, when selected, is used transversally and does not imply any mandatory environmental effect.
16. Verify before declaring completion. Failed verification should enter bounded repair/fallback, not an unlimited retry loop.
17. Keep durable state recoverable from GitHub so another agent can continue without the previous chat. UI projects should keep design system, Professional UI Profile and Motion Profile recoverable in project state. Critical-operation recovery decisions must also remain recoverable in architecture/state when material.
18. Before delivery, run `project_adoption_gate.py check --phase delivery` or prove the equivalent checklist when the script cannot run.

## Change Hygiene for existing code

Whenever this project is maintained, repaired, modernized or reviewed, follow App Factory `core/CHANGE_HYGIENE.md` whether the project was originally created by App Factory or imported later.

- preserve stable behavior, not obsolete implementation;
- prefer one active source of truth per responsibility;
- do not leave shadow implementations without a real compatibility boundary;
- after repair/debug loops, consolidate the working solution and remove discarded attempts, dead code, orphan imports/dependencies, temporary files and unnecessary override layers;
- dual paths are allowed only for real compatibility/migration and must have an objective removal condition plus transition tests;
- run regression checks again after consolidation, because cleanup is part of the delivered implementation.

The final tree should look like the implementation we would have chosen if we had known the successful solution from the start; the Git history/PR stores the attempts.

## Project-specific rules

Add only rules that are specific to this project below. Do not duplicate the entire App Factory.

- [project-specific rules]

## Factory fallback

If the App Factory plugin is unavailable but the agent has GitHub access, consult `mcpmieda/app-factory` starting from `AGENTS.md`, `core/ENTRYPOINT.md` and `core/PROJECT_ADOPTION_GATE.md`. For maintenance/review also consult `core/CHANGE_HYGIENE.md`. For architecture/autonomy/execution/learning/semantic/API/independent verification consult the corresponding Core contracts as needed. For UI work consult `ui/UI_POLICY.md`, `ui/PROFESSIONAL_UI_PROFILE.md` and `ui/MOTION_POLICY.md`. Do not require the user to restate the Factory rules manually.
