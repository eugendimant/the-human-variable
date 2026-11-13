"""qa/DESIGN_RULES.md: no AI-made looks and Tufte's figure rules, checked in a real browser on every page state
(home, Library, All decisions, record, predict and reveal for all 8 formats at 1440 and 390 px; console, projector and a phone)."""
import sys
from pathlib import Path
import pytest
pytest.importorskip('playwright')
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))


def test_design_rules_hold_on_every_page():
    import design_lint
    hits, errors = design_lint.run()
    assert not errors, errors
    assert not hits, [' | '.join(h) for h in hits[:25]]


def test_design_detectors_fire_on_injected_tells():
    """Each detector is live: inject one tell per rule into a blank page and require a hit."""
    from playwright.sync_api import sync_playwright
    import design_lint
    html = """<html><body style="font:16px sans-serif">
      <div class="hero"><span>Label</span><h1 style="font-size:80px;width:500px;text-wrap:balance">Predict what people do. Then see the evidence of it all now, every single day of the week.</h1></div>
      <p style="text-transform:uppercase">all caps text</p>
      <div style="width:300px;height:60px;background:linear-gradient(red,blue)">g</div>
      <div style="backdrop-filter:blur(4px)">glass</div>
      <div style="box-shadow:0 0 20px rgba(120,60,255,.6)">glow</div>
      <div style="border-left:4px solid #2f54eb;height:40px">stripe</div>
      <div style="background:repeating-linear-gradient(45deg,#fff 0 4px,#000 4px 8px);height:20px">h</div>
      <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#e0a01c"></span>
      <p>Emoji 🚀 here</p><p>Meta · string</p><button>Next →</button><p>A pause — here</p><p>Unlock the power of AI</p><p>03</p>
      <p style="font-size:10px">tiny</p><p style="letter-spacing:-.08em">crushed</p>
      <p class="gap-caption">Blue marks your call, amber the evidence.</p><div class="gap-legend">legend</div><p class="plate-h">What the study measured</p>
      <figure class="gap"><div class="hbars"><i class="ev">a</i><i class="ev">b</i></div></figure>
      <div style="width:300px;height:60px;background-image:radial-gradient(circle,#000 1px,transparent 1px);background-size:18px 18px">dots</div>
      <p style="width:90px">This sentence is far too long to sit in a column this narrow without breaking apart.</p>
      <svg width="200" height="60" viewBox="0 0 200 60"><text x="10" y="30" font-size="14">first label</text><text x="20" y="32" font-size="14">second label</text></svg>
      <div><em>Start here</em><strong style="font-size:24px;font-weight:800;display:block">Leading with AI today</strong></div>
    </body></html>"""
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.set_content(html)
        rules = {r for r, *_ in pg.evaluate(design_lint.JS)}; b.close()
    want = {'R01', 'R03', 'R04', 'R05', 'R06', 'R07', 'R08', 'R09', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R19', 'R20', 'R26', 'R27', 'R28'}
    assert {'R08', 'R18', 'R31'} <= rules   # patterned backgrounds and squeezed text (review 22)
    assert want <= rules, sorted(want - rules)


def test_hyphen_minus_detector_reads_svg_and_display_numbers():
    """Review 26: a hyphen standing in for a minus inside an SVG plate or a display number is caught."""
    from playwright.sync_api import sync_playwright
    import design_lint
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.set_content('<svg width="200" height="60"><text x="10" y="30" font-size="14">Study -17%</text></svg><div class="gap-head"><b class="num">-50%</b></div>')
        hits = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R13']
        pg.set_content('<svg width="200" height="60"><text x="10" y="30" font-size="14">Study −17%</text></svg><p>2019-2020 and a well-known fact</p>')
        clean = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R13']; b.close()
    assert len(hits) >= 2 and not clean, (hits, clean)


def test_nested_tile_detector_sees_borderless_tinted_tiles():
    """Review 26: a filled, rounded box with no border inside a plate is a tile in a tile (rule 3)."""
    from playwright.sync_api import sync_playwright
    import design_lint
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.set_content('<div style="background:#14203a;border-radius:8px;padding:20px;width:600px"><div style="background:rgba(255,255,255,.07);border-radius:8px;width:400px;height:60px">task</div></div>')
        hit = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R21']
        pg.set_content('<div style="background:#14203a;border-radius:8px;padding:20px;width:600px"><div style="border-top:1px solid #333;width:400px;height:60px">task</div></div>')
        clean = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R21']; b.close()
    assert hit and not clean, (hit, clean)


def test_html_text_overlap_detector():
    """Review 26: HTML text drawn over other text is caught; text side by side is not."""
    from playwright.sync_api import sync_playwright
    import design_lint
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.set_content('<div style="position:relative;height:40px"><p style="position:absolute;top:0;margin:0">You: -54 skill points</p><p style="position:absolute;top:2px;left:4px;margin:0">AI at work strip</p></div>')
        hit = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R31']
        pg.set_content('<p>You: 54 skill points</p><p>AI at work strip</p>')
        clean = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R31']; b.close()
    assert hit and not clean, (hit, clean)


def test_clipped_svg_mark_detector():
    """Audit 31: a mark stacked past the top of its SVG is caught."""
    from playwright.sync_api import sync_playwright
    import design_lint
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.set_content('<svg viewBox="0 0 900 200" width="900" height="200"><circle cx="100" cy="-60" r="5"/></svg>')
        hit = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R31']
        pg.set_content('<svg viewBox="0 0 900 200" width="900" height="200"><circle cx="100" cy="60" r="5"/></svg>')
        clean = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R31']; b.close()
    assert hit and not clean, (hit, clean)


def test_label_wider_than_its_pill_is_caught():
    """Review 27: a node label that overflows its pill is caught; one that fits is not."""
    from playwright.sync_api import sync_playwright
    import design_lint
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.set_content('<svg viewBox="0 0 400 100" width="400" height="100"><g><rect x="130" y="20" width="140" height="48"/><text x="200" y="50" text-anchor="middle" font-size="21">Learned of a random notice today</text></g></svg>')
        hit = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R31']
        pg.set_content('<svg viewBox="0 0 400 100" width="400" height="100"><g><rect x="130" y="20" width="140" height="48"/><text x="200" y="50" text-anchor="middle" font-size="14">Pay gap</text></g></svg>')
        clean = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R31']; b.close()
    assert hit and not clean, (hit, clean)


def test_lint_states_use_real_routes():
    """Review 28: a lint state whose hash is not a real route silently lints the home page."""
    import re
    from pathlib import Path
    R = Path(__file__).resolve().parents[1]
    routes = set(re.findall(r"'(#\w+)'", re.search(r"const HASH = \{([^}]*)\}", (R / 'src/app.js').read_text()).group(1)))
    used = set(re.findall(r"URL \+ '(#\w+)'", (R / 'tools/design_lint.py').read_text()))
    assert used and used <= routes, used - routes


def test_two_beat_slogan_headline_is_caught():
    """Owner, 2026-11-01: "Do X. Then Y." headlines are an AI tell."""
    from playwright.sync_api import sync_playwright
    import design_lint
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.set_content('<h1>Predict what people do. Then see the evidence.</h1>')
        hit = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R14']
        pg.set_content('<h1>How much less time did they take?</h1>')
        clean = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R14']; b.close()
    assert hit and not clean


def test_plural_after_one_is_caught():
    """Audit 36: "You were 1 points off." shipped on the home page."""
    from playwright.sync_api import sync_playwright
    import design_lint
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.set_content('<p>You were 1 points off.</p>')
        hit = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R14']
        pg.set_content('<p>You were 1 point off. You were 11 points off. 2.1 points.</p>')
        clean = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R14']; b.close()
    assert hit and not clean


def test_squeezed_heading_is_caught():
    """Owner, 2026-11-01: a heading capped narrower than its column wraps early and leaves the space empty."""
    from playwright.sync_api import sync_playwright
    import design_lint
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.set_content('<div style="width:900px"><h1 style="max-width:12ch;font-size:40px">How did unrestricted AI students score on unaided exams?</h1></div>')
        hit = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R33']
        pg.set_content('<div style="width:900px"><h1 style="font-size:40px">How did unrestricted AI students score on unaided exams versus controls in the study?</h1></div>')
        clean = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R33']; b.close()
    assert hit and not clean, (hit, clean)


def test_clipped_text_is_caught():
    """Review 34: a label cut off by overflow:hidden ("(not signifi") passed every gate."""
    from playwright.sync_api import sync_playwright
    import design_lint
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.set_content('<b style="display:block;width:60px;overflow:hidden;white-space:nowrap">+21.9% (not significant)</b>')
        hit = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R31' and 'clipped' in h[2]]
        pg.set_content('<b style="display:block;width:300px;overflow:hidden;white-space:nowrap">+21.9% (not significant)</b>')
        clean = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R31' and 'clipped' in h[2]]; b.close()
    assert hit and not clean


def test_orphan_is_caught():
    """Owner, 2026-11-12: "orphans are a no-no". A word alone on the last line is flagged; the same text with its last two words tied is not."""
    from playwright.sync_api import sync_playwright
    import design_lint
    bad = '<p style="width:150px;font:16px sans-serif">alpha bravo charlie delta golftangofoxtrotwhiskeyyankee</p>'
    good = '<p style="width:150px;font:16px sans-serif">alpha bravo charlie <span class="nw" style="white-space:nowrap">delta golftangofoxtrotwhiskeyyankee</span></p>'
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.set_content(bad); hit = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R34']
        pg.set_content(good); clean = [h for h in pg.evaluate(design_lint.JS) if h[0] == 'R34']; b.close()
    assert hit and not clean, (hit, clean)


def test_pages_tie_the_last_two_words():
    """Owner, 2026-11-12: render() ties the last two words of every text block, so the landing page has no orphan at any width."""
    from playwright.sync_api import sync_playwright
    import design_lint
    from test_browser import URL
    with sync_playwright() as p:
        b = p.chromium.launch(); hits = []
        for w, h in ((390, 844), (820, 1100), (1280, 720), (1440, 900), (1920, 1080)):
            pg = b.new_page(viewport={'width': w, 'height': h}); pg.goto(URL); pg.wait_for_timeout(300)
            hits += [(w,) + tuple(x) for x in pg.evaluate(design_lint.JS) if x[0] == 'R34']; pg.close()
        b.close()
    assert not hits, hits


def test_landing_page_has_no_sideways_scroll():
    """Iteration 67: the Dimant paper list set its venue line to nowrap and pushed the landing page to 475 px at 390; no width may scroll sideways."""
    from playwright.sync_api import sync_playwright
    from test_browser import URL
    with sync_playwright() as p:
        b = p.chromium.launch(); wide = []
        for w in (320, 360, 390, 430, 600, 820, 1024, 1280, 1440, 1920):
            pg = b.new_page(viewport={'width': w, 'height': 844}); pg.goto(URL); pg.wait_for_timeout(200)
            sw = pg.evaluate('document.documentElement.scrollWidth')
            if sw > w: wide.append((w, sw))
            pg.close()
        b.close()
    assert not wide, wide


def test_front_page_sample_is_random_and_every_sample_works():
    """Owner, 2026-11-12: "different studies at random on the front page, not just the same". The sample changes on each visit, never repeats the last one, and every candidate locks and reveals."""
    from playwright.sync_api import sync_playwright
    from test_browser import URL
    with sync_playwright() as p:
        b = p.chromium.launch(); seen = set()
        for _ in range(14):
            ctx = b.new_context(); pg = ctx.new_page(); pg.goto(URL); seen.add(pg.text_content('#try-q')); ctx.close()
        assert len(seen) >= 4, seen
        ctx = b.new_context(); pg = ctx.new_page(); pg.goto(URL); prev = pg.text_content('#try-q')
        for _ in range(8):
            pg.reload(); cur = pg.text_content('#try-q'); assert cur != prev, 'the same sample twice in a row'; prev = cur
        ctx.close()
        pool = pg_ids = None
        pg = b.new_page(); pg.goto(URL)
        pool = pg.get_attribute('.try-ruler', 'data-pool').split(','); assert len(pool) >= 6, pool
        for cid in pool:
            errs = []; q = b.new_page(); q.on('pageerror', lambda e: errs.append(str(e))); q.goto(URL + '?hero=' + cid)
            q.evaluate("()=>{const r=document.querySelector('#hero-range');r.value=Math.round((+r.min+ +r.max)/2);r.dispatchEvent(new Event('input',{bubbles:true}))}"); q.click('[data-act=hero-lock]'); q.wait_for_selector('.try-result:not(:empty)')
            txt = q.text_content('.try-result'); assert txt.startswith('You were ') and ('points off' in txt or 'point off' in txt or 'exactly right' in txt), (cid, txt)
            assert not errs, (cid, errs); q.close()
        b.close()


def test_served_landing_page_names_the_owners_papers():
    """Review 42, M-1: the server strips source titles, so the served band showed 18 empty rows while the offline file looked fine."""
    import sys, tempfile, threading
    from pathlib import Path
    from playwright.sync_api import sync_playwright
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from server import app, classroom as cl
    app.STORE = cl.Store(Path(tempfile.mkdtemp()) / 'band.sqlite3'); app.LIMIT = app.Limiter()
    srv = app.Server(('127.0.0.1', 0), app.Handler); threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{srv.server_address[1]}'
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.goto(base + '/'); pg.wait_for_timeout(300)
            titles = pg.evaluate("[...document.querySelectorAll('.paper-list strong')].map(e => e.textContent.trim())")
            visible = pg.evaluate("[...document.querySelectorAll('.dimant > div:last-child > .paper-list li')].length"); b.close()
    finally: srv.shutdown()
    assert len(titles) >= 15 and all(len(t) > 12 for t in titles), titles
    assert visible == 3, visible   # three rows show; the rest sit under "Show all"


def test_resume_banner_sits_below_credit_and_can_be_closed():
    """Iteration 68: the credit line comes first, the Continue banner can be closed, the choice survives a reload, and the landing page has no numbered how-it-works box."""
    from playwright.sync_api import sync_playwright
    from test_browser import URL
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}); pg.goto(URL)
        ids = pg.evaluate("BANK.paths.find(x => x.id === 'leading-ai').ids.slice(0, 2)")
        recs = [{'id': i, 'format': 'choice', 'correct': True, 'score': 1, 'confidence': .7, 'at': 1, 'seed': 1} for i in ids]
        pg.evaluate("r => localStorage.setItem('thv:v2:records', JSON.stringify(r))", recs); pg.reload()
        assert pg.locator('.resume').count() == 1
        assert pg.evaluate("document.querySelector('.credit').compareDocumentPosition(document.querySelector('.resume')) & 4")
        assert pg.locator('.round-steps, .how-box').count() == 0
        pg.click('.resume-x'); assert pg.locator('.resume').count() == 0
        pg.reload(); assert pg.locator('.resume').count() == 0
        b.close()


