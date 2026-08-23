# AGENTS.md — Gestão de Alunos

This project follows App Factory (`mcpmieda/app-factory`).

## Start here

1. Read `PROJECT_STATE.md`.
2. Use App Factory `factory-router` for software-development work.
3. Preserve HeroUI v3 as the selected design system.
4. Follow `ui/UI_POLICY.md` and `ui/MOTION_POLICY.md`.
5. For functional changes, keep `specs/semantic-contract.json`, Semantic Assurance and verification evidence current.
6. Work in complete functional slices and verify before completion.

## Project-specific rules

- System level: `local-app`.
- Public Vercel hosting does **not** imply shared persistence or a server-side product.
- Authoritative data source: browser `localStorage` under the versioned storage contract.
- API mode: `none` unless a real independent integration/consumer is introduced.
- No backend, database or authentication should be added only to make the architecture look more sophisticated.
- Existing v1 local records must remain recoverable through the versioned migration path.
- Unknown legacy values must remain unknown (`not_informed`), never fabricated.
- Backup restore validates the whole document before it can replace local data and requires explicit confirmation.
- Motion Profile: `ambient`, attenuated to `subtle` around dense data.
- `prefers-reduced-motion` is mandatory.
- Validation contract: Zod.
