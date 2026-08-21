# AGENTS — Website Pilot

Use the installed App Factory. Read `PROJECT_STATE.md`, then `PRODUCT.md` and `ARCHITECTURE.md`. This is content-first, not a web-admin: do not add auth, database, React state, dashboard shells, shadcn or ReUI without a new product requirement.

Verification: `npm ci`, `npm run format:check`, `npm run typecheck`, `npm run build`, `npm audit --audit-level=high`, `npx playwright install chromium`, `npm run test:e2e`.
