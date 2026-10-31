"""End-to-end over real HTTP: static pages, headers, a full classroom round, a 50-client load run, abuse limits."""
import concurrent.futures, json, threading, time, urllib.request, urllib.error
import pytest
from server import app, classroom as cl

@pytest.fixture(scope='module')
def base(tmp_path_factory):
    app.STORE = cl.Store(tmp_path_factory.mktemp('db') / 'h.sqlite3')
    srv = app.Server(('127.0.0.1', 0), app.Handler); t = threading.Thread(target=srv.serve_forever, daemon=True); t.start()
    yield f'http://127.0.0.1:{srv.server_address[1]}'
    srv.shutdown()

def req(base, path, data=None, key=None, client='c1', method=None, raw=False):
    h = {'X-Client-Id': client}
    if data is not None: h['Content-Type'] = 'application/json'
    if key: h['X-Instructor-Key'] = key
    r = urllib.request.Request(base + path, data=None if data is None else json.dumps(data).encode(), headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=10) as resp: body = resp.read(); return resp.status, (body if raw else json.loads(body)), resp.headers
    except urllib.error.HTTPError as e: return e.code, json.loads(e.read() or b'{}'), e.headers

def test_static_and_headers(base):
    for p in ('/', '/classroom'):
        s, body, h = req(base, p, raw=True)
        assert s == 200 and b'<!doctype html>' in body.lower()[:40]
        assert "frame-ancestors" in h['Content-Security-Policy'] and h['X-Content-Type-Options'] == 'nosniff'
    assert req(base, '/api/health')[1]['ok']
    assert req(base, '/../server/app.py')[0] == 404

def test_full_round(base):
    s, room, _ = req(base, '/api/rooms', {'title': 'Exec Ed'}); assert s == 201
    code, key = room['code'], room['secret']
    st, state, _ = req(base, f'/api/rooms/{code}'); assert state['phase'] == 'lobby' and not state['admin']
    assert req(base, f'/api/rooms/{code}', key=key)[1]['admin']
    c = next(x for x in cl.CHALLENGES.values() if x['format'] == 'choice')
    assert req(base, f'/api/rooms/{code}/control', {'action': 'open', 'challenge': c['id']}, key='bad')[0] == 403
    assert req(base, f'/api/rooms/{code}/control', {'action': 'open', 'challenge': c['id']}, key=key)[0] == 200
    toks = [req(base, f'/api/rooms/{code}/join', {}, client=f'p{i}')[1]['token'] for i in range(5)]
    for i, t in enumerate(toks): assert req(base, f'/api/rooms/{code}/responses', {'token': t, 'answer': i % len(c['options']), 'confidence': 70}, client=f'p{i}')[1]['accepted']
    st = req(base, f'/api/rooms/{code}')[1]; assert st['responses'] == 5 and 'aggregate' not in st and 'answer' not in json.dumps(st['decision'])
    assert req(base, f"/api/rooms/{code}?v={st['etag']}")[1] == {'same': True}
    req(base, f'/api/rooms/{code}/control', {'action': 'reveal'}, key=key)
    agg = req(base, f'/api/rooms/{code}')[1]['aggregate']; assert agg['n'] == 5 and sum(agg['counts']) == 5
    s, csv, h = req(base, f'/api/rooms/{code}/export.csv', key=key, raw=True); assert s == 200 and b'participant' in csv
    assert req(base, f'/api/rooms/{code}/export.csv')[0] == 403

