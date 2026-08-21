# Pulse Desk

Fictitious App Factory `web-admin` generated from the V0.7 baseline to validate Living UI / Semantic Motion. It intentionally excludes authentication, persistence and additional UI or motion libraries because they do not contribute to this validation.

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

The Playwright matrix covers desktop, mobile and a desktop context with `prefers-reduced-motion: reduce`.

Create a named project from the repository root with `node scripts/create-web-admin.mjs <destination> <name>`.
