---
name: learning-engine
description: Use privacy-safe local execution outcomes to improve future backend choices conservatively, after capability, safety, availability and task fallback filters.
---

# Learning Engine

Use when execution history exists and the Factory needs to decide whether evidence is strong enough to improve the V1.2 baseline route.

## Order of authority

1. required capabilities;
2. availability/permissions;
3. current-task failure threshold;
4. safety/risk/Definition of Done;
5. learned evidence.

Learning never bypasses the first four layers.

## Persist only technical metadata

Allowed learning fields are timestamp, known action class, known capability signature, known backend, outcome and optional duration.

Never persist prompt text, user/project descriptions, code, file contents, summaries/logs, secrets, names, task keys or private URLs.

Unknown action text becomes `other`; unknown capability/backend metadata is rejected.

## Confidence

Keep the baseline when samples are insufficient. Use the conservative prior/minimum-sample contract from `core/LEARNING_ENGINE.md`.

A learned preference may reorder already-capable lightweight backends. It must not:

- resurrect a backend rejected by failure threshold;
- choose a backend missing required capability;
- promote `local_full` over an eligible lighter backend only because of historical score;
- reduce verification to improve speed.

## Commands

Agents may use:

```text
python scripts/factory.py --root <project> learning-status
python scripts/factory.py --root <project> learning-recommend <action>
python scripts/factory.py --root <project> route <action>
python scripts/factory.py --root <project> route <action> --no-learning
```

The user normally does not run these manually.
