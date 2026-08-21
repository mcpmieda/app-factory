# Drizzle recipe

This project uses Drizzle because it owns persistent data. SQLite/better-sqlite3 is configured only for local validation; select a provider compatible with the real deployment before production.

Run `npm run setup` after installation. Migrations belong in `drizzle/` and must remain versioned.
