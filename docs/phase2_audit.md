# Phase 2 archive audit — 7 October 2026

The supplied archive contains FastAPI/React, a chronological synthetic generator, LightGBM classifiers, Isolation Forest, TreeSHAP, reporting, bilingual payment warnings, bills, savings, coaching, token sessions, SQLAlchemy SQLite/PostgreSQL persistence for reports/audit/feedback, and process-local monitoring. Existing deployment files are retained. No `.git` history or AGENTS.md was supplied; commit history and Git cleanliness cannot be verified from this archive.

Before changes: backend tests **30 passed, 10 skipped** because model artifacts were absent; frontend production build passed. Default generator produced 200 synthetic customers, 113445 transactions and 332 scam-labeled outgoing records. These are simulator counts, not Bangladesh observations.

Missing: native public-evidence page/report, reproducible multi-model benchmarks/ablations, frontend impact view, persistent pending decisions/version metadata, report verification-state metadata. Existing README national fraud/APP assertions lacked verified supporting references and must be replaced.

## Implementation plan

- [x] Preserve the payment/coaching APIs and existing deployment configuration.
- [x] Test then implement a shared curated evidence manifest, filters, incident detail, source explorer, statistics and full report. Put entry immediately below Why it decided. Public page must work without the model API.
- [x] Test then add independent recipient explanation, version/timestamp metadata and persistent decision snapshots. Preserve demo OTP compatibility; the UI must clearly identify synthetic authorization.
- [x] Run real generated-data benchmarks, model-feature ablations, policy ablations, friction comparison and validation-score drift reference. Do not synthesize report labels unavailable in historical data.
- [x] Add operational impact and AI evaluation panels, reproducible setup, security/AI/model/data documentation, CI and acceptance evidence.
- [x] Run regression tests, frontend build, HTTP/UI smoke checks, report rendering checks and final archive checks. Record blocked external verification or production work honestly.

## Boundaries

Static source snapshots use checked dates, not live-data claims. OTP theft cases are broader MFS fraud, not demonstrated victim-authorized APP transfers. Existing free demo tokens are not real customer authentication. PostgreSQL support exists but a production migration/deployment/load claim is out of scope. The supplied prompt and user's direct instruction authorize local implementation without another design approval; no commits or live deployment will occur. Deliverable is the updated archive only.
