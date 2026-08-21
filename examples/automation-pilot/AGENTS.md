# AGENTS — Automation Pilot

Use the installed App Factory. Read `PROJECT_STATE.md`, `PRODUCT.md` and `ARCHITECTURE.md`. Preserve deterministic output, partial-row recovery, dry-run safety and atomic replacement. Do not introduce a SaaS/API, secrets, network access or destructive destination without explicit product and risk review.

Verification: `python -m pip install -r requirements-dev.txt`, `python -m ruff format --check .`, `python -m ruff check .`, `python -m compileall -q roster_report tests`, `python -m unittest discover -s tests -v`. Run the documented dry-run and double-run idempotency check before changing output behavior.
