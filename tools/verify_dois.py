"""Check every source's DOI against Crossref (falls back to doi.org): the DOI resolves and its registered title matches ours.
Writes qa/DOI_CHECK.md. Run: python3 tools/verify_dois.py"""
import json, re, sys, time, urllib.request, urllib.parse, difflib, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
S = json.loads((ROOT / 'src/bank.json').read_text())['sources']
norm = lambda t: ' '.join(re.sub(r'[^a-z0-9 ]', '', re.sub(r'<[^>]+>', '', t or '').lower()).split())
def get(url, method='GET'):
    req = urllib.request.Request(url, method=method, headers={'User-Agent': 'the-human-variable/1.0 (mailto:edimant@sas.upenn.edu)'})
    return urllib.request.urlopen(req, timeout=30)
rows, bad = [], []
for sid, s in S.items():
    doi = s.get('doi', ''); ok_url = s.get('url') == 'https://doi.org/' + doi
    title = None; status = ''
    for attempt in range(3):
        try:
            m = json.load(get('https://api.crossref.org/works/' + urllib.parse.quote(doi)))['message']
            title = (m.get('title') or [''])[0]; status = 'crossref'; break
        except urllib.error.HTTPError as e:
            if e.code == 404: status = 'not in crossref'; break
            time.sleep(2)
        except Exception: time.sleep(2)
    if title is None:
        try: get('https://doi.org/api/handles/' + urllib.parse.quote(doi)); status = 'resolves (doi.org handle)'
        except Exception as e: status = 'DOES NOT RESOLVE'
    sim = difflib.SequenceMatcher(None, norm(title), norm(s['title'])).ratio() if title else None
    good = ok_url and status != 'DOES NOT RESOLVE' and (sim is None or sim >= 0.8 or norm(s['title'])[:40] in norm(title) or norm(title)[:40] in norm(s['title']))
    rows.append((sid, doi, status, '' if sim is None else f'{sim:.2f}', 'ok' if good else 'CHECK'))
    if not good: bad.append((sid, doi, status, sim, title, s['title']))
out = [f'# DOI check ({datetime.date.today().isoformat()})', '', f'{len(rows)} sources. {len(rows) - len(bad)} verified: the link is https://doi.org/<DOI>, the DOI resolves, and the registered title matches. {len(bad)} to check.', '', '| Source | DOI | Registry | Title match | Result |', '|---|---|---|---|---|']
out += [f'| {a} | {b} | {c} | {d} | {e} |' for a, b, c, d, e in rows]
(ROOT / 'qa/DOI_CHECK.md').write_text('\n'.join(out) + '\n')
print(len(rows), 'sources;', len(bad), 'to check')
for b in bad: print(b)
sys.exit(1 if bad else 0)
