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
    </body></html>"""
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900}); pg.set_content(html)
        rules = {r for r, *_ in pg.evaluate(design_lint.JS)}; b.close()
    want = {'R01', 'R03', 'R04', 'R05', 'R06', 'R07', 'R08', 'R09', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', 'R17', 'R19', 'R20', 'R26', 'R27', 'R28'}
    assert want <= rules, sorted(want - rules)
