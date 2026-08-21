# AGENTS.md — Cadastro de Aluno

This project follows App Factory (`mcpmieda/app-factory`).

## Start here

1. Read `PROJECT_STATE.md` before changing the project.
2. Use App Factory `factory-router` for software-development work.
3. Preserve the selected design system: HeroUI v3.
4. Follow App Factory `ui/UI_POLICY.md` and `ui/MOTION_POLICY.md`.
5. Work in complete functional slices.
6. Verify before declaring completion.

## Project-specific rules

- Product profile: `web-admin`, simplified for a small single-page administrative flow.
- Design system: HeroUI v3 only; do not mix shadcn/ReUI into this project without an explicit product reason.
- Persistence: browser `localStorage` only in this demo baseline.
- No authentication or backend is part of the current scope.
- Motion Profile: `ambient`, attenuated to subtle around the data list.
- `prefers-reduced-motion` is mandatory.
- Validation contract: Zod.
- Critical flow: one-step student registration + duplicate registration prevention + local persistence.
