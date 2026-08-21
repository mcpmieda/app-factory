# Patrimônio Escolar — validation example

Second application generated from the clean App Factory `web-admin` starter. All names and inventory records are fictitious.

## Requirements

- Node.js 22–24;
- npm 10.9.9.

## Local setup

```bash
npm ci
npm run setup
npm run dev
```

The setup creates `.env.local` with a random secret, applies migrations and seeds `admin@example.com` / `local-admin-password` plus fictitious assets. Running setup again is safe and does not duplicate data.

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

SQLite is intentionally local to validation. It is not the profile’s production default.
