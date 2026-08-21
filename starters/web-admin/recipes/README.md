# Web Admin Recipes

Recipes are small overlays consumed by `scripts/create-web-admin.mjs`. They are intentionally not a plugin framework.

```bash
node scripts/create-web-admin.mjs <destination> <name> \
  --recipe database-drizzle-postgres \
  --recipe auth-better-auth
```

## Available recipes

- `database-drizzle`: activates Drizzle with local SQLite for development/validation.
- `database-drizzle-postgres`: provides the same persistence capability through PostgreSQL and `DATABASE_URL`, without SQLite dependencies.
- `auth-better-auth`: activates pinned Better Auth and automatically requires the default SQLite recipe unless an explicit provider such as PostgreSQL is selected.
- `advanced-ui-reui`: records the decision and adds a focused integration guide. Components remain registry-selected because installing an entire advanced UI suite would violate the profile.

Recipes may declare a capability, conflict or small provider-specific variant. The generator resolves dependencies before writing, rejects conflicting providers safely and records the final deterministic order in `.app-factory.json`.
