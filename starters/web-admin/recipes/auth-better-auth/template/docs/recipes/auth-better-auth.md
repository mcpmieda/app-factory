# Better Auth recipe

Better Auth is active because this project requires identity. Signup remains disabled in the running app; only the idempotent local seed enables account creation.

Protected reads and every mutation must call `requireSession()` on the server. Never rely only on hiding client UI.

The runtime and matching `auth` CLI are pinned at 1.7.1. Run `npm run auth:schema:check` after installation or dependency changes and follow `auth-schema-maintenance.md` before creating a migration. An explicitly selected provider such as `database-drizzle-postgres` satisfies the database capability without adding SQLite.
