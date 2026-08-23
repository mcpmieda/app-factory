# Architecture

## Baseline

- Next.js App Router + React + TypeScript;
- Tailwind CSS + shadcn/ui;
- ReUI only when a justified advanced administrative component reduces work;
- Professional UI Profile: `professional-default` per App Factory `ui/PROFESSIONAL_UI_PROFILE.md`;
- default density/surface/emphasis for data-heavy admin: `comfortable + layered + balanced`, adjusted when the product requires it;
- Motion Profile: `ambient` contextual per App Factory `ui/MOTION_POLICY.md`;
- Zod at input/configuration boundaries;
- Vitest and Playwright;
- Server Components and Server Actions when sufficient.

## Professional UI

- shadcn/ui remains the visual foundation;
- ReUI remains a selective source of advanced admin patterns, not a second required design system;
- `professional-default` is a quality bar, not a package or permission to mix design systems;
- before medium/large UI work, inventory the actual archetypes: shell, page header, stats, search/command, filters, data view, form, detail/inspector and feedback states;
- reuse current shadcn/ReUI components before creating equivalents;
- maintain coherent hierarchy, spacing, typography, surfaces, radius/elevation, semantic color and density;
- implement loading, empty, error, disabled, success and destructive-action states when relevant;
- mobile layout must reorganize dense data instead of only shrinking desktop;
- HeroUI or another design system requires a real product-level visual decision, not an isolated desire for prettier components;
- commercial references may inspire composition, but proprietary templates/assets/code are not copied without an applicable project license.

## Motion

- use semantic motion for interaction, data, state, attention and navigation;
- use ambient backgrounds/effects only where they do not compete with dense administrative content;
- attenuate to `subtle` in dense tables/reading-heavy views;
- support `prefers-reduced-motion` for non-essential movement;
- do not add another design system only for animation.

## Visual QA

When UI is materially changed, verify proportionally:

- desktop and mobile viewport;
- keyboard/focus;
- loading/empty/error states;
- primary and destructive actions;
- overflow/clipping;
- reduced motion;
- console without relevant errors;
- screenshot regression only when a stable baseline exists and visual regression is a material risk.

## Optional modules

- `auth-better-auth`: identity and protected operations;
- `database-drizzle`: local/test SQLite persistence;
- `database-drizzle-postgres`: PostgreSQL persistence for production-style environments;
- `advanced-ui-reui`: selective advanced administrative components.

Do not add client state, form, observability, motion library or monorepo layers until a concrete flow needs them.
