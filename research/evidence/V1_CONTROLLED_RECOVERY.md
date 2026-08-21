# V1 controlled recovery evidence

Date: 2026-08-21

Scope: isolated temporary directory outside the repository. No failing change was introduced into the branch.

1. Baseline candidate classified `null` as `available`, a future due date as `loaned` and a past due date as `overdue`.
2. `node preflight.mjs` passed with `PASS: overdue classification preflight`.
3. The temporary candidate was deliberately changed to classify a past due date as `loaned`.
4. The same preflight failed with `AssertionError`, actual `loaned`, expected `overdue`.
5. The candidate was restored to the baseline rule.
6. The same preflight passed again with `PASS: overdue classification preflight`.

The maintained project stayed green before and after the exercise. The permanent equivalent guard is `src/features/loans/domain.test.ts` plus the overdue Playwright scenario.
