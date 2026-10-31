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

def test_tutor_endpoint_curated(base):
    s, r, _ = req(base, '/api/tutor', {'question': 'How would I test this in my company?', 'challenge': next(iter(cl.CHALLENGES)), 'client': 'abc'})
    assert s == 200 and r['answer'] and r['mode'] in ('curated', 'ai', 'cache')
