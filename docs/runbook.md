# Revenue Metrics Runbook

## Why This Exists

Production ecommerce analytics often breaks down at the interface between finance and growth:
the business wants one revenue number, while multiple teams compute different versions for valid reasons.

## Release Rules

- `realized_revenue` is the finance-owned metric for executive reporting.
- attributed revenue can differ from finance revenue, but the variance must be understood before publication.
- backfills should be executed in bounded windows rather than via full refresh by default.
- contract-breaking metric definition changes should be treated as governed releases, not silent edits.

## Typical Response Flow

1. Check finance-vs-marketing reconciliation.
2. Review changed refund behavior or late-arriving order updates.
3. Execute bounded backfill batches for the affected dates.
4. Re-publish only after variance status is no longer flagged for investigation.
