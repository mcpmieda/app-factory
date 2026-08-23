---
name: api-engineering
description: Use when a project exposes, consumes or evolves an API, integration, webhook, event contract, GraphQL schema, gRPC service or multi-step API workflow. Applies App Factory API governance proportionally: choose protocol, define contract source of truth, security, compatibility, resilience and executable gates without forcing APIs onto projects that do not need them.
---

# API Engineering

Use `core/API_ENGINEERING.md` as the source of truth. This Skill operationalizes that contract; it must not duplicate the whole policy.

## Process

1. Confirm that a meaningful API/integration boundary exists. If not, stop here; do not create OpenAPI or API infrastructure just for ceremony.
2. Classify API governance as `none`, `lightweight`, `contract` or `governed`.
3. Identify consumers, provider/owner, lifecycle and compatibility cost.
4. Select the simplest suitable interface style:
   - HTTP resource-oriented/OpenAPI;
   - GraphQL;
   - gRPC/Protobuf;
   - AsyncAPI for events/messages;
   - Arazzo only for material multi-step workflows.
5. For `contract`/`governed`, create or update the machine-readable contract before consumers depend on undocumented behavior.
6. Define boundary behavior: validation, errors, auth/authz, pagination/filtering, idempotency/concurrency and long-running operations only where relevant.
7. For external APIs, define timeout, retry/backoff, rate-limit behavior, response validation, idempotency/checkpoint and failure/recovery policy proportionally.
8. For webhooks, define authenticity, replay/idempotency and processing behavior.
9. Add executable gates supported by the project:
   - Redocly CLI or equivalent for spec lint/validation;
   - oasdiff or equivalent for OpenAPI compatibility when consumers depend on stability;
   - Schemathesis or equivalent for generated negative/property/stateful testing when useful;
   - Pact or equivalent only when independent consumer/provider evolution justifies it;
   - integration/smoke tests against real or equivalent runtime.
10. If the change is behaviorally relevant, update `core/SEMANTIC_VERIFICATION.md` artifacts before implementation and map API criteria to executable evidence.
11. Run `skills/security-review` for exposed/protected/production API surfaces as risk requires, using OWASP API Security as the API threat reference.
12. Record durable decisions in `ARCHITECTURE.md` or `API.md` without copying generic Factory guidance into the project.

## Contract rules

- One authoritative contract per interface; generated docs/SDKs derive from it where possible.
- Keep implementation and contract in the same functional change.
- Never expose secrets or sensitive real data in examples.
- Do not silently break existing consumers.
- Do not turn a legacy API migration into a big-bang rewrite merely to match a preferred style.
- Fix tool versions in CI/lockfiles for reproducibility.

## Verification

For `contract`/`governed`, require evidence proportional to risk that:

- the contract parses/lints;
- critical runtime behavior matches the contract;
- protected operations reject unauthorized access;
- invalid inputs produce controlled errors rather than accidental server failures;
- breaking changes are detected against a known baseline;
- retries cannot duplicate material writes when idempotency is required;
- external dependencies fail within bounded time and controlled recovery behavior;
- webhook duplicates/replays are safe when applicable.

## Relationship to other Skills

- `architecture`: chooses system boundaries; this Skill owns API-specific contract choices.
- `security-review`: owns security analysis; this Skill supplies API-specific threat/gate requirements.
- `semantic-verification`: owns intention → executable evidence traceability.
- `database`: owns persistence/schema decisions behind the API.
- `deployment`: owns runtime/release environment.

Do not replicate those responsibilities here.
