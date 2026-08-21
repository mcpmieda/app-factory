# Architecture

## Baseline

- Next.js App Router + React + TypeScript;
- Tailwind CSS + shadcn/ui;
- Motion Profile: `ambient` contextual per App Factory `ui/MOTION_POLICY.md`;
- Zod at input/configuration boundaries;
- Vitest and Playwright;
- Server Components and Server Actions when sufficient.

## Motion

- use semantic motion for interaction, data, state, attention and navigation;
- use ambient backgrounds/effects only where they do not compete with dense administrative content;
- attenuate to `subtle` in dense tables/reading-heavy views;
- support `prefers-reduced-motion` for non-essential movement;
- do not add another design system only for animation.

## Optional modules

- `auth-better-auth`: identity and protected operations;
- `database-drizzle`: local/test SQLite persistence;
- `database-drizzle-postgres`: PostgreSQL persistence for production-style environments;
- `advanced-ui-reui`: selective advanced administrative components.

Do not add client state, form, observability, motion library or monorepo layers until a concrete flow needs them.
