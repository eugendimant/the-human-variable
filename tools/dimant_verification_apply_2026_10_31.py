"""Dimant papers: every number verified against the paper text (docs/audit/dimant_verification_2026_10_31.json).
Verified sentences replace locations that named no document; three contagion figures are cross-checked in the author's
pre-publication version, where they are identical. Wording fixes from the same check. Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']
ev = json.loads((ROOT / 'src/evidence.json').read_text())
ver = json.loads((ROOT / 'docs/audit/dimant_verification_2026_10_31.json').read_text())
added = 0
for cid, rows in ver.items():
    if cid not in C: continue
    dsrc = next((s for s in C[cid]['sources'] if 'Dimant' in (S[s].get('authors_full') or S[s].get('authors', ''))), C[cid]['sources'][0])
    for r in rows:
        if r.get('status') not in ('verified_published', 'verified_preprint') or not r.get('quote'): continue
        loc = re.sub(r'(?i)cesifo working paper|working paper', "author's pre-publication version", r.get('version', ''))[:300]
        if r['status'] == 'verified_preprint': loc = "Author's pre-publication version of the same article (numbers identical to the published paper): " + loc
        if not any(x.get('quote') == r['quote'] for x in ev.setdefault(cid, [])):
            ev[cid].append({'source': dsrc, 'quote': r['quote'], 'location': loc}); added += 1
# wording fixes found by the check
S['opioid26']['authors_full'] = 'Mattie Toma, Russell Burnett, Pompa Debroy, Eugen Dimant, Jean Liu, Elana Safran, Uzaib Saya, Bill Schultz'
c = C['dimant-motivated-estimate']; c['study']['n'] = 'US MTurk participants in two experiments (1,945 and 2,414)'
for k in ('boundary', 'explain'):
    c[k] = c[k].replace('1,945 participants who chose their sources', '1,945 participants in the source-choice study')
for f in C['dimant-proximity-estimate']['follow']:
    if f['q'] == 'Were the groups different at the start?':
        f['a'] = 'No. Initial takers were 45%, 44% and 42% across conditions, so the gap emerged from watching peers.'
C['dimant-observability-choice']['boundary'] = 'Give-or-take charity games in the lab and online (1,650 decision makers online), where a decision maker chose with or without a passive observer watching.'
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('quotes added', added)
