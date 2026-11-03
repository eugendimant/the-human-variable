"""Real-browser checks: every format plays and reveals, keyboard play, no overflow at phone width, axe accessibility,
and a live-classroom round with three phones. Skipped when Playwright or Chromium is unavailable."""
import json, re, threading
from pathlib import Path
import pytest
pw = pytest.importorskip('playwright.sync_api')
ROOT = Path(__file__).resolve().parents[1]
BANK = json.loads((ROOT / 'src/bank.json').read_text())
BY = {c['id']: c for c in BANK['challenges']}
LIVE = [c for c in BANK['challenges'] if all(BANK['sources'][s]['verification']['status'] != 'quarantined' for s in c['sources'])]
URL = (ROOT / 'index.html').as_uri()
AXE = (ROOT / 'tests/vendor/axe.min.js')

@pytest.fixture(scope='module')
def browser():
    with pw.sync_playwright() as p:
        try: b = p.chromium.launch()
        except Exception as e: pytest.skip(f'Chromium unavailable: {e}')
        yield b; b.close()

def page(browser, w=1440, h=900):
    pg = browser.new_page(viewport={'width': w, 'height': h}); pg.errors = []
    pg.on('pageerror', lambda e: pg.errors.append(str(e)))
    pg.on('console', lambda m: m.type == 'error' and pg.errors.append(m.text))
    return pg

def answer(pg, c):
    f = c['format']
    if f in ('choice', 'causal'): pg.keyboard.press('1')
    elif f == 'multi': pg.keyboard.press('1'); pg.keyboard.press('2')
    elif f in ('estimate', 'forecast'):
        sel = '#est' if f == 'estimate' else '#fc'
        pg.eval_on_selector(sel, "e=>{e.value=e.min;e.dispatchEvent(new Event('input',{bubbles:true}))}")
    elif f == 'rank': pg.click('[data-rank="0"][data-dir="1"]')
    elif f == 'allocate': pass  # starts as an even split that sums to the budget
    elif f == 'delegate':
        for i in range(len(c['delegate']['tasks'])): pg.click(f'[data-deleg="{i}"][data-pick="0"]')
    if f == 'allocate':  # move one slider so the split is the player's own
        pg.eval_on_selector('[data-alloc="0"]', "e=>{e.value=+e.value+10;e.dispatchEvent(new Event('input',{bubbles:true}))}")
    if f not in ('forecast', 'allocate'):
        pg.eval_on_selector('#conf', "e=>{e.value=70;e.dispatchEvent(new Event('input',{bubbles:true}))}")

def one_of_each():
    seen = {}
    for c in LIVE: seen.setdefault(c['format'], c)
    return list(seen.values())

@pytest.mark.parametrize('w,h', [(1440, 900), (390, 844)])
def test_every_format_plays_and_reveals(browser, w, h):
    for c in one_of_each():
        pg = page(browser, w, h); pg.goto(URL + '?play=' + c['id'])
        assert not pg.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), ('predict', c['id'], w)
        answer(pg, c)
        assert pg.is_enabled('#lock-btn'), c['id']
        pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
        assert pg.locator('#gap-h').count() == 1, c['id']
        assert not pg.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), (c['id'], w)
        assert not pg.errors, (c['id'], pg.errors)
        rec = pg.evaluate('THV.records()'); assert rec[-1]['id'] == c['id'] and -1 <= rec[-1]['score'] <= 1
        pg.close()

def test_keyboard_round_and_record(browser):
    pg = page(browser); pg.goto(URL)
    pg.click('[data-act="toggle-custom"]'); pg.click('[data-length="5"]'); pg.click('[data-act="start"]')
    for _ in range(12):
        if pg.locator('#lock-btn').count() == 0: break
        c = next(x for x in LIVE if x['id'] == pg.evaluate('THV.st.deck[THV.st.i].id'))
        answer(pg, c); pg.focus('#q-h'); pg.keyboard.press('Enter')
        pg.wait_for_selector('#r-h'); pg.keyboard.press('n')
    pg.wait_for_selector('text=Round complete')
    assert pg.locator('.score-big').count() == 1 and pg.locator('.score-meta div').count() == 1 and pg.locator('.cal-sum').count() <= 1 and not pg.errors

