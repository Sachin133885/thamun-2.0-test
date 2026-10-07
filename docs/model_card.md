# Thamun model card

**Purpose:** Screen synthetic pre-authorization payment attempts and demonstrate explainable intervention. Intended for hackathon demonstration and offline research; out of scope: real financial authorization, automatic account restriction, definitive scammer identification or production loss prevention.

**Models:** Existing LightGBM binary scam classifier, LightGBM payment-category classifier, Isolation Forest anomaly detector. TreeSHAP uses LightGBM `pred_contrib`; SHAP is an explanation of model output, not causal evidence.

**Data:** Fixed-seed transaction simulator, four synthetic personas, April–September 2026. Training/validation chronology and exact software/artifact metadata are in `ml/models/meta.json`. Category and risk pipelines preserve the existing August-validation / September-hold-out protocol; benchmark models fit April–July only and tune thresholds in August without refitting.

**Features:** Historical amount ranks/ratios, balance share, recipient history, hourly behavior and payment velocity, incoming-fund context, history length and payment/recipient types. Features are computed before each transaction updates customer state. Purpose rules and report confidence are independent policy inputs. No historical report dataset exists for report-feature ML ablation.

**Results:** `docs/evaluation.md` covers the original synthetic full-policy replay; `docs/ml_evaluation.md` covers calculated model benchmarks, FPR/FNR, AP and Brier. Metrics are not interchangeable: original serving policy includes anomaly, purpose, bills and coaching, while benchmarks isolate feature groups and use different validation-selected thresholds. Idealized truthful purpose and true historical categories in simulator replay are optimistic assumptions.

**Risks:** False pauses interrupt legitimate unfamiliar/high-value payments; false negatives can miss manipulated routine transfers. Cold-start behavior, adversarial reporting, unobserved recipient/device signals, label shift and synthetic distribution mismatch remain unresolved. Scores are not calibrated production fraud probabilities.

**Oversight:** Explain supported reasons, label unverified reports, allow cancel/acknowledged continuation, and persist versioned snapshots and actions. Model version is the risk artifact's SHA-256 prefix; feature schema and decision-policy identifiers accompany decisions. Checkpoints are not a registry service.

**Retraining:** Review score distribution shift alongside confirmed outcome labels; validate replacement artifacts on fresh time periods, assess subgroup effects, recalibrate and review thresholds. No automatic production retraining is implemented. Training-distribution comparison is a lightweight score-drift prototype, not full feature monitoring.
