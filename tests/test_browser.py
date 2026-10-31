"""Real-browser checks: every format plays and reveals, keyboard play, no overflow at phone width, axe accessibility,
and a live-classroom round with three phones. Skipped when Playwright or Chromium is unavailable."""
import json, threading
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
        pg.eval_on_selector('[data-alloc="0"]', "e=>{e.value=+e.value;e.dispatchEvent(new Event('input',{bubbles:true}))}")
    if f != 'forecast':
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
    pg.wait_for_selector('text=Round complete.')
    assert pg.locator('.score-big').count() == 1 and pg.locator('.score-meta div').count() == 3 and not pg.errors

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
        inst.click('text=Reveal to the room'); inst.wait_for_selector('.rv')
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
    answer(pg, next(x for x in LIVE if x['id'] == 'axb05')); pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
    assert 'Spending' in pg.text_content('.dag')

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
    pg.click('.nav [data-nav="almanac"]'); pg.wait_for_selector('.theme')
    pg.click('.nav [data-nav="record"]'); pg.wait_for_timeout(100)
    assert pg.evaluate('location.hash') == '#record'
    pg.go_back(); pg.wait_for_selector('.theme'); assert pg.evaluate('location.hash') == '#library'
    pg.goto(URL + '#record'); assert pg.locator('.nav [aria-current="page"]').get_attribute('data-nav') == 'record'
    assert not pg.errors, pg.errors; pg.close()