def test_quarantined_items_never_served(browser):
    pg = page(browser); pg.goto(URL)
    ids = set(pg.evaluate('THV.ALL.map(c=>c.id)'))
    bad = {c['id'] for c in BANK['challenges']} - {c['id'] for c in LIVE}
    assert bad and not (ids & bad)

@pytest.mark.parametrize('view', ['home', 'play', 'reveal', 'record', 'almanac', 'atlas'])
def test_axe_no_serious_violations(browser, view):
    pg = page(browser); c = next(x for x in LIVE if x['format'] == 'estimate')
    pg.goto(URL + ('?play=' + c['id'] if view in ('play', 'reveal') else ''))
    if view == 'reveal': answer(pg, c); pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
    if view in ('record', 'almanac', 'atlas'): pg.evaluate("document.querySelector('[data-nav=almanac]').click()") if view != 'record' else None
    if view in ('record', 'atlas'): pg.evaluate(f"document.querySelector('[data-nav={view}]').click()")
    pg.add_script_tag(path=str(AXE))
    res = pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21aa']}).then(r=>r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,t:v.nodes.slice(0,2).map(n=>n.target.join(' '))})))")
    serious = [v for v in res if v['impact'] in ('serious', 'critical')]
    assert not serious, serious

def test_reduced_motion_and_focus(browser):
    ctx = browser.new_context(reduced_motion='reduce', viewport={'width': 1440, 'height': 900}); pg = ctx.new_page()
    c = next(x for x in LIVE if x['format'] == 'estimate'); pg.goto(URL + '?play=' + c['id'])
    answer(pg, c); pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
    assert pg.evaluate("document.activeElement.id") == 'r-h'  # focus moves to the reveal heading
    d = pg.evaluate("getComputedStyle(document.querySelector('.ev-mark')||document.body).transitionDuration")
    assert d in ('0s', '1e-05s') or float(d.rstrip('s')) <= 0.001
    ctx.close()

def test_live_classroom_three_phones(browser, tmp_path):
    from server import app, classroom as cl
    app.STORE = cl.Store(tmp_path / 'b.sqlite3')
    srv = app.Server(('127.0.0.1', 0), app.Handler); threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{srv.server_address[1]}'
    try:
        inst = page(browser); inst.goto(base + '/classroom'); inst.fill('#title', 'Test class'); inst.click('text=Create the session')
        code = inst.text_content('.join-code').strip()
        inst.add_script_tag(path=str(AXE))
        res = inst.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21aa']}).then(r=>r.violations.filter(v=>v.impact==='serious'||v.impact==='critical').map(v=>v.id))")
        assert not res, res
        phones = []
        for i in range(3):
            ctx = browser.new_context(viewport={'width': 390, 'height': 844}); ph = ctx.new_page(); ph.goto(base + '/?room=' + code); phones.append(ph)
        phones[0].wait_for_selector('.room-wait')
        c = next(x for x in cl.CHALLENGES.values() if x['format'] == 'choice')
        inst.click(f'[data-open="{c["id"]}"]')
        for ph in phones:
            ph.wait_for_selector('.opt', timeout=10000); ph.locator('.opt').first.click()
            ph.eval_on_selector('#conf', "e=>{e.value=70;e.dispatchEvent(new Event('input',{bubbles:true}))}"); ph.click('#lock-btn')
        phones[0].wait_for_selector('text=Your answer is in', timeout=10000)
        for _ in range(40):
            if (inst.text_content('#resp-count') or '').strip() == '3': break
            inst.wait_for_timeout(250)
        assert inst.text_content('#resp-count').strip() == '3'
        inst.click("text=Reveal to the room"); inst.wait_for_selector(".rv"); assert "Cannot" not in (inst.text_content("#toast") or "") and not inst.errors, inst.errors
        phones[1].wait_for_selector('#class-h', timeout=10000)
        assert '3 answers' in phones[1].text_content('#class-h')
        assert not inst.errors and not any(ph.errors for ph in phones if hasattr(ph, 'errors'))
    finally:
        srv.shutdown()

