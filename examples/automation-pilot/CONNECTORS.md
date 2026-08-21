# Replacing local boundaries with a real connector

Keep `build_report()` pure. Add an input adapter that returns the same row dictionaries and an output adapter that accepts the report object; do not mix API calls into transformation rules.

Before enabling a connector:

1. define least-privilege credentials outside Git and redact logs;
2. make read-only/dry-run the first operation;
3. add timeouts, bounded retries and pagination/checkpoint behavior;
4. use an idempotency key or upsert contract for writes;
5. stage and validate output before committing remote changes;
6. test partial failures and resumability with a fake connector;
7. document rate limits, ownership and rollback.

External accounts and APIs are intentionally outside this pilot.
