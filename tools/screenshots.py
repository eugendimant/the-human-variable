"""Capture the reference screenshots in docs/screenshots/ (desktop 1440x900 and phone 390x844)."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]; OUT = ROOT / 'docs/screenshots'; OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'tests')); from test_browser import answer, BANK  # same answering helper as the tests
URL = (ROOT / 'index.html').as_uri(); C = {c['id']: c for c in BANK['challenges']}

def shoot(b, name, w, h, url, act=None, full=False):
    pg = b.new_page(viewport={'width': w, 'height': h}); pg.goto(url); pg.wait_for_timeout(300)
    if act: act(pg)
    pg.wait_for_timeout(900); pg.screenshot(path=str(OUT / f'{name}.png'), full_page=full); pg.close()

def play(cid, lock=True):
    def go(pg):
        answer(pg, C[cid])
        if lock: pg.click('#lock-btn'); pg.wait_for_selector('#r-h')
    return go

with sync_playwright() as p:
    b = p.chromium.launch()
    for tag, w, h in (('desktop', 1440, 900), ('phone', 390, 844)):
        shoot(b, f'{tag}-home', w, h, URL)
        shoot(b, f'{tag}-predict-causal', w, h, URL + '?play=dimant-notalie-causal', play('dimant-notalie-causal', False))
        shoot(b, f'{tag}-reveal-estimate', w, h, URL + '?play=bz07', play('bz07'))
        shoot(b, f'{tag}-reveal-allocate', w, h, URL + '?play=' + next(c['id'] for c in BANK['challenges'] if c['format'] == 'allocate'),
              play(next(c['id'] for c in BANK['challenges'] if c['format'] == 'allocate')))
        shoot(b, f'{tag}-predict-delegate', w, h, URL + '?play=rollout3', play('rollout3', False))
        shoot(b, f'{tag}-library', w, h, URL + '#library')
        def seeded(pg):   # a record with a few calls, played in the same page so storage persists
            for cid in ('bz07', 'rollout3', 'dimant-notalie-causal', 'dimant-enforcers-rank'):
                pg.goto(URL + '?play=' + cid); pg.wait_for_timeout(250); play(cid)(pg)
            pg.goto(URL + '#record')
        shoot(b, f'{tag}-record', w, h, URL, seeded)
        shoot(b, f'{tag}-record-empty', w, h, URL + '#record')
    b.close()
print('wrote', len(list(OUT.glob('*.png'))), 'screenshots to', OUT)