def test_lock_requires_confidence_and_touch(browser):
    pg = page(browser); c = next(x for x in LIVE if x['format'] == 'choice'); pg.goto(URL + '?play=' + c['id'])
    pg.keyboard.press('1'); assert not pg.is_enabled('#lock-btn')
    pg.eval_on_selector('#conf', "e=>{e.value=80;e.dispatchEvent(new Event('input',{bubbles:true}))}"); assert pg.is_enabled('#lock-btn')
    r = next(x for x in LIVE if x['format'] == 'rank'); pg.goto(URL + '?play=' + r['id'])
    pg.eval_on_selector('#conf', "e=>{e.value=80;e.dispatchEvent(new Event('input',{bubbles:true}))}"); assert not pg.is_enabled('#lock-btn')
    pg.click('[data-rank="0"][data-dir="1"]'); assert pg.is_enabled('#lock-btn')

def test_causal_diagram_hides_answer_until_reveal(browser):
    pg = page(browser); pg.goto(URL + '?play=axb05')
    assert 'Spending' not in pg.text_content('.dag')
    assert pg.locator('.dag [marker-end]').count() == 0          # review 5, M7: no arrow directions before the reveal
    answer(pg, next(x for x in LIVE if x['id'] == 'axb05')); pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
    assert 'Spending' in pg.text_content('.dag')
    assert pg.locator('.dag [marker-end]').count() > 0

def test_served_solo_round_fetches_evidence_after_lock(browser, tmp_path):
    """On the hosted page the bank has no answers; locking fetches the evidence and the reveal still works for every format."""
    from server import app, classroom as cl
    app.STORE = cl.Store(tmp_path / 's.sqlite3')
    srv = app.Server(('127.0.0.1', 0), app.Handler); threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{srv.server_address[1]}'
    try:
        for c in one_of_each():
            pg = page(browser); pg.goto(base + '/?play=' + c['id'])
            assert pg.evaluate('typeof window.THV') == 'undefined'          # no test hook on the hosted page
            assert '"answerTitle"' not in pg.content().split('const BANK =')[1].split('</script>')[0]
            answer(pg, c); pg.click('#lock-btn'); pg.wait_for_selector('#r-h', timeout=10000)
            assert pg.text_content('#r-h').strip() == c['answerTitle'], c['id']
            assert not pg.errors, (c['id'], pg.errors); pg.close()
        # Source takeaways and principles arrive with the evidence, not in the page.
        pg = page(browser); pg.goto(base + '/?play=ai01'); answer(pg, BY['ai01']); pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
        assert pg.evaluate("BANK.sources.noy23.takeaway") == cl.BANK['sources']['noy23']['takeaway']
        pg.goto(base + '/#library'); pg.wait_for_timeout(800)
        assert cl.BANK['themes'][0]['principle'][:40] in pg.content(); assert not pg.errors, pg.errors; pg.close()
    finally:
        srv.shutdown()

def test_back_button_moves_between_views(browser):
    pg = page(browser); pg.goto(URL)
    pg.click('.nav [data-nav="almanac"]'); pg.wait_for_selector('[id^=theme-]')
    pg.click('.nav [data-nav="record"]'); pg.wait_for_timeout(100)
    assert pg.evaluate('location.hash') == '#record'
    pg.go_back(); pg.wait_for_selector('[id^=theme-]'); assert pg.evaluate('location.hash') == '#library'
    pg.goto(URL + '#record'); assert pg.locator('.nav [aria-current="page"]').get_attribute('data-nav') == 'record'
    assert not pg.errors, pg.errors; pg.close()

