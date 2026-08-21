# PROJECT_STATE

## Objective

Implement the first complete functional slice of **Web Admin Starter**.

## Current state

- phase: bootstrap;
- App Factory profile: `web-admin`;
- Factory baseline: `v1.4.0`;
- Motion Profile: `ambient` contextual;
- authentication: not activated;
- persistence: not activated;
- advanced UI/ReUI: not activated;
- Semantic Verification: use for new functional slices, business rules, relevant bugfixes and medium/high-risk contract changes; keep docs/chores and tiny no-behavior refactors lightweight.

## Next action

Replace the starter landing page with the first product flow defined in `PRODUCT.md`, activating only the recipes that its requirements justify. Initialize/resume autonomous state so the agent can recover context, decide whether semantic specification is required, choose a capable execution backend, verify through deterministic gates and use privacy-safe local learning only after enough execution evidence exists.

When Semantic Verification applies, the agent creates and maintains `specs/semantic-contract.json`, `specs/verification-plan.json` and current review evidence; the user should not have to fill the schema manually.

Local Factory caches and learning (`.factory/context/`, `.factory/execution.json`, `.factory/learning.json`) stay outside Git by default; `.factory/state.json` may be versioned at explicit handoffs when useful. Semantic artifacts under `specs/` are durable/versionable when applicable.
