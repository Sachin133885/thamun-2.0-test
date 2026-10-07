# Local validation — Phase 2 archive

Validation was performed on the supplied archive after implementation, with Python 3.12.14 and Node.js 24.19.0. There was no Git repository/history in the upload.

| Check | Actual result |
|---|---|
| Baseline backend | 30 passed; 10 model-dependent tests skipped before training |
| Final `python -m pytest -q` | 48 passed; no skipped tests; 8 dependency/test-fixture warnings |
| `npm test` | 5 passed across 2 files, including evidence filters/report escaping and internal-anchor navigation |
| `npm run build` | Passed, Vite production bundle and public evidence assets generated |
| `npm audit --audit-level=high` | 0 vulnerabilities in the installed lockfile |
| Python compile / shell syntax | `compileall` passed; `bash -n start.sh` passed |
| Public built assets over local HTTP | Manifest, benchmarks, friction results, Markdown report and PDF: all 5 returned 200 and matched source assets |
| Generated ML experiments | Generator, training, original policy replay and benchmark/ablation runs completed; actual outputs included |
| Report layout | Five-page PDF rendered to images and visually inspected; no overlapping or clipped content observed |

Backend regression tests cover original payment/coaching/report behavior plus public evidence, unverified recipient metadata, restart persistence, decision scope/single use, invalid OTP retry, required PAUSE acknowledgment, version metadata, customer-bound reset and analytics authorization. Frontend tests use jsdom; they do not establish browser layout quality or accessibility certification.

A real-browser visual check was attempted, but Chromium was unavailable and its download returned invalid archive content. No new browser screenshot or end-to-end browser pass is claimed. Existing screenshots retained from the original archive are not screenshots of Phase 2.

The Bangladesh Bank December 2025 PDF, exact police national statistics and separate direct BSS source could not be independently verified; manifest entries disclose this and omit unsupported values. The report uses dated historical observations, not a live national fraud estimate.

Remote CI, Python dependency audit, hosted secret scan, PostgreSQL migration/restart, multi-worker financial consistency, load testing, hosted deployment, production authentication, real wallet integration and representative real-user validation were not executed. Workflow configuration and documentation for these concerns are included without claiming production readiness.

The deliverable excludes dependency installations, generated raw training CSVs, database/session state, credentials, caches and build output. It includes trained synthetic demo models, reproducible source, tests, verified evidence manifest/report, evaluation outputs and setup instructions. Model version compatibility is checked by `start.sh`, which regenerates models when needed.