def test_allocate_rebalances_and_needs_a_real_change(browser):
    """Review 5, M5: raising one option takes points from the others; a no-op does not unlock."""
    c = next(x for x in LIVE if x['format'] == 'allocate'); pg = page(browser); pg.goto(URL + '?play=' + c['id'])
    pg.eval_on_selector('[data-alloc="0"]', "e=>{e.value=+e.value;e.dispatchEvent(new Event('input',{bubbles:true}))}")
    assert not pg.is_enabled('#lock-btn')
    pg.eval_on_selector('[data-alloc="0"]', "e=>{e.value=80;e.dispatchEvent(new Event('input',{bubbles:true}))}")
    vals = [v for _, v in sorted(pg.eval_on_selector_all('[data-alloc]', 'els => els.map(e => [+e.dataset.alloc, +e.value])'))]   # displayed in shuffled order
    assert vals[0] == 80 and sum(vals) == c['allocate']['total'] and pg.is_enabled('#lock-btn'), vals
    assert not pg.errors, pg.errors; pg.close()


def test_offline_tutor_matches_server_rules(browser):
    """Review 14, M1: the page's offline tutor follows the same table as the server: generic questions and own follow-ups answer from the decision on screen."""
    pg = page(browser); pg.goto(URL); pg.wait_for_timeout(300)
    from tests.test_tutor import GENERIC_QS
    bad = pg.evaluate("""qs => { const out = []; for (const c of THV.ALL) { const cite0 = THV.curated('x', c) && null;
        for (const q of qs) { const r = THV.curated(q, c); if (!r.cites.length || !r.text || /outside what this lab/.test(r.text)) out.push([c.id, q]) }
        for (const f of c.follow) if (THV.curated(f.q, c).text !== f.a) out.push([c.id, f.q]) } return out }""", GENERIC_QS)
    assert not bad, (len(bad), bad[:10])
    import json as _j
    phr = _j.loads((Path(__file__).parent / 'tutor_phrasings.json').read_text())
    bad2 = pg.evaluate("""qs => { const out = []; for (const c of THV.ALL) for (const q of qs) { const r = THV.curated(q, c); if (/outside what this lab/.test(r.text) || !r.cites.length) out.push([c.id, q]) } return out }""", phr)
    assert not bad2, (len(bad2), bad2[:10])   # review 15, M1: natural phrasings stay on the decision
    r = pg.evaluate("THV.curated('What is the capital of France?', THV.ALL[0]).text"); assert 'outside' in r
    from tests.test_tutor import REVIEW20, REVIEW21, REVIEW22, REVIEW23, REVIEW24, REVIEW25
    from server import tutor as _T
    for q, cid, _ in REVIEW20 + REVIEW21 + REVIEW22 + REVIEW23 + REVIEW24 + REVIEW25 + [('Should I believe a lab game?', 'ai01', 0), ('Does the norm nudge work?', 'social16', 0)]:   # review 20: page and server agree
        pt = pg.evaluate("([q, id]) => THV.curated(q, THV.ALL.find(c => c.id === id)).text", [q, cid])
        assert pt.replace('\n\n', ' ').split()[:12] == _T.curated(q, cid)['answer'].split()[:12], (q, pt[:80])
    assert not pg.errors, pg.errors; pg.close()


def test_served_confidence_prompts_read_cleanly(browser, tmp_path):
    """Review 16, M1: with the public bank (no answers), every format's confidence prompt is complete."""
    import subprocess, sys, socket, time, os
    s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
    env = dict(os.environ, PORT=str(port), THV_DATA_DIR=str(tmp_path))
    proc = subprocess.Popen([sys.executable, 'start_classroom.py'], cwd=str(Path(__file__).resolve().parents[1]), env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.5); pg = page(browser); bad = []
        for fmt in ('choice', 'causal', 'multi', 'estimate', 'rank', 'delegate'):
            c = next(x for x in LIVE if x['format'] == fmt)
            pg.goto(f'http://127.0.0.1:{port}/?play={c["id"]}'); pg.wait_for_timeout(400)
            txt = pg.inner_text('#view')
            if re.search(r'\b(undefined|null|NaN)\b', txt): bad.append((c['id'], fmt))
        assert not bad, bad; pg.close()
    finally: proc.kill()


