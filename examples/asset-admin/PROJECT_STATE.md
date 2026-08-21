# PROJECT_STATE

## Objective

Validate a second `web-admin` application created from the V0.5 starter for fictitious school asset management.

## Current state

- phase: validation implementation;
- App Factory profile: `web-admin`;
- Factory baseline: `v0.5`;
- generated from: `starters/web-admin/template/`;
- recipes: `database-drizzle`, `auth-better-auth`;
- authentication: Better Auth, local seeded account, protected server operations;
- persistence: Drizzle + SQLite/better-sqlite3 for local validation only;
- advanced UI/ReUI: not activated; current list complexity does not justify it;
- data: fictitious only.

## Verification target

Clean install, setup/migrations/idempotent seed, format, lint, artifact-independent typecheck, unit coverage, build, high/critical audit gate and Playwright desktop/mobile for the critical lifecycle.

## Next action

Review the V0.5 validation evidence before promoting the generated starter to stable V1. Select a real production database/provider only when a deployment target exists.
