# AGENTS — Chrome Extension Pilot

Use the installed App Factory. Read `PROJECT_STATE.md`, `PRODUCT.md` and `ARCHITECTURE.md`. Preserve Manifest V3, CSP-safe bundled code and least privilege. Never broaden match patterns, add named permissions, remote scripts, secrets or production hosts without an explicit product/security decision.

Verification: `npm ci`, `npm run format:check`, `npm run typecheck`, `npm test`, `npm run build`, `npm audit --audit-level=high`, `npx playwright install chromium`, `npm run test:e2e`, `npm run package`. The ZIP under `artifacts/` is validation output and must not be committed.
