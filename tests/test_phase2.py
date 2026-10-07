import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_public_evidence_manifest_has_provenance_and_no_fabricated_pdf_pages():
    from api.public_evidence import public_evidence
    data = public_evidence()
    assert data['kind'] == 'public_evidence'
    assert len(data['items']) >= 5
    sources = {s['id']: s for s in data['sources']}
    for item in data['items']:
        assert sources[item['source_id']]['status'] == 'verified'
        assert item['supports'] and item['limitations'] and item['relevance']
    assert not any(i.get('pdf_page') for i in data['items'])
    assert not any(i['relevance'] == 'Direct APP evidence' for i in data['items'] if i['id'] in ['dighi', 'faridpur'])
    assert all(s['url'].startswith('https://') for s in sources.values())


def test_recipient_risk_explains_history_without_accusing_new_recipient():
    from api.recipient import recipient_risk
    low = recipient_risk({'is_new_cp': 1, 'cp_count': 0, 'cp_age_days': 0}, {'confidence': 'none', 'reports': 0})
    assert low['level'] == 'medium' and low['verification_state'] == 'unverified'
    assert 'new_recipient' in low['reasons']
    high = recipient_risk({'is_new_cp': 0, 'cp_count': 5, 'cp_age_days': 30}, {'confidence': 'high', 'reports': 12})
    assert high['level'] == 'high' and high['reports'] == 12
    assert high['is_confirmed_malicious'] is False


def test_persistent_decision_survives_restart_and_is_scoped(tmp_path):
    from api.db import Database
    db = Database(f'sqlite:///{tmp_path / "decisions.db"}')
    db.save_decision('owner', 'D0001', 'K-restart', {'decision': 'pause', 'amount': 500, 'versions': {'model': 'hash'}})
    again = Database(f'sqlite:///{tmp_path / "decisions.db"}')
    assert again.load_decision('owner', 'D0001', 'K-restart')['decision'] == 'pause'
    assert again.load_decision('other', 'D0001', 'K-restart') is None
    assert again.finish_decision('owner', 'D0001', 'K-restart', 'cancel')
    assert again.load_decision('owner', 'D0001', 'K-restart') is None
    assert not again.finish_decision('owner', 'D0001', 'K-restart', 'proceed')


def test_benchmark_metrics_define_denominators_and_degenerate_cases():
    from ml.benchmark import classification_metrics
    m = classification_metrics([0, 0, 1, 1], [0.1, 0.9, 0.8, 0.2], 0.5)
    assert m['precision'] == 0.5 and m['recall'] == 0.5 and m['false_positive_rate'] == 0.5
    assert m['confusion_matrix'] == [[1, 1], [1, 1]]
    assert classification_metrics([0, 0], [0.1, 0.2], 0.5)['roc_auc'] is None


def test_demo_balance_goal_and_counter_survive_store_restart(tmp_path):
    from api.db import Database
    from api.store import Store
    db = Database(f'sqlite:///{tmp_path / "sessions.db"}')
    first = Store(db=db)
    state = first.session('restart-test', 'D0001')
    state.goal = {'target': 10000, 'created': '2026-10-08'}
    state.counter = 77
    first.persist('restart-test', 'D0001')
    second = Store(db=db)
    restored = second.session('restart-test', 'D0001')
    assert restored.goal['target'] == 10000 and restored.counter == 77
    assert restored.profile.balance == state.profile.balance
    assert second.session('another-session', 'D0001').goal is None


def test_paused_llm_explanation_rejects_safe_claim_even_with_same_numbers(monkeypatch):
    from api import explain
    monkeypatch.setenv('LLM_API_KEY', 'x')
    monkeypatch.setenv('LLM_MODEL', 'x')
    monkeypatch.setenv('LLM_DATA_RESIDENCY', 'allow_external')
    base = explain.explain('pause', [{'code': 'amount_vs_usual', 'ratio': 4.0, 'usual': 2000}], 8000, 'en')
    monkeypatch.setattr(explain, 'chat', lambda *a, **k: 'This payment is safe. ' + base['message'])
    assert explain.rephrase(base)['source'] == 'template'


@pytest.mark.skipif(not (ROOT / 'ml/models/meta.json').exists(), reason='train models first')
def test_demo_users_cannot_read_global_analytics_or_reset_other_bound_customer(monkeypatch):
    from fastapi.testclient import TestClient
    from api.main import app
    client = TestClient(app)
    monkeypatch.setenv('AUTH_REQUIRED', 'true')
    token = client.post('/auth/session', json={'customer_id': 'D0001'}).json()['access_token']
    h = {'Authorization': 'Bearer ' + token}
    assert client.get('/analytics?scope=all', headers=h).status_code == 403
    assert client.post('/demo/reset', json={'customer_id': 'D0002'}, headers=h).status_code == 403
    assert [c['customer_id'] for c in client.get('/customers', headers=h).json()] == ['D0001']


@pytest.mark.skipif(not (ROOT / 'ml/models/meta.json').exists(), reason='train models first')
def test_invalid_authorization_does_not_consume_pending_check():
    from fastapi.testclient import TestClient
    from api.main import app
    client = TestClient(app)
    h = {'X-Session': 'phase2-validation'}
    script = client.get('/demo/script', params={'customer_id': 'D0001'}, headers=h).json()
    item = next(s for s in script if s['id'] == 'reported_small')
    check = client.post('/check', json={'customer_id': 'D0001', 'type': item['type'], 'counterparty': item['counterparty'], 'amount': item['amount']}, headers=h).json()
    body = {'customer_id': 'D0001', 'check_id': check['check_id'], 'action': 'proceed'}
    assert client.post('/pay', json=body, headers=h).status_code == 400
    assert client.post('/pay', json=dict(body, otp='1234'), headers=h).status_code == 409
    assert client.post('/pay', json=dict(body, otp='1234', acknowledged=True), headers=h).status_code == 200
    assert client.post('/pay', json=dict(body, otp='1234', acknowledged=True), headers=h).status_code == 404
    assert check['versions']['decision_policy'] and check['timestamp']
    assert check['details']['recipient']['is_confirmed_malicious'] is False
