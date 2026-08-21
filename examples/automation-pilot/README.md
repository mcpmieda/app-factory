# Automation pilot — roster report

Small complete local automation used to validate the App Factory `automation` route. Requires Python >=3.11; runtime dependencies: none.

```sh
python -m pip install -r requirements-dev.txt
python -m ruff format --check .
python -m ruff check .
python -m compileall -q roster_report tests
python -m unittest discover -s tests -v
python -m roster_report fixtures/roster.csv output/report.json --dry-run
python -m roster_report fixtures/roster.csv output/report.json
```

Running the last command again produces byte-identical JSON. Read `PROJECT_STATE.md` and `CONNECTORS.md` before continuing.
