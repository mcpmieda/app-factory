# PROJECT_STATE

## Objective

Manter verificável a primeira fatia completa de **Empréstimos de Equipamentos**.

## Current state

- phase: functional slice complete and locally verified;
- App Factory profile: `web-admin`;
- Factory baseline: `v0.7`;
- Motion Profile: `ambient` contextual;
- authentication: not activated;
- persistence: Drizzle + local SQLite activated;
- advanced UI/ReUI: not activated;
- data: fictitious seed only;
- journey: inventory → loan → reload → return complete;
- impossible state: a partial unique index and domain rule reject a second active loan;
- filters: item/responsible/status, including a dedicated overdue view;
- validation: format, lint, typecheck, unit/integration, build, audit high/critical and 8 Playwright scenarios passed locally;
- browser: desktop, Pixel 7, keyboard, no horizontal overflow, clean console and reduced motion passed.

## Next action

The next safe change is small and test-led: extract and unit-test the combined status/search filtering rules without changing the persistence model. Production deployment remains out of scope until provider, authentication and authorization are decided.
