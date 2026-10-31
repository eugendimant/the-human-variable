"""Fixes from independent review 19 (2026-10-31). Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
ev = json.loads((ROOT / 'src/evidence.json').read_text())
# M1: the 75.4% belongs to the single-occupancy subsample; the full Study 2 comparison is 93.3% vs 76.5%
c = C['biz04']
c['explain'] = c['explain'].replace('the environmental sign reached 93.3% versus 75.4%.', 'the environmental sign reached 93.3% versus 76.5% for the norm signs combined.')
if c.get('chart'): c['chart']['values'] = [76.5 if v == 75.4 else v for v in c['chart']['values']]
for q in ev['biz04']:
    if q.get('quote', '').startswith('the standard environmental message (93.3%)'):
        q['quote'] = 'the standard environmental message (93.3%) was more effective than the four descriptive norm messages combined (76.5%)'
        q['location'] = 'PLoS ONE 9(8), Study 2 Results, full sample (N = 162); rechecked against the journal HTML'
# m2: the principle no longer contradicts bz16
for t in bank['themes']:
    if t['id'] == 'choice': t['principle'] = 'Defaults, frames and anchors decide many choices before preferences do, while menu effects are contested in real plans. The design of the decision is a management decision.'
# m3: the human-human baseline is the comparison point, not an option
c = C['axb08']; a = c['allocate']
if c['options'][0] == 'Human opponent':
    c['options'] = c['options'][1:]; a['values'] = a['values'][1:]; a['valueLabels'] = a['valueLabels'][1:]; a['best'] = [b - 1 for b in a['best']]; a['step'] = 1
    c['question'] = c['question'].rstrip() if 'human-human' in c['question'].lower() else c['question']
    c['scene'] = c['scene'].rstrip() + ('' if 'human-human' in c['scene'].lower() else ' The options below are compared with debates between two people.')
# m7: the paper reports the median interval as over 100 points
C['bz02']['question'] = 'Across 25 large ad experiments, the median ROI confidence interval was more than how many percentage points wide?'
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
