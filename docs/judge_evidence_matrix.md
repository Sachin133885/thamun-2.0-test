# Judge evidence matrix

| Feedback | Response | Status/evidence type | Location |
|---|---|---|---|
| Clearer problem | Manipulated customer-authorized payment story | Implemented positioning; prototype flow | README, `docs/demo_script.md` |
| Bangladesh evidence | Filterable evidence cards, tier badges, incident detail, full report | Public-source snapshot; verified claims and verification gaps | `/#evidence`, report Markdown/PDF |
| AI depth | LR/RF/LightGBM benchmarks; historical/context feature ablations | Calculated synthetic temporal results | `/#evaluation`, `evidence/evaluation/benchmarks.json` |
| Alert fatigue | Explicit generic new-recipient warning comparator | Offline simulation, not customer research | `docs/alert_fatigue_evaluation.md` |
| Recipient intelligence | Independent report/history explanation | Implemented demo rules | Inspector, `api/recipient.py` |
| Business impact | Actual session screenings, pauses and recorded decisions | Synthetic prototype events, no money-saved claim | `/#impact`, `/analytics` |
| Persistence | SQLite default, existing PostgreSQL option; new decision/session tables | Implemented; restart tests | `api/db.py`, `tests/test_phase2.py` |
| Security | Customer scope, admin access, acknowledgement, input and report controls | Implemented prototype controls; not bank-grade security | `docs/security.md`, backend tests |
| Data residency | Private-model default and clear hosting limits | Configuration plus future deployment requirement | `docs/responsible_ai.md` |
| Scalability | Versioned score drift and documented state limitations | Lightweight prototype; production scale unvalidated | `docs/scalability.md` |
| Documentation | Cards, architecture, change record and reproducible commands | Implemented docs; future components distinguished | `docs/` |

See `phase2_validation.md` for exact executed checks. No statistic, model result, UX finding, deployment or compliance claim should be inferred from a merely configured CI job or proposed capability.