def test_fifty_phones_polling_and_submitting(base):
    _, room, _ = req(base, '/api/rooms', {'title': 'load'}, client='inst2'); code, key = room['code'], room['secret']
    c = next(x for x in cl.CHALLENGES.values() if x['format'] == 'estimate')
    req(base, f'/api/rooms/{code}/control', {'action': 'open', 'challenge': c['id']}, key=key, client='inst2')
    lat = []
    def student(i):
        cid = f'load{i}'; t = req(base, f'/api/rooms/{code}/join', {}, client=cid)[1]['token']
        time.sleep(i * 0.01)  # phones join over half a second
        for _ in range(6):  # polling at 2 Hz, four times faster than the shipped client
            t0 = time.time(); s, _, _ = req(base, f'/api/rooms/{code}', client=cid); lat.append(time.time() - t0); assert s == 200
            time.sleep(0.5)
        s, r, _ = req(base, f'/api/rooms/{code}/responses', {'token': t, 'answer': c['estimate']['min'], 'confidence': 50}, client=cid)
        return s, r
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(50) as ex: res = list(ex.map(student, range(50)))
    elapsed = time.time() - t0
    assert all(s == 200 and r['accepted'] for s, r in res)
    assert req(base, f'/api/rooms/{code}', key=key, client='inst2')[1]['responses'] == 50
    lat.sort(); p95 = lat[int(len(lat) * .95)]
    print(f'\n50 clients x 6 polls + submit: {elapsed:.2f}s total, p95 poll latency {p95*1000:.0f} ms')
    assert p95 < 1.0

def test_abuse_limits(base):
    assert req(base, '/api/rooms/ZZZZZ/join', {}, client='x')[0] == 404
    big = urllib.request.Request(base + '/api/tutor', data=b'{"question":"' + b'a' * 9000 + b'"}', headers={'Content-Type': 'application/json'})
    with pytest.raises(urllib.error.HTTPError) as e: urllib.request.urlopen(big)
    assert e.value.code == 400
    bad = urllib.request.Request(base + '/api/rooms', data=b'not json', headers={'Content-Type': 'application/json'})
    with pytest.raises(urllib.error.HTTPError) as e: urllib.request.urlopen(bad)
    assert e.value.code == 400
    codes = [req(base, '/api/health', client='hammer')[0] for _ in range(60)]
    assert 429 in codes  # per-client read bucket

def test_tutor_endpoint_curated(base, tmp_path, monkeypatch):
    monkeypatch.setattr(app, 'STORE', cl.Store(tmp_path / 't.sqlite3'))
    s, r, _ = req(base, '/api/tutor', {'question': 'How would I test this in my company?', 'challenge': next(iter(cl.CHALLENGES)), 'client': 'abc'})
    assert s == 200 and r['answer'] and r['mode'] in ('curated', 'ai', 'cache')

def test_served_pages_carry_no_answers(base):
    import re
    for p in ('/', '/classroom'):
        s, body, _ = req(base, p, raw=True)
        m = re.search(rb'<script>const BANK = (.*?);</script>', body, re.S); bank = json.loads(m.group(1))
        assert bank['public'] is True
        keys = set()
        def walk(o):
            if isinstance(o, dict): keys.update(o); [walk(v) for v in o.values()]
            elif isinstance(o, list): [walk(v) for v in o]
        walk(bank['challenges'])
        assert not keys & {'answer', 'multiAnswers', 'rankAnswer', 'target', 'truth', 'values', 'explain', 'answerTitle', 'why'}, p
        # Review 3, B1/M1: no answer-bearing text anywhere in the page bytes (sources, themes, diagrams included).
        text = body.decode('utf-8'); leaks = []
        for c in cl.BANK['challenges']:
            if c['id'] not in cl.CHALLENGES: continue
            probes = [c['answerTitle'], c['explain'], c['implication']] + [f['a'] for f in c['follow']]
            probes += [cl.BANK['sources'][s]['takeaway'] for s in c['sources'] if cl.BANK['sources'][s].get('takeaway')]
            if 'dag' in c: probes += [c['dag']['alt']] + [n['label'] for n in c['dag']['nodes'] if n.get('mask')]
            leaks += [(c['id'], x[:50]) for x in probes if x and json.dumps(x, ensure_ascii=False)[1:-1].replace('</', '<\\/') in text]
        leaks += [('theme', t['id']) for t in cl.BANK.get('themes', []) if json.dumps(t['principle'], ensure_ascii=False)[1:-1] in text]
        assert not leaks, (p, leaks[:8])

