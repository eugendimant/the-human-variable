"""Review 4, M7: explanations state the key number from the version of record (draft and quotes:
docs/audit/explain_rewrites_2026_10_31.json). Also applies the drafting agent's evidence findings. Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']
ev = json.loads((ROOT / 'src/evidence.json').read_text())
d = json.loads((ROOT / 'docs/audit/explain_rewrites_2026_10_31.json').read_text())
d['social20']['explain'] = re.sub(r'\s*Ready-made Qualtrics software comes with it\.', '', d['social20']['explain'])
REPLACE_EVIDENCE = {'social12', 'social13', 'social15', 'social16', 'ai02', 'biz02', 'biz04'}
for cid, v in d.items():
    if cid not in C: continue
    C[cid]['explain'] = v['explain']
    q = [{'source': x.get('source', C[cid]['sources'][0]), 'quote': x['quote'], 'location': x['location']} for x in v.get('quotes', [])]
    ev[cid] = q if cid in REPLACE_EVIDENCE else ev.get(cid, []) + [x for x in q if x['quote'] not in {y['quote'] for y in ev.get(cid, [])}]
# study sizes from the published texts
N = {'dimant-requiem-forecast': '1,200 MTurk participants', 'dimant-deviant-choice': '418 participants', 'dimant-contagion-multi': '185 participants',
     'dimant-observability-choice': '423 lab and 1,650 online participants', 'dimant-conspiracy-choice': '4,128 participants', 'dimant-opioid-forecast': '512 veterans',
     'biz07': '312 participants in experiments 2 and 3; 369 in experiment 4', 'biz08': 'Eight experiments'}
for cid, n in N.items():
    C[cid].setdefault('study', {})['n'] = n
# axe08: the top-freelancer result is suggestive, so the forecast claims the opposite
C['axe08']['forecast'] = {'claim': 'Freelancers with strong past performance were shielded from the losses.', 'truth': False}
C['social14']['scene'] = re.sub(r'\bstudents\b', 'participants', C['social14']['scene'])
# social03 restated social01's finding from the same paper: retire it as a duplicate
if 'social03' in C:
    bank['challenges'] = [c for c in bank['challenges'] if c['id'] != 'social03']
    bank['retired'].append({'id': 'social03', 'title': C['social03']['title'], 'sources': C['social03']['sources'], 'reason': 'Review 4: duplicate of social01 (same paper, same tight-versus-loose result).'})
    for p in bank['paths']: p['ids'] = [i for i in p['ids'] if i != 'social03']
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
bank = json.loads((ROOT / 'src/bank.json').read_text())
for c in bank['challenges']:
    if c['id'] == 'dimant-masks-forecast':
        c['explain'] = 'Across 4,931 participants, none of the 7 nudges promoted mask-wearing in either party. Forecasters overestimated the effects overall (z = 4.40, p < 0.001), most of all for Democrats.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('masks ok')
