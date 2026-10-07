# Scalability and drift

FastAPI has existing SQLite/PostgreSQL SQLAlchemy support; PostgreSQL can be selected with `DATABASE_URL`. Report/audit/feedback persistence is preserved. This update adds persistent `risk_decisions` and `demo_sessions` tables using additive table creation. Existing table columns are untouched. Back up the database before applying schema changes; a migration/version-management system remains production work.

Models load once per process. The synthetic payment/history cache is bounded to 120 sessions and can hydrate snapshots after eviction/restart. Snapshot persistence requires a stable signing secret to reuse bearer sessions. Reports, goals, balance/history, pending decisions and action logs survive restarts; transient nudge suppression/monitor counters are not a production source of truth.

Before horizontal scale: serialize concurrent mutations for each customer, use transactional outcome+balance+audit writes, replace snapshot persistence with an event/transaction schema, move limits and metrics to shared stores, define idempotency for check creation, and add model-artifact verification/registry. The conditional pending-decision finalization prevents duplicate use of one check but does not establish banking-grade transaction guarantees.

Current monitoring tracks process request/error/latency counters, decision mix and bounded risk-score distributions. `python -m ml.benchmark` emits a versioned synthetic reference. PSI after 200 observations compares score distributions and recommends review; it is not observed fraud prevalence. The serving model's reference is retrospective on August, which was included in final serving training, and is disclosed. Full feature/missing-value drift, labeled performance drift and external monitoring are future work.

Optional queues and caches should be introduced only when measured needs justify them. Keep model inference and required decisions synchronous enough for authorization; educational LLM output has a template fallback. Wallet integration, Bangladesh/private hosting, encryption and provider load/service-level targets require design and verification.

Production-scale load performance has not yet been validated. No production throughput or latency claim is made. Local results, if present in `phase2_validation.md`, describe only that environment. Live Render/Vercel deployments have not been updated.