@pytest.mark.parametrize('width', [1440, 390])
def test_axe_every_format_reveal(browser, width):
    """Review 21, minor 1: every format's reveal passes axe at both widths (the rank reveal failed contrast at 390)."""
    bad = []
    for f in ('choice', 'causal', 'multi', 'estimate', 'forecast', 'rank', 'allocate', 'delegate'):
        c = next(x for x in LIVE if x['format'] == f)
        pg = browser.new_page(viewport={'width': width, 'height': 900}); pg.goto(URL + '?play=' + c['id']); pg.wait_for_timeout(150)
        answer(pg, c); pg.click('#lock-btn'); pg.wait_for_selector('#r-h'); pg.wait_for_timeout(900)
        pg.add_script_tag(path=str(AXE))
        res = pg.evaluate("axe.run(document,{runOnly:['wcag2a','wcag2aa','wcag21aa']}).then(r=>r.violations.filter(v=>['serious','critical'].includes(v.impact)).map(v=>v.id+': '+v.nodes.slice(0,2).map(n=>n.target.join(' ')).join(', ')))")
        bad += [(f, v) for v in res]; pg.close()
    assert not bad, bad


def test_served_views_survive_a_reload_after_every_format(browser, tmp_path):
    """Invariant I13 (review 24, B1): on the hosted page the bank has no answers, so every view must render from stored records
    after a reload, for records of every format, including records saved by older versions."""
    from server import app, classroom as cl
    app.STORE = cl.Store(tmp_path / 'r.sqlite3'); app.LIMIT = app.Limiter()
    srv = app.Server(('127.0.0.1', 0), app.Handler); threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{srv.server_address[1]}'
    try:
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900}); pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        for c in one_of_each():
            pg.goto(base + '/?play=' + c['id']); answer(pg, c); pg.click('#lock-btn'); pg.wait_for_selector('#r-h', timeout=10000)
        # a record from before topBest existed
        pg.evaluate("""() => { const k = 'thv:v2:records', r = JSON.parse(localStorage.getItem(k) || '[]'); const a = r.find(x => x.format === 'allocate'); if (a) { const o = Object.assign({}, a); delete o.topBest; r.push(o) } localStorage.setItem(k, JSON.stringify(r)) }""")
        for view in ('/#record', '/#library', '/#studies', '/'):
            pg.goto(base + view); pg.reload(); pg.wait_for_timeout(700)
            assert len(pg.inner_text('main').strip()) > 200, view
        assert not errs, errs
        ctx.close()
    finally:
        srv.shutdown()


def test_record_is_identical_offline_and_hosted(browser, tmp_path):
    """Invariant I13, generalised after review 25 (M1): records made on the hosted page read the same there after a reload as on the
    offline file, which has every answer; checked for one decision of every format and for blind constant routing on every delegate item."""
    from server import app, classroom as cl
    app.STORE = cl.Store(tmp_path / 'p.sqlite3'); app.LIMIT = app.Limiter()
    srv = app.Server(('127.0.0.1', 0), app.Handler); threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{srv.server_address[1]}'
    def hosted(plays):
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900}); pg = ctx.new_page()
        for c, act in plays:
            pg.goto(base + '/?play=' + c['id']); pg.wait_for_timeout(150); act(pg, c)
            pg.click('#lock-btn'); pg.wait_for_selector('#r-h', timeout=10000)
        pg.goto(base + '/#record'); pg.reload(); pg.wait_for_timeout(600)
        txt, recs = pg.inner_text('.score-strip'), pg.evaluate("localStorage.getItem('thv:v2:records')"); ctx.close(); return txt, recs
    def offline(recs):
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900}); pg = ctx.new_page(); pg.goto(URL)
        pg.evaluate("r => localStorage.setItem('thv:v2:records', r)", recs); pg.goto(URL + '#record'); pg.reload(); pg.wait_for_timeout(600)
        txt = pg.inner_text('.score-strip'); ctx.close(); return txt
    def route0(pg, c):
        for k in range(len(c['delegate']['tasks'])): pg.click(f'[data-deleg="{k}"][data-pick="0"]')
        if pg.locator('#conf').count(): pg.eval_on_selector('#conf', "e=>{e.value=70;e.dispatchEvent(new Event('input',{bubbles:true}))}")
    try:
        for plays in ([(c, answer) for c in one_of_each()], [(c, route0) for c in LIVE if c['format'] == 'delegate']):
            txt, recs = hosted(plays)
            assert txt == offline(recs), (txt, offline(recs))
    finally:
        srv.shutdown()


