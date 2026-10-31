"""Classroom store: lifecycle, permissions, validation, concurrency, aggregates, export, retention."""
import concurrent.futures, json, time
import pytest
from server import classroom as cl
from conftest import BANK

def pick(fmt):
    return next(c for c in cl.CHALLENGES.values() if c['format'] == fmt)

@pytest.fixture
def store(tmp_path): return cl.Store(tmp_path / 't.sqlite3')

def test_lifecycle_and_permissions(store):
    s = store.create('MBA 610'); code, key = s['code'], s['secret']
    assert len(code) == 5 and store.state(code)['phase'] == 'lobby'
    with pytest.raises(cl.Forbidden): store.control(code, 'wrong', 'open', pick('choice')['id'])
    p = store.join(code)
    with pytest.raises(cl.Conflict): store.submit(code, p['token'], 0, 50)  # nothing open
    c = pick('choice'); store.control(code, key, 'open', c['id'])
    assert store.submit(code, p['token'], c['answer'], 80)['accepted']
    assert not store.submit(code, p['token'], c['answer'], 80)['accepted']  # one answer per decision
    assert 'aggregate' not in store.state(code)  # hidden until reveal
    store.control(code, key, 'reveal')
    agg = store.state(code)['aggregate']; assert agg['n'] == 1 and agg['shareCorrect'] == 100
    with pytest.raises(cl.Conflict): store.submit(code, store.join(code)['token'], 0, 50)  # closed after reveal
    with pytest.raises(cl.Forbidden): store.submit(code, 'not-a-token', 0, 50)

def test_validation_every_format(store):
    s = store.create(); code, key = s['code'], s['secret']; tok = store.join(code)['token']
    bad = {'choice': 99, 'causal': -1, 'multi': [0, 0], 'estimate': 1e12, 'forecast': 101, 'rank': [0, 0, 1], 'allocate': [100, 100, 0], 'delegate': ['x']}
    for fmt, b in bad.items():
        c = pick(fmt); store.control(code, key, 'open', c['id'])
        with pytest.raises(cl.ClassroomError): store.submit(code, tok, b, 50)

def test_fifty_concurrent_students(store):
    s = store.create(); code, key = s['code'], s['secret']; c = pick('estimate'); store.control(code, key, 'open', c['id'])
    toks = [store.join(code)['token'] for _ in range(50)]
    lo, hi = c['estimate']['min'], c['estimate']['max']
    with concurrent.futures.ThreadPoolExecutor(50) as ex:
        res = list(ex.map(lambda i: store.submit(code, toks[i], lo + (hi - lo) * i // 49, 60), range(50)))
    assert all(r['accepted'] for r in res) and store.state(code, admin=True)['responses'] == 50
    store.control(code, key, 'reveal'); a = store.state(code)['aggregate']
    assert a['n'] == 50 and sum(a['hist']) == 50 and a['median'] is not None

def test_aggregate_shapes(store):
    s = store.create(); code, key = s['code'], s['secret']; toks = [store.join(code)['token'] for _ in range(3)]
    for fmt in ('choice', 'multi', 'forecast', 'rank', 'allocate', 'delegate'):
        c = pick(fmt); store.control(code, key, 'open', c['id'])
        for t in toks:
            r = {'choice': lambda: 0, 'multi': lambda: [0, 1], 'forecast': lambda: 70, 'rank': lambda: list(range(len(c['options']))),
                 'allocate': lambda: [c['allocate']['total']] + [0] * (len(c['options']) - 1), 'delegate': lambda: [0] * len(c['delegate']['tasks'])}[fmt]()
            assert store.submit(code, t, r, 50)['accepted']
        store.control(code, key, 'reveal'); a = store.state(code)['aggregate']; assert a['n'] == 3
        key_field = {'choice': 'counts', 'multi': 'counts', 'forecast': 'hist', 'rank': 'meanPosition', 'allocate': 'meanShare', 'delegate': 'taskCounts'}[fmt]
        assert key_field in a, (fmt, a)

def test_export_is_admin_only_and_safe(store):
    s = store.create(); code, key = s['code'], s['secret']; c = pick('choice'); store.control(code, key, 'open', c['id'])
    store.submit(code, store.join(code)['token'], 0, 50)
    with pytest.raises(cl.Forbidden): store.export_csv(code, 'nope')
    out = store.export_csv(code, key); assert out.splitlines()[0].startswith('participant,') and 'P001' in out
    assert 'token' not in out.lower()

def test_retention_purge(store, monkeypatch):
    s = store.create(); monkeypatch.setattr(cl, 'RETENTION_HOURS', 0.0)
    time.sleep(0.01); assert store.purge() >= 1
    with pytest.raises(cl.NotFound): store.state(s['code'])

def test_end_deletes_everything(store):
    s = store.create(); store.join(s['code']); store.control(s['code'], s['secret'], 'end')
    with pytest.raises(cl.NotFound): store.state(s['code'])

def test_public_challenge_hides_answers():
    for c in cl.CHALLENGES.values():
        keys = set()
        def walk(o):
            if isinstance(o, dict): keys.update(o); [walk(v) for v in o.values()]
            elif isinstance(o, list): [walk(v) for v in o]
        walk(cl.public_challenge(c))
        assert not keys & {'answer', 'multiAnswers', 'rankAnswer', 'target', 'truth', 'values', 'valueLabels', 'why', 'explain', 'answerTitle', 'implication', 'boundary', 'follow', 'chart', 'tolerance'}, c['id']
