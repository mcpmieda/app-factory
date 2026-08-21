# Better Auth schema maintenance contract

Supported and tested baseline: `better-auth@1.7.1` with the matching `auth@1.7.1` CLI. Both versions are pinned by the recipe and must move together.

## Detect and review change

1. Update both pins on a dedicated branch; do not silently upgrade an existing generated application because the starter baseline changed.
2. Run `npm run auth:schema:check`. The command asks the pinned Better Auth CLI for its current Drizzle contract and fails when tables, columns, indexes or provider differ from the versioned schema.
3. Generate the candidate schema to a review file with `npx auth@1.7.1 generate --config src/lib/auth.ts --output auth-schema.candidate.ts --yes`, substituting the proposed version when upgrading.
4. Review the schema diff and create a new Drizzle migration. Never edit or reorder an already-applied migration in a real project.
5. Inspect SQL for dropped tables/columns, narrowing types, rewritten identifiers and irreversible data conversion. A destructive migration must not run automatically without an explicit data recovery/backfill plan.
6. Verify migration, idempotent seed, login/session and application queries against an ephemeral database before publishing the recipe update.

## Compatibility rule

The Factory baseline controls only newly generated projects. A real project owns its installed Better Auth version, schema and migration history; it upgrades deliberately and may remain on an older supported baseline. Recipe evolution must add migrations and tests rather than rewriting project history.
