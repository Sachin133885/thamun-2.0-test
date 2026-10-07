# Prototype security

## Implemented

- Signed expiring demo-session tokens, customer-bound authorization, admin-key routes, validated Pydantic inputs and SQLAlchemy parameterized queries.
- Bound sessions see only their own demo customer in `/customers` and cannot reset another customer's state.
- Session-level request/report limits, report deduplication and qualified unverified confidence. These are not verified real identities; demo users can obtain new sessions.
- Cross-session pending-check isolation and conditional single-use decision finalization. Invalid demo authorization no longer consumes the pending check. PAUSE continuation requires `acknowledged: true` in the backend.
- Default CORS restricted to local frontend origins; deployment must set its exact frontend origin. Forwarded IP headers are trusted only with explicit `TRUST_PROXY_HEADERS=true` behind a configured trusted proxy.
- Global analytics require the admin boundary; ordinary sessions get only their own events. `/admin/analytics`, audit and feedback export require `X-Admin-Key`.
- Generic client error messages and existing no-store/nosniff/frame-denial headers. React escapes evidence/report text and external links use `noopener noreferrer`.
- `.env.example` contains no operational secrets. Never use production PINs/OTPs in this demo.

## Configuration

Set a strong, stable `THAMUN_SECRET` to keep token sessions valid across API restarts. The fallback temporary secret intentionally invalidates tokens on restart. Set `ADMIN_KEY` privately or leave admin routes disabled. Restrict `ALLOWED_ORIGINS` for deployed use. `AUTH_REQUIRED=false` is only for isolated local tests.

## Limits and production requirements

`/auth/session` creates demo identities without a real login; it is not customer authentication. Unbound demo tokens intentionally switch among synthetic customers. No real wallet data should be loaded into this prototype. Community submissions require provider-linked identities, anti-Sybil controls, review and appeal before production.

SQLite/session snapshots are a prototype persistence design. Multi-process concurrent customer mutations and atomic payment/session/audit commits need a transaction service and database locking before real payments. Rate limiting and monitoring remain process-local. Use a shared gateway/store for scale. Audit records are not cryptographically tamper-proof.

Bearer tokens are in localStorage; a production XSS/session design needs review. Cookie auth would require appropriate CSRF controls. Use TLS, encryption, role-based access, data retention/deletion policy and legal review. Do not infer compliance from this document.

CI config includes dependency and secret scanning. Remote GitHub Actions, provider settings and production security have not been validated by this local archive update. See `phase2_validation.md` for checks actually executed.
