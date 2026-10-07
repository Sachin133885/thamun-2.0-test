"""Reproducible synthetic temporal benchmarks; no customer-performance claims."""
import hashlib
import json
import platform
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, brier_score_loss, confusion_matrix,
                             f1_score, precision_recall_curve, precision_score, recall_score, roc_auc_score)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from data.personas import PURPOSES
from ml.features import RISK_FEATURES
from ml.train import split

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence/evaluation'
BASE = ['log_amount', 'type_idx', 'cp_type_idx', 'hour']
RECIPIENT = ['is_new_cp', 'cp_count', 'cp_age_days', 'new_cp_24h', 'in_cp_ratio']
BEHAVIOR = [x for x in RISK_FEATURES if x not in RECIPIENT]


def classification_metrics(y, probability, threshold):
    y = np.asarray(y, dtype=int)
    p = np.asarray(probability, dtype=float)
    guess = p >= threshold
    tn, fp, fn, tp = confusion_matrix(y, guess, labels=[0, 1]).ravel()
    both = len(np.unique(y)) == 2
    return {'samples': len(y), 'positive_samples': int(y.sum()), 'positive_prevalence': float(y.mean()),
            'precision': float(precision_score(y, guess, zero_division=0)),
            'recall': float(recall_score(y, guess, zero_division=0)),
            'f1': float(f1_score(y, guess, zero_division=0)),
            'roc_auc': float(roc_auc_score(y, p)) if both else None,
            'pr_auc_average_precision': float(average_precision_score(y, p)) if both else None,
            'false_positive_rate': float(fp / (fp + tn)) if fp + tn else None,
            'false_negative_rate': float(fn / (fn + tp)) if fn + tp else None,
            'brier_score': float(brier_score_loss(y, p)), 'threshold': float(threshold),
            'confusion_matrix': [[int(tn), int(fp)], [int(fn), int(tp)]]}