def test_page_tutor_agrees_with_server_on_every_probe(browser):
    """Invariant I9 at audit scale: the page's offline tutor gives the server's answer on every audit probe and lead-in question."""
    import json as _j
    from server import tutor as _T
    W = _j.loads((Path(__file__).parent / 'tutor_wide_questions.json').read_text())
    pairs = [tuple(x) for x in W['probes']] + [(p + q, cid) for cid in ('ai01', 'axb08', 'bz07', 'civic-wallet-rank', 'judg09', 'bz08') for p in W['lead_ins']['prefixes'] for q in W['lead_ins']['questions']]
    pairs = [(q, cid) for q, cid in pairs if cid in _T.CHALLENGES and not _T.CHALLENGES[cid].get('retired')]
    pg = page(browser); pg.goto(URL); pg.wait_for_timeout(300)
    page_ans = pg.evaluate("ps => ps.map(([q, id]) => THV.curated(q, THV.ALL.find(c => c.id === id)).text)", pairs)
    pairs += [(q, c['id']) for c in _T.CHALLENGES.values() if not c.get('retired') for q in W['every_decision']]   # review 26: every decision, full text
    page_ans = page_ans + pg.evaluate("ps => ps.map(([q, id]) => THV.curated(q, THV.ALL.find(c => c.id === id)).text)", pairs[len(page_ans):])
    bad = [(q, cid, a[:60], _T.curated(q, cid)['answer'][:60]) for (q, cid), a in zip(pairs, page_ans) if a.split() != _T.curated(q, cid)['answer'].split()]
    sug = pg.evaluate("ps => ps.map(([q, id]) => THV.curated(q, THV.ALL.find(c => c.id === id)).suggest || null)", pairs[:400])   # audit 34: the suggestion buttons, in the same order
    bad += [(q, cid, 'suggest', s) for (q, cid), s in zip(pairs[:400], sug) if s != _T.curated(q, cid).get('suggest')]
    assert not bad, (len(bad), bad[:8]); pg.close()


def test_estimate_study_line_shows_no_number_in_band(browser):
    """Audit 37: the rendered study line (sample included) never prints a number inside an estimate's scoring band (invariant I4)."""
    import re
    pg = page(browser); bad = []
    for c in [x for x in LIVE if x['format'] == 'estimate']:
        pg.goto(URL + '?play=' + c['id']); txt = pg.inner_text('.study-line').replace(',', '')
        bad += [(c['id'], m) for m in re.findall(r'-?\d+(?:\.\d+)?', txt) if abs(float(m) - c['estimate']['target']) <= c['estimate']['tolerance']]
    assert not bad, bad


def test_allocate_effect_labels_keep_their_grid_place(browser):
    """Audit 40: a non-significant label lost its grid class and fell onto its own row at full number size."""
    for c in [x for x in LIVE if x['format'] == 'allocate']:
        pg = page(browser); pg.goto(URL + '?play=' + c['id']); answer(pg, c); pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
        sizes = pg.eval_on_selector_all('.alloc-cmp b.num.ev', 'e => e.map(x => getComputedStyle(x).fontSize)')
        assert sizes and len(set(sizes)) == 1, (c['id'], sizes)
        assert pg.locator('.alloc-cmp b.num:not(.ev):not(.you)').count() == 0, c['id']


