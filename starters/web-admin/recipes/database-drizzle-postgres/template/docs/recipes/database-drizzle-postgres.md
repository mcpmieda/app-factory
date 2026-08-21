# PostgreSQL + Drizzle recipe

This recipe selects PostgreSQL as the `database-drizzle` capability. It removes the need for SQLite dependencies and persists exclusively through `DATABASE_URL`.

Use a least-privilege PostgreSQL role and inject the URL through the deployment environment. Run `npm run db:migrate` as a controlled release step before starting the new application version. Review generated SQL before applying destructive changes; never automate a destructive migration solely because Drizzle generated it.

For a production-readiness smoke test:

1. set `DATABASE_URL`;
2. run `npm run setup` and `npm run db:smoke`;
3. run the normal checks and `npm run build`;
4. run `npm run start:smoke` against the production build.

No local file database is used by this provider.
