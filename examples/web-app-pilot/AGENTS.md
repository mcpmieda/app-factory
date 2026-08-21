# AGENTS — Web App Pilot

Use the installed App Factory. Read `PROJECT_STATE.md`, `PRODUCT.md` and `ARCHITECTURE.md`. This is an end-user journey, not a web-admin. Preserve the focused booking flow; do not add dashboard shell, Data Grid, ReUI, auth, database, global state or client cache without a demonstrated product need.

Verification: `npm ci`, `npm run format:check`, `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm audit --audit-level=high`, `npx playwright install chromium`, `npm run test:e2e`.