def test_outlined_rank_badges_are_readable_on_the_plate(browser):
    """Audit 45: the outlined study places used the dark evidence ink on the dark plate (2.4:1); axe files them as incomplete, so check the colour."""
    c = next(x for x in LIVE if x['id'] == 'forecast-teams-rank')
    pg = page(browser); pg.goto(URL + '?play=' + c['id']); answer(pg, c); pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
    cols = pg.eval_on_selector_all('.plate .rc-badge.evn', 'e => e.map(x => getComputedStyle(x).color)')
    assert cols and set(cols) == {'rgb(240, 180, 60)'}, cols


def test_balance_follows_resize(browser):
    """Audit 45: the wide-reveal balance is a class recomputed on resize, so a phone never shows the moved study card."""
    c = next(x for x in LIVE if x['id'] == 'axb01')
    ctx = browser.new_context(viewport={'width': 1440, 'height': 900}); pg = ctx.new_page(); pg.goto(URL + '?play=' + c['id']); answer(pg, c); pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
    pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(400)
    assert not pg.evaluate("document.querySelector('.reveal').classList.contains('meta-right')")
    assert pg.evaluate("getComputedStyle(document.querySelector('.reveal>.rev-meta .study-card')).display") == 'none'
    ctx.close()


def test_moved_study_card_sits_under_the_figure(browser):
    """Audit 47: the balanced card landed in a grid row below the left column, so it moved sideways only; it must sit right under the figure."""
    pg = page(browser); out = []
    for c in LIVE:
        pg.goto(URL + '?play=' + c['id']); answer(pg, c); pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
        r = pg.evaluate("(()=>{const rv=document.querySelector('.reveal');if(!rv.classList.contains('meta-right'))return null;return document.querySelector('.reveal>.rev-meta').getBoundingClientRect().top-document.querySelector('.reveal>figure.gap').getBoundingClientRect().bottom})()")
        if r is not None: out.append((c['id'], r))
    assert out and all(0 <= r <= 40 for _, r in out), [x for x in out if not 0 <= x[1] <= 40]

def test_stranded_room_answer_can_be_sent_again(browser, tmp_path):
    """Review 35, M1: an answer that fails for the whole retry window keeps a resend button and goes through once the network returns."""
    from server import app, classroom as cl
    app.STORE = cl.Store(tmp_path / 'r.sqlite3')
    srv = app.Server(('127.0.0.1', 0), app.Handler); threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{srv.server_address[1]}'
    try:
        inst = page(browser); inst.goto(base + '/classroom'); inst.fill('#title', 'Resend class'); inst.click('text=Create the session')
        code = inst.text_content('.join-code').strip()
        ctx = browser.new_context(viewport={'width': 390, 'height': 844}); ph = ctx.new_page(); ph.goto(base + '/?room=' + code)
        ph.wait_for_selector('.room-wait')
        c = next(x for x in cl.CHALLENGES.values() if x['format'] == 'choice')
        inst.click(f'[data-open="{c["id"]}"]')
        ph.wait_for_selector('.opt', timeout=10000)
        ph.route('**/responses', lambda r: r.abort())
        ph.locator('.opt').first.click()
        ph.eval_on_selector('#conf', "e=>{e.value=70;e.dispatchEvent(new Event('input',{bubbles:true}))}"); ph.click('#lock-btn')
        ph.wait_for_selector('[data-act="resend"]', timeout=40000)
        assert 'Not sent yet' in ph.text_content('.room-wait h1') and 'did not reach the class' in ph.text_content('.room-wait')
        ph.unroute('**/responses')
        ph.click('[data-act="resend"]')
        ph.wait_for_selector('text=Your answer is in', timeout=10000)
        assert ph.locator('[data-act="resend"]').count() == 0
        for _ in range(40):
            if (inst.text_content('#resp-count') or '').strip() == '1': break
            inst.wait_for_timeout(250)
        assert inst.text_content('#resp-count').strip() == '1'
        ctx.close()
    finally:
        srv.shutdown()
