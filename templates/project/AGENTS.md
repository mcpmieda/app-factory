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
8. When a meaningful API/integration/webhook/event boundary exists, follow App Factory `core/API_ENGINEERING.md`. Keep API governance proportional (`none`/`lightweight`/`contract`/`governed`), do not invent a formal API because backend code exists, and keep machine-readable contract/compatibility decisions recoverable when `contract`/`governed` applies.
9. For semantic work, follow App Factory `core/SEMANTIC_ASSURANCE.md` + `core/SEMANTIC_VERIFICATION.md`. Use `scenario` for simple isolated behavior; use `domain` when concepts/relations/roles/states/rules interact; use `formal` only when temporal, concurrent/distributed, combinatorial or critical properties justify it. For `domain`/`formal`, keep `specs/semantic-assurance.json` current against the semantic contract and use `SEMANTICS.md` only for project-specific human decisions/limits.
10. Do not implement while Semantic Assurance has deterministic contradictions, broken required refs or unresolved `blocking` questions. Z3/Alloy/FRET/P/Quint/TLA+/DMN/OPA/Cedar are conditional tools, not a universal stack.
11. Derive Independent Verification with App Factory `core/INDEPENDENT_VERIFICATION.md`. Keep simple work `baseline`; for `independent`/`adversarial`/`release`, use only applicable free/open-source checks and keep their status/target/exceptions recoverable in `VERIFICATION.md` or equivalent workflow/config.
12. For new functionality, relevant bugfixes, business rules, data/API contracts or medium/high-risk structural changes, create/update the semantic contract before implementation, derive verification traceability from its acceptance criteria, and require current review evidence before delivery. Keep docs/chores and tiny no-behavior refactors lightweight.
13. Use Execution Fabric / `execution-router`: eliminate incapable/unavailable backends first, prefer the current agent when capable, use GitHub/CI for deterministic verification, formal gates and Independent Verification when capable, and use a local/full executor only when a missing interactive/local capability or bounded fallback genuinely requires it.
14. If `.factory/learning.json` exists, Learning Engine may optimize only among already-eligible lightweight backends and only with enough samples. Capability, safety, current-task fallback, system architecture contract, API contract, Semantic Assurance, Independent Verification, semantic contract and Definition of Done always win.
15. Do not transfer routine technical work, executor choice, solver/scanner choice or next-step decisions to the user when an agent can safely perform them.
16. Reuse mature components/libraries/templates before rebuilding equivalents.
17. For projects with UI, preserve the selected design system and follow App Factory `ui/UI_POLICY.md` + `ui/PROFESSIONAL_UI_PROFILE.md` + `ui/MOTION_POLICY.md`; record `professional-default`/exceção e o project Motion Profile instead of inventing ad-hoc visual or animation rules. `professional-default` is a quality bar, not permission to mix design systems: admin/dashboard/CRUD continues to prefer shadcn with ReUI selective, while HeroUI remains an alternative when its visual language is a better fit. Use screenshot regression when a stable visual baseline exists and accidental visual change is a material risk.
18. Verify before declaring completion. Failed verification should enter bounded repair/fallback, not an unlimited retry loop. API `contract`/`governed` work must also pass proportional API gates. Formalizations/Independent Verification checks marked `required` must execute successfully or have an explicit justified exception; unavailable is not `pass`.
19. DAST/fuzz destructive checks must never target production by inference. Use disposable/local/explicitly authorized environments and fictitious test data.
20. For medium/high-risk semantic work, prefer a separate reviewer/context; when unavailable use a clean-context review that only receives the spec, current content/diff needed and executable evidence, not the implementation reasoning. Deterministic scanners/model checkers do not count as this reviewer.
21. Keep durable state recoverable from GitHub so another agent can continue without the previous chat. `.factory/state.json` may be versioned at important handoffs; `.factory/context/`, `.factory/execution.json` and `.factory/learning.json` are local/regenerable operational data and should stay outside Git by default. Semantic artifacts under `specs/` are durable/versionable when applicable. System level and authoritative data/persistence/identity/recovery decisions should also be recoverable when relevant; API mode/contract/baseline should be recoverable when `contract`/`governed` applies; semantic depth/assurance should be recoverable for `domain`/`formal`; Independent Verification mode/checks/exceptions should be recoverable when above `baseline`; UI projects should keep design system, Professional UI Profile/exceção and Motion Profile recoverable in product/architecture state.

## Project-specific rules

Add only rules that are specific to this project below. Do not duplicate the entire App Factory.

- [project-specific rules]

## Factory fallback

If the App Factory plugin is unavailable but the agent has GitHub access, consult `mcpmieda/app-factory` starting from `AGENTS.md` and `core/ENTRYPOINT.md`. For architecture/autonomy/execution/learning/semantic/API/independent verification also consult `core/SYSTEM_ENGINEERING.md`, `core/API_ENGINEERING.md`, `core/SEMANTIC_ASSURANCE.md`, `core/INDEPENDENT_VERIFICATION.md`, `core/CONTEXT_ENGINE.md`, `core/AUTONOMY_ENGINE.md`, `core/EXECUTION_FABRIC.md`, `core/LEARNING_ENGINE.md`, `core/SEMANTIC_VERIFICATION.md` and `core/TASK_ROUTER.md`. For `domain`/`formal`, use `SEMANTICS.md` as the project-specific semantic note. For UI work also consult `ui/UI_POLICY.md`, `ui/PROFESSIONAL_UI_PROFILE.md` and `ui/MOTION_POLICY.md`. Do not require the user to restate the Factory rules manually.
