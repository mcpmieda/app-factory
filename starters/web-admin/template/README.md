# Web Admin Starter

Clean App Factory `web-admin` foundation. It intentionally excludes authentication, persistence, ReUI, Biome, form/state libraries, observability, analytics and monorepo tooling.

## Requirements

- Node.js 22–24;
- npm 10.9.9.

## Start

```bash
npm ci
npm run dev
```

## Verification

```bash
npm run format:check
npm run lint
npm run typecheck
npm run test:coverage
npm run build
npm audit --audit-level=high
npx playwright install chromium
npm run e2e
```

Create a named project from the repository root with `node scripts/create-web-admin.mjs <destination> <name>`.
