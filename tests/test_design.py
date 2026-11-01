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
      <div class="hero"><span>Label</span><h1 style="font-size:80px;width:500px">Predict what people do. Then see the evidence of it all now, every single day of the week.</h1></div>
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
