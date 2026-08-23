# ARCHITECTURE

## Classification

- system level: `local-app`;
- process scale: `S/M`;
- API governance: `none`;
- semantic depth: `domain`;
- deployment: Vercel distribution of the Next.js app;
- authoritative data source: browser `localStorage`.

## Boundary

```text
Vercel / browser download
        ↓
Next.js + HeroUI client application
        ↓
versioned local repository
        ↓
localStorage v2
```

There is no shared server data path in the current product.

## Persistence contract

Current key:

`app-factory.student-registration.v2`

Legacy key:

`app-factory.student-registration.v1`

Read strategy:

1. validate and use v2 when present;
2. otherwise validate v1;
3. migrate v1 → v2 deterministically;
4. persist v2;
5. remove the legacy key only after the v2 write succeeds.

The migration preserves old values. New fields with no historical source receive explicit neutral values, never invented business data.

## Recovery

- JSON backup is the portable recovery mechanism for this local product;
- backup is versioned and validated before restore;
- restore replaces local state only after explicit user confirmation;
- CSV is export/reporting, not a lossless restore contract.

## Security/identity

There is no identity boundary because this app intentionally stores only device-local demonstration data. If a future requirement introduces multiple users, institutional shared data, permissions or cross-device continuity, System Engineering must reclassify the product before implementation.

## Why no backend

A backend would not solve a current requirement. Adding one now would raise hosting, identity, authorization, migration and operational complexity without changing the intended local behavior. Reclassification occurs when the product requirement changes, not because the app is publicly hosted.
