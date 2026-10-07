# Prototype and future wallet architecture

```mermaid
flowchart TD
  Wallet["Future MFS wallet integration"] -.-> API["FastAPI transaction checks"]
  UI["React simulated payment"] --> API
  API --> Risk["LightGBM + Isolation Forest"]
  API --> Context["Recipient, purpose and report context"]
  Risk --> Explain["TreeSHAP + policy reasons"]
  Context --> Explain
  Explain --> Policy["SILENT / NUDGE / PAUSE"]
  Policy --> Choice["Customer cancels or acknowledges continuation"]
  Choice --> Persist["SQLite / optional PostgreSQL"]
  API --> Persist
  Explain -.-> LLM["Optional private LLM: wording only"]
  API --> Monitor["Process metrics + score drift"]
  Evidence["Checked public-source manifest"] --> Page["Bangladesh Evidence dashboard + report"]
  Models["Artifact hashes + feature/policy versions"] --> API
```

Solid connections describe implemented prototype paths. Dotted wallet integration is proposed; dotted LLM is optional. Evidence is a static historical snapshot independent of customer data and model results. Benchmarks are regenerated offline and published as aggregate summaries.

Security boundary: authenticated demo sessions own customer state/checks; admin-key routes own global data exports. These sessions are not real identities. Real provider authentication, payment processing, production model registry, geographic hosting guarantees and banking-grade transaction audit are not implemented.

Frontend routes: `/#evidence`, `/#evaluation`, `/#impact` work with static hosting. `/evidence`, `/evaluation`, `/impact` are supported by Vercel rewrites. Actual public files remain under `/evidence/`. `GET /public-evidence` returns the same checked manifest; existing `GET /evidence` remains synthetic evaluation.
