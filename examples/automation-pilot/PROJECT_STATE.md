# PROJECT_STATE

- Product: local fictitious roster normalizer and training-priority report.
- Status: V0.9 pilot complete and locally verifiable.
- Factory baseline: App Factory V0.9 branch from `5eb7209`.
- Stack: Python >=3.11 standard library at runtime, Ruff 0.16.4 for development, unittest.
- Current slice: validate CSV schema/rows, normalize, apply a priority rule, preserve valid rows after partial errors, preview with `--dry-run`, atomically write deterministic JSON.
- Safety: no network/account/secret; dry-run does not write; final replacement is atomic; repeated input yields byte-identical output.
- Next safe action: rerun gates. Read `CONNECTORS.md` before replacing filesystem boundaries.
- Constraints: never make a real connector destructive by default; add retries, authentication and redacted logs according to that connector's risk.
