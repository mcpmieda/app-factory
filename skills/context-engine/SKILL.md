---
name: context-engine
description: Build or refresh the App Factory incremental repository map when resuming, inspecting, planning, debugging, maintaining, or reconciling changes in an existing software project. Use it to avoid rereading the whole repository while still opening authoritative files when details matter.
---

# Context Engine

Use `core/CONTEXT_ENGINE.md` as the contract.

## Flow

1. Prefer the project's existing `.factory/context/repo-map.json` only as cache, never as authority over real files.
2. Refresh context at resume/next or when external changes are possible.
3. Read `.factory/context/SUMMARY.md` first for navigation.
4. Open only the authoritative files relevant to the current task.
5. Reconcile `added`, `changed` and `removed` before continuing a partially completed phase.
6. Never index secrets, dependency trees, build output or binary payloads just to make the map more complete.

## Runtime

When the repository includes the runtime:

```bash
python scripts/factory.py context
```

Adapters may invoke an equivalent installed command. Do not make the user run it if the agent can.
