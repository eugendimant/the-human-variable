"""Fixes from independent review 8 (2026-10-31). Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
# --- M3: the measurement path also holds tests where the intervention worked
for p in bank['paths']:
    if p['id'] == 'measure':
        p['ids'] = ['bz01', 'bz05', 'bz11', 'bz09', 'bz02', 'bz10', 'accuracy-prompt', 'bz07', 'dimant-masks-forecast', 'dimant-requiem-forecast', 'civic-wallet-experts']
# --- M4: the node that names the mechanism stays masked until the reveal
for cid, node in (('dimant-notalie-causal', 'gain'), ('axe12', None), ('meta-perception-causal', 'fix')):
    d = C[cid]['dag']
    for n in d['nodes']:
        if (node and n['id'] == node) or (node is None and re.search(r'lazy', n['label'], re.I)): n['mask'] = True
# --- minor 2: same-paper siblings do not state each other's answers
C['social15']['implication'] = re.sub(r',?\s*since pessimistic expectations drove the hostility', '', C['social15']['implication'])
C['social15']['implication'] = re.sub(r'\s*since pessimistic expectations drove the hostility', '', C['social15']['implication'])
# --- minor 6, 7, 8
x = C['axe11']; o = x['options']; gt, gf, ht, hf = (o.index(s) for s in ('GPT-3-written, true', 'GPT-3-written, false', 'Human-written, true', 'Human-written, false'))
x['rankTies'] = [sorted([gt, gf]), sorted([ht, hf]), sorted([hf, gt]), sorted([gf, ht])]   # only same-truth comparisons were tested
m = C['dimant-masks-forecast']
m['forecast']['claim'] = 'At least one of the seven messages increased mask-wearing intentions among Democrats or Republicans.'
m['explain'] = m['explain'].replace('promoted mask-wearing', 'raised mask-wearing intentions or pledges')
for t in bank['themes']:
    if t['id'] == 'forecasting': t['principle'] = 'Forecasts improve with training, teaming and scoring, and fail through overconfidence and planning optimism. Whether turn-taking or members’ ability drives group performance is still debated.'
C['biz02']['options'] = [o if o != 'Employees read the form as mandatory' else 'Few employees knew they could change it' for o in C['biz02']['options']]
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
if 'biz06' in C:
    bank['challenges'] = [c for c in bank['challenges'] if c['id'] != 'biz06']
    bank['retired'].append({'id': 'biz06', 'title': C['biz06']['title'], 'sources': C['biz06']['sources'], 'reason': 'Review 8: repeats biz05 (same paper, same smiley-face result).'})
    for p in bank['paths']: p['ids'] = [i for i in p['ids'] if i != 'biz06']
f = C['civic-wallet-experts']['follow']
for i, x in enumerate(f):
    if re.search(r'46%.*61%.*72%', x['a']): f[i] = {'q': 'Why might the experts have missed it?', 'a': 'They expected self-interest to win out. The authors trace the rise to concern for the owner combined with an aversion to seeing oneself as a thief.'}
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('siblings')
ev = json.loads((ROOT / 'src/evidence.json').read_text())
q = {'source': C['civic-wallet-experts']['sources'][0], 'quote': 'a combination of altruistic concerns and an aversion to viewing oneself as a thief', 'location': 'Abstract (PubMed 31221770, Science version of record)'}
if q['quote'] not in [x['quote'] for x in ev.get('civic-wallet-experts', [])]: ev.setdefault('civic-wallet-experts', []).append(q)
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n'); print('evidence')
# --- minor 1: evidence entries say exactly what they are
ev = json.loads((ROOT / 'src/evidence.json').read_text())
ev['dimant-masks-forecast'] = [q for q in ev.get('dimant-masks-forecast', []) if 'condensed' not in q.get('location', '')]
ev['axe10'] = [q for q in ev.get('axe10', []) if 'as summarized' not in q.get('location', '')]
for k, qs in ev.items():
    for q in qs:
        loc = q.get('location', '')
        loc = loc.replace('(via new_sources.json; reconfirmed)', '(published version)').replace('(values transcribed)', '(published version; table values as printed)')
        loc = re.sub(r'read via fetch tool, which summarized the rest', 'abstract text', loc)
        loc = re.sub(r'read via f[^)]*', 'Carlson School author copy of the published article', loc) if 'Carlson School author copy; read via' in loc else loc
        q['location'] = loc
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n'); print('labels')
ev = json.loads((ROOT / 'src/evidence.json').read_text())
for k, qs in ev.items():
    for q in qs:
        q['location'] = q['location'].replace('Design (new_sources.json, journal PDF)', 'Design (journal PDF)').replace('; 60.0% is GPT + overview, 70.6% GPT only per new_sources.json', '; 60.0% is GPT-4 plus overview, 70.6% GPT-4 only')
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n'); print('labels2')
# --- minor 3: a second allocation item where the study separated one arm from the rest
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
x = C['axb08']
if x['format'] == 'choice':
    o = x['options']; vals = {'Human opponent': 0, 'Human with demographic profile': 0, 'GPT-4': 0, 'GPT-4 with demographic profile': 81.2}
    labels = {'Human opponent': 'Baseline', 'Human with demographic profile': '−15.7% (n.s.)', 'GPT-4': '+21.9% (n.s.)', 'GPT-4 with demographic profile': '+81.2%'}
    x['format'] = 'allocate'; x.pop('answer'); x.pop('chart', None)
    x['question'] = 'Which opponent shifted agreement most? Spread 100 points by how likely each is.'
    x['allocate'] = {'total': 100, 'step': 10, 'label': 'Points placed', 'prefix': '', 'suffix': '', 'values': [vals[k] for k in o], 'valueLabels': [labels[k] for k in o],
                     'valueName': 'change in odds of higher agreement than in human-human debates (non-significant changes count as zero)', 'best': [o.index('GPT-4 with demographic profile')]}
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('axb08')
