# Product — Patrimônio Escolar

## Outcome

Prove that a broad request — “Quero criar um sistema de patrimônio para a escola” — can become a coherent `web-admin` application from the reusable starter.

This is a validation app with fictitious data, not a production school system.

## User and critical flow

A fictitious administrative user signs in, sees inventory indicators, searches/filters assets, creates or edits a record, changes its location/status and archives/reactivates it safely.

## Asset data

- unique patrimonial code;
- description;
- category;
- location/sector;
- optional custodian;
- status;
- notes;
- active/archive state;
- created/updated timestamps.

## Success criteria

- every administrative route and mutation is protected server-side;
- validation and duplicate codes produce useful feedback;
- archive is reversible and requires confirmation;
- state persists after reload;
- loading, empty, error and success states exist;
- desktop and mobile critical flows pass without relevant console errors.

## Non-goals

- real school/user data;
- production deployment or production database selection;
- permanent deletion;
- ReUI, because the current list does not require an advanced grid;
- analytics, observability, client cache/state or form frameworks.
