"""Run the qa/DESIGN_RULES.md detectors (tools/design_lint.js) on every page state at 1440 and 390 px.
Usage: python3 tools/design_lint.py [--json]. Exit 1 on any hit."""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests')); from test_browser import answer, BANK
JS = (ROOT / 'tools/design_lint.js').read_text()
URL = (ROOT / 'index.html').as_uri(); LIVE = [c for c in BANK['challenges'] if not c.get('retired') and all(BANK['sources'][s]['verification']['status'] != 'quarantined' for s in c['sources'])]   # quarantined items are not played
ONE = {}
for c in LIVE: ONE.setdefault(c['format'], c['id'])

def states(every=False):
    yield 'home', URL, None
    for v in (41, 39, 40, 0, 60): yield f'home-done-{v}', URL + '?hero=ai01', f'hero:{v}'   # the locked try-it, near the study value and at both ends (audit 36)
    yield 'library', URL + '#library', None
    yield 'all-decisions', URL + '#studies', None   # the real hash (review 28: '#atlas' silently linted the home page)
    yield 'record-empty', URL + '#record', None
    for c in (LIVE if every else [next(x for x in LIVE if x['id'] == cid) for cid in ONE.values()] + [x for x in LIVE if x['format'] in ('allocate', 'delegate', 'rank', 'estimate', 'causal') and x['id'] not in ONE.values()]):   # at phone width: one per format plus every allocate, delegate and rank item   # every decision at desktop width (review 23)
        yield f"predict-{c['id']}", URL + '?play=' + c['id'], None
        yield f"reveal-{c['id']}", URL + '?play=' + c['id'], c
    yield 'record', URL, 'record'
    yield 'library-played', URL, 'library-played'
    yield 'reveal-theme-strip', URL, 'theme-strip'   # a wide reveal with other calls on the same principle   # review 26: the library changes once principles open

def live(errors):
    """Console (setup, lobby, open, revealed), projector (open, revealed) and a phone, on a real server."""
    import threading
    sys.path.insert(0, str(ROOT)); from server import app, classroom as cl
    import tempfile; app.STORE = cl.Store(Path(tempfile.mkdtemp()) / 'lint.sqlite3'); app.LIMIT = app.Limiter()
    srv = app.Server(('127.0.0.1', 0), app.Handler); threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{srv.server_address[1]}'; hits = []
    def grab(pg, name, w):
        pg.wait_for_timeout(900)
        for r, where, d in pg.evaluate(JS): hits.append((r, f'{name}@{w}', where, d))
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            inst = b.new_page(viewport={'width': 1440, 'height': 900}); inst.on('pageerror', lambda e: errors.append(('console', str(e))))
            inst.goto(base + '/classroom'); grab(inst, 'console-setup', 1440)
            inst.fill('#title', 'Lint class'); inst.click('text=Create the session'); code = inst.text_content('.join-code').strip(); grab(inst, 'console-lobby', 1440)
            ph = b.new_page(viewport={'width': 390, 'height': 844}); ph.goto(base + '/?room=' + code); ph.wait_for_selector('.room-wait'); grab(ph, 'phone-wait', 390)
            import urllib.request, random
            def post(path, d, cid):
                r = urllib.request.Request(base + path, data=json.dumps(d).encode(), headers={'Content-Type': 'application/json', 'X-Client-Id': cid})
                for _ in range(5):
                    try:
                        with urllib.request.urlopen(r) as fh: return json.loads(fh.read())
                    except urllib.error.HTTPError as e:
                        if e.code != 429: raise
                        import time; time.sleep(1)
            toks = [(f'lint{i:03d}', post(f'/api/rooms/{code}/join', {}, f'lint{i:03d}')['token']) for i in range(80)]   # a full room, so stacked marks are drawn at class size (audit 31)
            for f in ('rank', 'allocate', 'delegate', 'choice', 'estimate'):
                c = next(x for x in cl.CHALLENGES.values() if x['format'] == f)
                inst.locator('[data-act=picker]:visible').first.click() if inst.locator('[data-act=picker]:visible').count() else None
                inst.click(f'[data-open="{c["id"]}"]'); ph.wait_for_selector('#lock-btn', timeout=10000); grab(ph, f'phone-{f}', 390); grab(inst, f'console-open-{f}', 1440)
                if f == 'estimate':
                    e = c['estimate']; stp = e.get('step', 1)
                    for i, (cid_, tk) in enumerate(toks): post(f'/api/rooms/{code}/responses', {'token': tk, 'answer': e['target'] if i % 3 else e['min'] + round(random.random() * (e['max'] - e['min']) / stp) * stp, 'confidence': 60}, cid_)
                inst.locator('[data-act=projector]:visible').first.click(); grab(inst, f'projector-open-{f}', 1440); inst.locator('[data-act=projector]:visible').first.click()
                inst.click('text=Reveal to the room'); inst.wait_for_selector('.rv'); grab(inst, f'console-revealed-{f}', 1440)
                inst.locator('[data-act=projector]:visible').first.click(); grab(inst, f'projector-revealed-{f}', 1440); inst.locator('[data-act=projector]:visible').first.click()
            b.close()
    finally:
        srv.shutdown()
    return hits

