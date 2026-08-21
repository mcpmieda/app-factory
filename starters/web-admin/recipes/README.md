# Web Admin Recipes

Recipes are small overlays consumed by `scripts/create-web-admin.mjs`. They are intentionally not a plugin framework.

```bash
node scripts/create-web-admin.mjs <destination> <name> \
  --recipe database-drizzle \
  --recipe auth-better-auth
```

## Available recipes

- `database-drizzle`: activates Drizzle with local SQLite for development/validation. Select a production provider before deployment.
- `auth-better-auth`: activates Better Auth and automatically requires `database-drizzle`.
- `advanced-ui-reui`: records the decision and adds a focused integration guide. Components remain registry-selected because installing an entire advanced UI suite would violate the profile.

Each generated project records applied recipes in `.app-factory.json`.
