# Synthetic temporal ML benchmarks

Experimental result on synthetic simulated data; not real MFS performance.

Fit only on pre-validation records; validation F1 chooses thresholds; final temporal test used once. No refit or test tuning.

| Model | Precision | Recall | F1 | ROC-AUC | AP | FPR | FNR | Brier |
|---|---|---|---|---|---|---|---|---|
| Logistic Regression — basic | 0.0588 | 0.3148 | 0.0991 | 0.9529 | 0.0586 | 0.0298 | 0.6852 | 0.0973 |
| Random Forest — basic | 0.0732 | 0.1111 | 0.0882 | 0.9537 | 0.0782 | 0.0083 | 0.8889 | 0.0471 |
| LightGBM — basic | 0.1618 | 0.2037 | 0.1803 | 0.9715 | 0.1753 | 0.0062 | 0.7963 | 0.0428 |
| LightGBM + behavioral features | 0.5814 | 0.4630 | 0.5155 | 0.9865 | 0.5708 | 0.0020 | 0.5370 | 0.0094 |
| LightGBM + recipient history | 0.6818 | 0.5556 | 0.6122 | 0.9964 | 0.7442 | 0.0015 | 0.4444 | 0.0037 |
| LightGBM + stated purpose (idealized) | 0.9268 | 0.7037 | 0.8000 | 0.9990 | 0.9191 | 0.0003 | 0.2963 | 0.0016 |

PR-AUC here means average precision (AP), not trapezoidal PR area. FPR=FP/(FP+TN); FNR=FN/(FN+TP). Brier is an uncalibrated probability-error diagnostic; no post-hoc calibration was fitted. Confusion matrices, thresholds, exact features, split dates, software versions and hashes are in `evidence/evaluation/benchmarks.json`.

- Risk models can recover synthetic generator rules; no real-customer validation.
- Purpose ablation uses idealized truthful simulator purpose, unlike incomplete customer answers.
- No timestamped historical scam reports exist in the evaluation dataset; report-feature ablation is not evaluated.
- Basic categorical codes are integer encoded for all baselines; a richer encoding search was not performed.
- Single seed and fixed model configurations; no claim of statistical significance or optimal tuning.

Reproduce: `python -m data.generate && python -m ml.train && python -m ml.benchmark`.