def run():
    hits = []; errors = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w, h in ((1440, 900), (390, 844)):
            every_state = (w == 1440)
            for name, url, act in states(every=every_state):
                pg = b.new_page(viewport={'width': w, 'height': h}); pg.on('pageerror', lambda e: errors.append((name, str(e))))
                pg.goto(url); pg.wait_for_timeout(250)
                if isinstance(act, str) and act.startswith('hero:'):
                    pg.evaluate("v=>{const r=document.querySelector('#hero-range');r.value=v;r.dispatchEvent(new Event('input',{bubbles:true}))}", int(act[5:])); pg.click('[data-act=hero-lock]')
                elif act == 'theme-strip':
                    th = LIVE[0]['theme']; same = [x for x in LIVE if x.get('theme') == th][:5]
                    for x in same:
                        pg.goto(URL + '?play=' + x['id']); pg.wait_for_timeout(200); answer(pg, x); pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
                elif act in ('record', 'library-played'):
                    for cid in list(ONE.values())[:4]:
                        pg.goto(URL + '?play=' + cid); pg.wait_for_timeout(200); answer(pg, next(x for x in LIVE if x['id'] == cid)); pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
                    pg.goto(URL + ('#record' if act == 'record' else '#library')); pg.wait_for_timeout(300)
                elif act:
                    try: answer(pg, act); pg.click('#lock-btn', timeout=5000); pg.wait_for_selector('#r-h', timeout=5000)
                    except Exception as e: errors.append((name, 'could not play to the reveal: ' + str(e).splitlines()[0])); pg.close(); continue
                pg.wait_for_timeout(600 if every_state else 1300)
                for r, where, d in pg.evaluate(JS): hits.append((r, f'{name}@{w}', where, d))
                if act == 'theme-strip' and w == 1440:   # the strip appears from 1200 px, where it is drawn smallest (audit 34)
                    pg.set_viewport_size({'width': 1200, 'height': 900}); pg.wait_for_timeout(400)
                    for r, where, d in pg.evaluate(JS): hits.append((r, f'{name}@1200', where, d))
                pg.close()
        b.close()
    hits += live(errors)
    seen = set(); uniq = []
    for x in hits:
        k = (x[0], x[2], x[3]) 
        if k not in seen: seen.add(k); uniq.append(x)
    return uniq, errors

if __name__ == '__main__':
    hits, errors = run()
    if '--json' in sys.argv: print(json.dumps({'hits': hits, 'errors': errors}, indent=1)); sys.exit(1 if hits or errors else 0)
    from collections import Counter
    print('by rule:', dict(sorted(Counter(h[0] for h in hits).items())))
    for h in hits: print(' | '.join(h))
    for e in errors: print('R25 page error |', *e)
    sys.exit(1 if hits or errors else 0)
