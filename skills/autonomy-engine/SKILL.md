---
name: autonomy-engine
description: Continue a software project autonomously using App Factory state, context fingerprint, next-action routing, verification, repair limits, review and delivery. Use when starting or resuming work so the user does not have to drive technical phases manually.
---

# Autonomy Engine

Use `core/AUTONOMY_ENGINE.md` as the contract.

## Default behavior

At the beginning of actionable software work:

1. recover or initialize autonomous state;
2. refresh repository context;
3. ask the engine for the next action;
4. execute that action with the current agent/tools when safe;
5. record the resulting event;
6. continue until done or genuinely blocked.

Do not expose every state transition to the user.

## Stop conditions

Only interrupt for a real human decision, unavailable credential/data, destructive/high-impact authorization, cost, or a technical stall that cannot be resolved by changing strategy/executor.

## Verification

A successful implementation event does not mean completion. Move through verification and review before delivery. Failed verification enters bounded repair instead of an unbounded retry loop.

## Handoff

When another executor is truly needed, leave `.factory/state.json`, GitHub Issue/PR state and authoritative project documents sufficient for a fresh session to run `resume` without conversation history.
