# Phase 2 changes

| Phase 1 issue | Implemented response | Why it matters | Implementation and verification |
|---|---|---|---|
| Problem unclear | APP positioning; clear prototype authorization boundary | Separates manipulated payments from takeover/OTP theft | README, public evidence report, `Evidence.jsx` |
| Bangladesh relevance | Curated public-source manifest and interactive evidence dashboard | Source quality and limitations visible to judges | `web/public/evidence/bangladesh.json`, `Evidence.test.jsx` |
| Synthetic ML limitation | Separate public/ML dashboards; reproducible benchmarks and ablations | Real evidence does not imply real model validation | `ml/benchmark.py`, JSON results, ML/data cards |
| Alert friction | Explicit generic-policy comparison and adaptive-policy proxy | Quantifies interruptions without invented user research | `docs/alert_fatigue_evaluation.md` |
| Recipient context | Independent qualified recipient-risk explanation | Newness/reports are signals, not accusations | `api/recipient.py`, `test_phase2.py` |
| In-memory important state | Decision/session snapshots and restart hydration | Pending checks, history and goals survive restart | `api/db.py`, `api/store.py`, restart tests |
| Weak traceability | UUID check IDs; model hash, feature/policy versions and timestamp | Decisions trace to actual artifacts | `/check`, persistent `risk_decisions` |
| Authorization correctness | Backend PAUSE acknowledgement; validation before consumption | Invalid confirmation no longer loses the check | `/pay`, payment UI, API regression tests |
| Security | Bound-customer views/reset, admin analytics, conservative CORS/proxy trust | Limits data access and spoofed forwarding | `security.md`, API tests |
| LLM integrity | Preserve numeric checks; additional safety-reversal rejection | Unchanged numbers do not guarantee safe wording | `api/explain.py`, regression test |
| Impact unclear | Session operational dashboard, cancellation value labeled honestly | Avoids equating cancellation with prevented loss | `Analysis.jsx`, `/analytics` |
| Setup and judge flow | Bootstrap start script; evidence before ML/impact in Inspector | Demo is easier to explore | `start.sh`, README |
| Monitoring/quality | Score-drift reference and GitHub Actions checks | Provides a testable path toward scale | `api/monitor.py`, `.github/workflows/quality.yml` |

No live service, Git commit or push was performed. The archive lacked Git history. Unverified official PDF/police statistics are explicitly withheld. Real wallet integration, real identities, report moderation, atomic financial persistence, production feature monitoring, load capacity and legal compliance remain future work.