def test_class_lock_holds_evidence_until_revealed(base, tmp_path, monkeypatch):
    monkeypatch.setattr(app, 'STORE', cl.Store(tmp_path / 'lock.sqlite3'))
    c = next(x for x in cl.CHALLENGES.values() if x['format'] == 'forecast')
    other = next(x for x in cl.CHALLENGES.values() if x['id'] != c['id'])
    s, full, _ = req(base, '/api/reveal/' + c['id']); assert s == 200 and 'truth' in full['forecast']   # no class: practice is open
    _, room, _ = req(base, '/api/rooms', {'title': 'block'}, client='inst9'); key = room['secret']
    req(base, f"/api/rooms/{room['code']}/join", {}, client='stu1')                                     # a class with a participant locks evidence
    req(base, f"/api/rooms/{room['code']}/control", {'action': 'open', 'challenge': c['id']}, key=key, client='inst9')
    for cid in (c['id'], other['id']):
        assert req(base, '/api/reveal/' + cid, client='peek')[0] == 409, cid                             # nothing leaks, open or not
    lib = req(base, '/api/library', client='peek')[1]; assert lib['class_lock'] and not lib['challenges']
    t = req(base, '/api/tutor', {'question': 'How big is this effect in practice?', 'challenge': c['id'], 'client': 'peek'})[1]
    assert t['mode'] == 'locked' and 'truth' not in json.dumps(t)
    req(base, f"/api/rooms/{room['code']}/control", {'action': 'reveal'}, key=key, client='inst9')
    st = req(base, f"/api/rooms/{room['code']}", client='peek')[1]; assert st['evidence']['id'] == c['id']
    app.STORE._lock = None
    assert req(base, '/api/reveal/' + c['id'], client='peek')[0] == 200                                  # revealed decisions open up
    assert req(base, '/api/reveal/' + other['id'], client='peek')[0] == 409
    req(base, f"/api/rooms/{room['code']}/control", {'action': 'end'}, key=key, client='inst9'); app.STORE._lock = None
    assert req(base, '/api/reveal/' + other['id'], client='peek')[0] == 200                              # class over: practice returns

def test_join_can_be_closed(base, tmp_path, monkeypatch):
    monkeypatch.setattr(app, 'STORE', cl.Store(tmp_path / 'j.sqlite3'))
    _, room, _ = req(base, '/api/rooms', {'title': 'j'}, client='inst6')
    req(base, f"/api/rooms/{room['code']}/control", {'action': 'lockjoin'}, key=room['secret'], client='inst6')
    assert req(base, f"/api/rooms/{room['code']}/join", {}, client='late')[0] == 409

def test_instructor_bank_needs_key(base):
    _, room, _ = req(base, '/api/rooms', {'title': 'bank'}, client='inst8')
    assert req(base, f"/api/instructor/bank?code={room['code']}", client='inst8')[0] == 403
    s, d, _ = req(base, f"/api/instructor/bank?code={room['code']}", key=room['secret'], client='inst8'); assert s == 200 and 'answerTitle' in d['challenges'][0]

def test_public_host_requires_passcode(base, monkeypatch):
    monkeypatch.setattr(app, 'LOOPBACK', False); monkeypatch.setattr(app, 'PASSCODE', '')
    assert req(base, '/api/rooms', {'title': 'x'}, client='pub')[0] == 403
    monkeypatch.setattr(app, 'PASSCODE', 'sesame')
    assert req(base, '/api/rooms', {'title': 'x', 'passcode': 'nope'}, client='pub')[0] == 403
    assert req(base, '/api/rooms', {'title': 'x', 'passcode': 'sesame'}, client='pub')[0] == 201

def test_forwarded_for_uses_rightmost(base, monkeypatch):
    monkeypatch.setattr(app, 'TRUST_PROXY', True)
    h = app.Handler.__new__(app.Handler); h.headers = {'X-Forwarded-For': 'spoofed, 10.0.0.9'}; h.client_address = ('127.0.0.1', 1)
    assert h.ip() == '10.0.0.9'

def test_join_flood_limited(base):
    _, room, _ = req(base, '/api/rooms', {'title': 'flood'}, client='inst7')
    codes = [req(base, f"/api/rooms/{room['code']}/join", {}, client=f'f{i}')[0] for i in range(110)]
    assert codes.count(200) <= 75 and 429 in codes
