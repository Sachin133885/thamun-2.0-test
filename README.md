# Thamun — Pause. Understand. Decide.

Explainable AI and adaptive pre-authorization intervention for Bangladesh MFS Authorized Push Payment (APP) scams.

Scammers can persuade customers to authorize a payment themselves. Thamun checks available behavioral, recipient, report and purpose signals before **simulated** final authorization, explains concerns, and lets the customer cancel or explicitly acknowledge continuation.

**Prototype on synthetic data. No real accounts or payments.** This archive does not integrate with bKash, Nagad or upay and does not intercept live wallet OTPs. Never enter real credentials, PINs or OTPs.

Team: Neural Nexus — Tammam Ibn Aman, Sachin Sarker, Deep Mitra. Existing deployment references: [web app](https://thamun.vercel.app), [API](https://thamun-demo.onrender.com), [demo video](https://drive.google.com/file/d/1c6QW9KjVeQPvivgj_39NzZTq4E2FSBrW/view?usp=sharing). Their current deployment state was not verified or changed by this archive update.

## Quick local demo

Prerequisites: Python 3.10+ with venv/pip and a working LightGBM runtime; Node.js 22.12+ (24 recommended), npm, and internet access for initial dependency installation. On Linux, LightGBM may need `libgomp1`. No GPU or LLM key is required.

```bash
# Extract the ZIP, then enter its thamun-main directory.
./start.sh
```

The script creates a Python environment if needed, installs dependencies, generates/trains demo models only when absent, and starts FastAPI on localhost:8000 and Vite on localhost:5173. Open http://localhost:5173. Ctrl+C shuts down the API child process. The ZIP contains trained synthetic demo artifacts; a fresh Git checkout can regenerate them. Neither `.env` nor private credentials are included.

To retain the same token/session across restarts, copy `.env.example` to `.env` and set a stable random `THAMUN_SECRET`. An unset secret generates a temporary key and intentionally invalidates old tokens after restart. Leave `ADMIN_KEY` blank unless using admin routes. Set exact `ALLOWED_ORIGINS` for deployment; do not use the localhost defaults for a hosted frontend.

For explicit setup in two terminals:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r api/requirements.txt
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
# In another terminal:
cd web
npm ci
npm run dev
```

## Judge navigation

1. Run a scenario in **Demo guide**.
2. Inspect the score, SHAP, recipient context and policy reasons in **Why it decided**.
3. Click **Bangladesh Real Evidence**, immediately below the Inspector's explanation.
4. Explore **AI / ML Analysis** and **Prototype Impact** below that entry.

Direct routes: `/#evidence`, `/#evaluation`, `/#impact`. The evidence page is usable without the model backend. `/evidence`, `/evaluation`, `/impact` also work with the included Vercel rewrites.

## 🇧🇩 Bangladesh MFS Evidence Report

[Full evidence report](docs/bangladesh_mfs_evidence_report.md) · [PDF](docs/bangladesh_mfs_evidence_report.pdf).

The native evidence dashboard has source-backed scale cards, search/category/tier filters, a two-month zero-based comparison, expandable incident cases, source explorer, evidence-to-feature mapping and integrated full-report viewer. It is a dated curated snapshot, not a live feed. Bangladesh Bank web statistics, institutional hosted media and case reports remain visibly separate.

Public data does not consistently isolate APP fraud. The Dighi and Faridpur cases concern impersonation/credential compromise and are classified as broader MFS fraud, not proven victim-initiated APP cases. The supplied Bangladesh Bank December 2025 PDF and exact police national statistics were not verified; their numbers/page references are withheld. See each item's source, date, locator and limitations.

Public evidence supports the problem context; it does **not** validate Thamun's model or demonstrate prevented fraud.

## Existing features preserved

- LightGBM risk and payment-category models, Isolation Forest behavioral anomalies and TreeSHAP contributions.
- Historical feature construction, August threshold selection and September hold-out.
- SILENT / NUDGE / PAUSE plus contextual payment-purpose inquiry.
- Qualified scam-report confidence and deduplication; new recipient alone is not a scammer.
- Bill readiness, spending insights, savings goals and Ask Thamun coaching.
- English/Bangla customer warnings and template fallback when optional LLMs are unavailable.
- FastAPI APIs, React/Vite frontend, existing tests and Render configuration.

| Intervention | Prototype behavior |
|---|---|
| SILENT | Routine payment proceeds to synthetic confirmation without an interruptive warning |
| NUDGE | Brief context or coaching warning |
| PAUSE | Explain concerns; customer cancels or acknowledges before continuation |

The backend requires `acknowledged: true` for PAUSE continuation. Demo confirmation accepts a four-digit synthetic code; never use a real OTP. A check is single-use, owned by its session/customer, and bound to its evaluated fields. Changing amount/recipient/purpose requires a fresh check.

## Architecture and traceability

[Architecture](docs/architecture.md) shows implemented and future components separately. The optional LLM can rephrase or coach but cannot change the risk decision. Fixed reasons and advice remain authoritative. Numeric and conservative safety-reversal checks have documented semantic limitations.

SQLite is the local default; existing PostgreSQL support uses `DATABASE_URL`. Reports, audit and feedback are persisted, with new decision and demo-session snapshots for restart hydration. `/check` includes actual model-artifact hash, feature-schema/policy versions and timestamp. Real financial atomicity and multi-worker state coordination remain future work.

## Evaluation and reproduction

All experiments use generated data; none are real customer outcomes.

```bash
source .venv/bin/activate
python -m data.generate
python -m ml.train
python -m ml.evaluate
python -m ml.benchmark
python -m pytest -q
cd web
npm test
npm run build
```

[Original policy replay](docs/evaluation.md) · [Model benchmarks](docs/ml_evaluation.md) · [Ablations](docs/ablation_study.md) · [Warning-friction simulation](docs/alert_fatigue_evaluation.md).

Machine-readable results, split dates, feature lists, validation thresholds, dependency versions and dataset hash are in `evidence/evaluation/`. Benchmarks compare Logistic Regression, Random Forest and LightGBM, then add historical behavior, recipient history and idealized stated purpose. No historical scam-report labels exist, so report-feature ablation is explicitly unavailable. Models recover simulator patterns; truthful purposes and synthetic category histories are optimistic assumptions. Apparent performance does not establish production accuracy or calibrated fraud probabilities.

The impact dashboard reports session screenings and customer choices. Cancelled attempt value is not money saved or measured loss avoided. Repeated checks are separate screening events; arbitrary demo transactions have no ground-truth false-pause labels.

To regenerate the evidence report/PDF from the checked manifest:

```bash
pip install -r scripts/requirements.txt
python scripts/build_evidence_report.py
```

Source facts must be reverified before editing the manifest. No background scrape or automatic replacement of verified values is implemented.

## API and environment

Interactive local API docs: http://localhost:8000/docs.

Existing customer/payment/coaching/report routes remain. `GET /public-evidence` provides curated public evidence; existing `GET /evidence` provides synthetic evaluation. `/analytics` is session-scoped; `/admin/analytics`, audit and feedback export require `X-Admin-Key`. `/monitoring` is prototype process monitoring.

Configuration: `.env.example` documents signing/admin keys, auth, CORS, rate limits, SQLite/PostgreSQL and optional private-model settings. `web/.env.example` documents `VITE_API_URL`, read at build time. Custom `API_PORT` must match the frontend API URL. Forwarded IP headers require an explicitly trusted proxy. Never commit `.env`, tokens, database files or credentials.

## Security, responsible AI and limits

[Security](docs/security.md) · [Responsible AI/data residency](docs/responsible_ai.md) · [Scalability/drift](docs/scalability.md) · [Model card](docs/model_card.md) · [Data card](docs/data_card.md).

Demo-session issuance is not production customer login. User reports remain unverified and susceptible to new-session abuse. Rate limits and monitoring are per process. Snapshot persistence and audit writes are not a banking transaction service. Production-scale load, geographic hosting, legal compliance, real wallet integration and representative user validation are unvalidated. New evidence-page headings/entry support Bangla; research-source detail remains primarily English and does not claim a professionally reviewed complete Bangla translation.

CI configuration includes backend/frontend tests, build, dependency checks and secret scanning. A configured workflow is not a verified successful remote CI run. See [actual local validation](docs/phase2_validation.md), [Phase 2 changes](docs/phase2_changes.md), [judge evidence matrix](docs/judge_evidence_matrix.md) and [demo script](docs/demo_script.md).

## Deployment and roadmap

Render's existing build/start commands are preserved: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`. Its build regenerates data/models. Vercel builds `web` using `npm ci && npm run build`; public evidence assets ship with the frontend. Configure provider database/keys/CORS and a matching frontend API URL before publishing. No deployment or push was performed.

Next steps: authorized wallet integration; real provider identities; approved anonymized transaction/outcome data; report moderation and appeal; atomic persistent payment/event records; shared limits/observability; fresh temporal/customer validation; geographic/private-model and legal review.

**Pause. Understand. Decide.**