def select_threshold(y, p):
    precision, recall, thresholds = precision_recall_curve(y, p)
    if not len(thresholds):
        return 0.5
    score = 2 * precision[:-1] * recall[:-1] / np.maximum(precision[:-1] + recall[:-1], 1e-12)
    return float(thresholds[int(np.argmax(score))])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    path = ROOT / 'data/out/features.csv'
    table = pd.read_csv(path, parse_dates=['ts'], keep_default_na=False)
    purpose_codes = {code: index + 1 for index, code in enumerate(PURPOSES)}
    table['purpose_idx'] = table.purpose.map(lambda s: purpose_codes.get(s, 0))
    fit, valid, _, test = split(table)
    groups = [
        ('Logistic Regression — basic', BASE, 'lr'),
        ('Random Forest — basic', BASE, 'rf'),
        ('LightGBM — basic', BASE, 'lgb'),
        ('LightGBM + behavioral features', list(dict.fromkeys(BASE + BEHAVIOR)), 'lgb'),
        ('LightGBM + recipient history', list(dict.fromkeys(BASE + BEHAVIOR + RECIPIENT)), 'lgb'),
        ('LightGBM + stated purpose (idealized)', list(dict.fromkeys(BASE + BEHAVIOR + RECIPIENT + ['purpose_idx'])), 'lgb'),
    ]
    results, saved_scores = [], {}
    for name, features, kind in groups:
        x, y = fit[features].to_numpy(), fit.is_scam.to_numpy(dtype=int)
        if kind == 'lr':
            model = make_pipeline(StandardScaler(), LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
        elif kind == 'rf':
            model = RandomForestClassifier(n_estimators=120, max_depth=10, min_samples_leaf=10,
                                           class_weight='balanced', n_jobs=2, random_state=42)
        else:
            model = lgb.LGBMClassifier(n_estimators=180, num_leaves=15, learning_rate=0.05,
                                      class_weight='balanced', n_jobs=2, random_state=42, verbosity=-1)
        model.fit(x, y)
        vp = model.predict_proba(valid[features].to_numpy())[:, 1]
        threshold = select_threshold(valid.is_scam, vp)
        tp = model.predict_proba(test[features].to_numpy())[:, 1]
        results.append({'model': name, 'features': features, 'metrics': classification_metrics(test.is_scam, tp, threshold)})
        saved_scores[name] = (tp, threshold)
        print(name, 'F1=', round(results[-1]['metrics']['f1'], 4), flush=True)
    data = {'label': 'Experimental result on synthetic simulated data; not real MFS performance',
            'seed': 42, 'dataset_sha256': hashlib.sha256((ROOT / 'data/out/transactions.csv').read_bytes()).hexdigest(),
            'splits': {k: {'rows': len(v), 'from': str(v.ts.min()), 'to': str(v.ts.max())} for k, v in [('fit', fit), ('validation', valid), ('test', test)]},
            'protocol': 'Fit only on pre-validation records; validation F1 chooses thresholds; final temporal test used once. No refit or test tuning.',
            'versions': {'python': platform.python_version(), 'numpy': np.__version__, 'pandas': pd.__version__,
                         'sklearn': sklearn.__version__, 'lightgbm': lgb.__version__},
            'models': results, 'limitations': [
                'Risk models can recover synthetic generator rules; no real-customer validation.',
                'Purpose ablation uses idealized truthful simulator purpose, unlike incomplete customer answers.',
                'No timestamped historical scam reports exist in the evaluation dataset; report-feature ablation is not evaluated.',
                'Basic categorical codes are integer encoded for all baselines; a richer encoding search was not performed.',
                'Single seed and fixed model configurations; no claim of statistical significance or optimal tuning.']}
    (OUT / 'benchmarks.json').write_text(json.dumps(data, indent=2))
    headline = '# Synthetic temporal ML benchmarks\n\n' + data['label'] + '.\n\n' + data['protocol'] + '\n\n'
    headline += '| Model | Precision | Recall | F1 | ROC-AUC | AP | FPR | FNR | Brier |\n|---|---|---|---|---|---|---|---|---|\n'
    for row in results:
        m = row['metrics']
        headline += '| ' + row['model'] + ' | ' + ' | '.join(f'{m[k]:.4f}' if m[k] is not None else 'undefined' for k in
                     ['precision', 'recall', 'f1', 'roc_auc', 'pr_auc_average_precision', 'false_positive_rate', 'false_negative_rate', 'brier_score']) + ' |\n'
    headline += '\nPR-AUC here means average precision (AP), not trapezoidal PR area. FPR=FP/(FP+TN); FNR=FN/(FN+TP). Brier is an uncalibrated probability-error diagnostic; no post-hoc calibration was fitted. Confusion matrices, thresholds, exact features, split dates, software versions and hashes are in `evidence/evaluation/benchmarks.json`.\n\n'
    headline += '\n'.join('- ' + s for s in data['limitations'])
    headline += '\n\nReproduce: `python -m data.generate && python -m ml.train && python -m ml.benchmark`.\n'
    (ROOT / 'docs/ml_evaluation.md').write_text(headline)
    (ROOT / 'docs/ablation_study.md').write_text('# Feature and policy ablations\n\n' + headline.split('\n\n', 1)[1] +
        '\n\nFeature ablations are rows 3–6. Improvements are descriptive, not causal evidence. Recipient intelligence in the serving policy is rule-based; recipient history features are evaluated here independently. Report ablation is unavailable, not silently assumed effective.\n')
    # A reproducible generic comparator: pause every transfer to a first-time recipient.
    p, threshold = saved_scores['LightGBM + recipient history']
    model_pause = p >= threshold
    from api.engine import needs_purpose, purpose_rules
    rules = np.array([bool(purpose_rules({'amount': r['amount']}, r['purpose'], r))
                      if needs_purpose(r, r, True) else False for r in test.to_dict('records')])
    adaptive = (model_pause & (test.amount.to_numpy() >= 300)) | rules
    generic = (test.is_new_cp.to_numpy() == 1)
    def policy(name, mask):
        m = classification_metrics(test.is_scam, mask.astype(float), 0.5)
        return {'name': name, 'pause_rate': float(mask.mean()), 'paused': int(mask.sum()),
                'fraud_coverage': m['recall'], 'false_pause_rate': m['false_positive_rate'],
                'false_pauses': m['confusion_matrix'][0][1]}
    policies = [policy('Generic: pause every new-recipient payment', generic), policy('Model only', model_pause),
                policy('Purpose rules only (idealized)', rules), policy('Model + purpose rules, materiality policy', adaptive)]
    fatigue = {'label': 'Simulation result — not real customer data', 'samples': len(test), 'policies': policies,
               'continuation': None, 'cancellation': None,
               'limitations': 'Offline friction proxy. No behavior assumptions, user research, coaching nudges or historical report effects included. Not a full deployed-policy replay.'}
    (OUT / 'alert_fatigue.json').write_text(json.dumps(fatigue, indent=2))
    doc = '# Alert frequency and policy ablation\n\n' + fatigue['label'] + '.\n\n' + fatigue['limitations'] + '\n\n'
    doc += '| Policy | Pause rate | Synthetic fraud coverage | Legitimate false-pause rate |\n|---|---|---|---|\n'
    for row in policies:
        doc += f"| {row['name']} | {row['pause_rate']:.4f} | {row['fraud_coverage']:.4f} | {row['false_pause_rate']:.4f} |\n"
    doc += '\nDenominators: all test attempts for pause rate, scam-labeled attempts for coverage, legitimate-labeled attempts for false pauses. No user continuation, cancellation or monetary loss avoided is estimated. Lower warning frequency does not establish reduced human alert fatigue.\n'
    (ROOT / 'docs/alert_fatigue_evaluation.md').write_text(doc)
    existing = json.loads((ROOT / 'ml/models/meta.json').read_text())
    booster = lgb.Booster(model_file=str(ROOT / 'ml/models/risk.txt'))
    vp = booster.predict(valid[RISK_FEATURES])
    edges = [0.01, 0.05, 0.1, 0.25, 0.5, 0.75]
    counts = np.bincount(np.searchsorted(edges, vp, side='right'), minlength=len(edges)+1)
    reference = {'score_edges': edges, 'score_shares': (counts / len(vp)).tolist(),
                 'high_risk_share': float((vp >= existing['risk']['threshold']).mean()),
                 'label': 'Synthetic retrospective validation-period reference; serving model includes validation-period training.',
                 'model_sha256': hashlib.sha256((ROOT / 'ml/models/risk.txt').read_bytes()).hexdigest()}
    import joblib
    from ml.risk import isolation_scores
    anomaly = isolation_scores(joblib.load(ROOT / 'ml/models/isolation_forest.pkl'), existing['risk']['iso_scale'], valid)
    reference['high_risk_share'] = float(((vp >= existing['risk']['threshold']) | (anomaly >= existing['risk']['iso_threshold'])).mean())
    (ROOT / 'evidence/reference.json').write_text(json.dumps(reference, indent=2))
    # Serve only generated summaries to the frontend; never export transaction records.
    public = ROOT / 'web/public/evidence'
    (public / 'benchmarks.json').write_text(json.dumps(data, indent=2))
    (public / 'alert_fatigue.json').write_text(json.dumps(fatigue, indent=2))


if __name__ == '__main__':
    main()
