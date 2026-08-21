# Architecture

The runtime uses only Python's standard library: `csv` for ingestion, explicit normalization/validation, stable JSON serialization and same-directory temporary files plus `os.replace` for atomic output. The CLI separates a fatal input/schema error (exit 2) from recoverable row errors (reported in a successful artifact). No timestamp or random identifier enters output, so identical input is byte-identical.

Python was selected because a local file transformation does not need a web runtime or JavaScript build. Ruff is pinned as a development-only formatter/linter; unittest covers rules and the subprocess boundary.
