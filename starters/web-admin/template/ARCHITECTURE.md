# Architecture

## Baseline

- Next.js App Router + React + TypeScript;
- Tailwind CSS + shadcn/ui;
- Zod at input/configuration boundaries;
- Vitest and Playwright;
- Server Components and Server Actions when sufficient.

## Optional modules

- `auth-better-auth`: identity and protected operations;
- `database-drizzle`: local/test SQLite persistence;
- `database-drizzle-postgres`: PostgreSQL persistence for production-style environments;
- `advanced-ui-reui`: selective advanced administrative components.

Do not add client state, form, observability or monorepo layers until a concrete flow needs them.