def test_tie_leaves_flex_rows_and_path_lines_alone():
    """Review 43, M-1 and m-1: tieEnds pushed the last two words of every accordion question (a flex row) 17 to 320 px away, and the path index line took the serif of the blurb. A tied pair never sits in a summary, and a path's count line keeps one typeface."""
    from playwright.sync_api import sync_playwright
    from test_browser import URL
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}); pg.goto(URL); pg.wait_for_timeout(200)
        fonts = pg.evaluate("[...document.querySelectorAll('.path small, .path small .nw')].map(e => getComputedStyle(e).fontFamily + '|' + getComputedStyle(e).fontSize)")
        assert len(set(fonts)) == 1, fonts
        assert pg.evaluate("[...document.querySelectorAll('summary')].filter(e => /flex|grid/.test(getComputedStyle(e).display) && e.querySelector(':scope > .nw')).length") == 0   # a flex row's text is an anonymous item: a nowrap span there is pushed away from the rest
        assert 'flex|grid' in open(str(__import__('pathlib').Path(__file__).resolve().parents[1] / 'src' / 'tie.js'), encoding='utf-8').read()
        b.close()


def test_front_page_sample_has_no_try_again():
    """Iteration 69: after the reveal, "Try again" gave the same question with the answer known. Only "Play five more" is left."""
    from playwright.sync_api import sync_playwright
    from test_browser import URL
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 800}); pg.goto(URL); pg.wait_for_timeout(200)
        pg.evaluate("const r = document.querySelector('#hero-range'); r.value = 40; r.dispatchEvent(new Event('input', {bubbles: true}))")
        pg.click('[data-act=hero-lock]'); pg.wait_for_timeout(200)
        assert pg.locator('[data-act=start-quick]').count() == 1 and pg.locator('[data-act=hero-reset]').count() == 0
        assert 'Try again' not in pg.locator('.try-wrap').inner_text()
        b.close()

def test_served_tutor_text_gets_paragraphs_and_duration_chip_is_gated():
    """Review 46, m-2 and m-3: labelled parts of a served answer start new paragraphs; the duration chip needs a follow-up about duration."""
    js = (Path(__file__).resolve().parents[1] / "src/app.js").read_text()
    assert 'function tutorParas' in js and 'esc(tutorParas(t.text))' in js
    assert 'durationOk(c)' in js.split('function tutorChips')[1].split('function srcHtml')[0] and 'did the effect (last|fade|persist)' in js
