"""Assemble the single-file offline game (index.html) from src/.
Run: python src/build.py        Check only: python src/build.py --check"""
import base64, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'

def b64(name): return base64.b64encode((SRC / 'fonts' / name).read_bytes()).decode()

def build():
    bank = json.loads((SRC / 'bank.json').read_text(encoding='utf-8'))
    css = (SRC / 'app.css').read_text(encoding='utf-8')
    css = (css.replace('/*@FONT_SANS@*/', b64('schibsted-grotesk-latin-wght-normal.woff2'))
              .replace('/*@FONT_SERIF@*/', b64('newsreader-latin-wght-normal.woff2'))
              .replace('/*@FONT_SERIF_I@*/', b64('newsreader-latin-wght-italic.woff2')))
    data = json.dumps(bank, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    html = (SRC / 'shell.html').read_text(encoding='utf-8')
    parts = {'/*@CSS@*/': css, '/*@BANK@*/': data,
             '/*@SCORING@*/': (SRC / 'scoring.js').read_text(encoding='utf-8'),
             '/*@JS@*/': (SRC / 'app.js').read_text(encoding='utf-8')}
    for k, v in parts.items():
        assert html.count(k) == 1, k
        html = html.replace(k, v.replace('\\', '\\\\') if False else v)
    return html

if __name__ == '__main__':
    out = build()
    target = ROOT / 'index.html'
    if '--check' in sys.argv:
        ok = target.exists() and target.read_text(encoding='utf-8') == out
        print('index.html is current' if ok else 'index.html is STALE: run python src/build.py'); sys.exit(0 if ok else 1)
    target.write_text(out, encoding='utf-8'); print(f'Built {target} ({len(out)//1024} KB)')
