# Chrome extension pilot — Focus Lens

Small complete Manifest V3 extension used to validate the App Factory `chrome-extension` route.

```sh
npm ci
npm run format:check
npm run typecheck
npm test
npm run build
npm audit --audit-level=high
npx playwright install chromium
npm run test:e2e
npm run package
```

The ZIP is generated under ignored `artifacts/` for validation only. Read `PROJECT_STATE.md` before continuing.
