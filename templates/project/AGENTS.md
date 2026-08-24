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
8. When a meaningful API/integration/webhook/event boundary exists, follow App Factory `core/API_ENGINEERING.md`. Keep API governance proportional (`none`/`lightweight`/`contract`/`governed`) and keep machine-readable contract/compatibility decisions recoverable when applicable.
9. For semantic work, follow App Factory `core/SEMANTIC_ASSURANCE.md` + `core/SEMANTIC_VERIFICATION.md`. Use proportional semantic depth and keep project-specific semantic artifacts recoverable when required.
10. Do not implement while Semantic Assurance has deterministic contradictions, broken required refs or unresolved `blocking` questions. Formal tools are conditional, not a universal stack.
11. Derive Independent Verification with App Factory `core/INDEPENDENT_VERIFICATION.md`. Keep simple work `baseline`; above baseline use only applicable checks and keep status/target/exceptions recoverable.
12. For new functionality, relevant bugfixes, business rules, data/API contracts or medium/high-risk structural changes, create/update the semantic contract before implementation, derive verification traceability from acceptance criteria, and require current review evidence before delivery. Keep docs/chores and tiny no-behavior refactors lightweight.
13. Use Execution Fabric / `execution-router`: eliminate incapable/unavailable backends first, prefer the current agent when capable, use GitHub/CI for deterministic verification, and use a local/full executor only when a missing interactive/local capability genuinely requires it.
14. If `.factory/learning.json` exists, Learning Engine may optimize only among already-eligible lightweight backends and only with enough samples. Capability, safety and architecture contracts always win.
15. Do not transfer routine technical work, executor choice, solver/scanner choice or next-step decisions to the user when an agent can safely perform them.
16. Reuse mature components/libraries/templates before rebuilding equivalents.
17. For projects with UI, preserve the selected design system and follow App Factory `ui/UI_POLICY.md` + `ui/PROFESSIONAL_UI_PROFILE.md` + `ui/MOTION_POLICY.md`. When `ambient-constellation` is active, also follow `ui/AMBIENT_CONSTELLATION_PROFILE.md`. Requests such as `ambient constellation`, `ambient constellarion` or `ambiente de constelação` activate it with `strong` intensity. **A new system whose primary design system is HeroUI inherits `ambient-constellation strong` automatically**, unless the user explicitly opts out or a real product/accessibility/platform constraint requires an exception. Dense content stays in clean surfaces while constellation remains in shell/header/perimeter; reduced motion uses a static constellation fallback. `professional-default` remains a quality bar, not permission to mix design systems. Use screenshot regression when a stable visual baseline exists and accidental visual change is a material risk.
18. Verify before declaring completion. Failed verification should enter bounded repair/fallback, not an unlimited retry loop. Required formal/Independent Verification gates must execute successfully or have an explicit justified exception; unavailable is not `pass`.
19. DAST/fuzz destructive checks must never target production by inference. Use disposable/local/explicitly authorized environments and fictitious test data.
20. For medium/high-risk semantic work, prefer a separate reviewer/context; when unavailable use a clean-context review with only the spec, current content/diff and executable evidence, not implementation reasoning.
21. Keep durable state recoverable from GitHub so another agent can continue without the previous chat. UI projects should keep design system, Professional UI Profile/exceção, Motion Profile and any Ambient Surface Profile recoverable in product/architecture state.

## Change Hygiene for existing code

Whenever this project is maintained, repaired, modernized or reviewed, follow App Factory `core/CHANGE_HYGIENE.md` whether the project was originally created by App Factory or imported later.

- preserve stable behavior, not obsolete implementation;
- prefer one active source of truth per responsibility;
- do not leave `old/new/fixed/final/copy/v2` shadow implementations without a real compatibility boundary;
- after repair/debug loops, consolidate the working solution and remove discarded attempts, dead code, orphan imports/dependencies, temporary files, unnecessary suppressions and CSS override layers;
- dual paths are allowed only for real compatibility/migration and must have an objective removal condition plus transition tests;
- run `scripts/change_hygiene.py` from the App Factory when available; objective blockers must be resolved and advisories reviewed contextually;
- run regression checks again after consolidation, because cleanup is part of the delivered implementation.

The final tree should look like the implementation we would have chosen if we had known the successful solution from the start; the Git history/PR stores the attempts.

## Project-specific rules

Add only rules that are specific to this project below. Do not duplicate the entire App Factory.

- [project-specific rules]

## Factory fallback

If the App Factory plugin is unavailable but the agent has GitHub access, consult `mcpmieda/app-factory` starting from `AGENTS.md` and `core/ENTRYPOINT.md`. For maintenance/review also consult `core/CHANGE_HYGIENE.md`. For architecture/autonomy/execution/learning/semantic/API/independent verification consult the corresponding Core contracts as needed. For UI work consult `ui/UI_POLICY.md`, `ui/PROFESSIONAL_UI_PROFILE.md`, `ui/MOTION_POLICY.md` and, when active or when HeroUI is the primary system, `ui/AMBIENT_CONSTELLATION_PROFILE.md`. Do not require the user to restate the Factory rules manually.
