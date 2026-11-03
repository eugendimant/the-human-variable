"""Review 35 content fixes. Idempotent; edits by text, never by index."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}

def rep(cid, field, old, new):
    C[cid][field] = C[cid][field].replace(old, new)

# m2: the equity contrast is similar in size and not significant at 5%
rep('dimant-enforcers-rank', 'explain', ' when it restored equity, a weaker difference.', ' when it restored equity, a similar gap that was not significant at the 5% level.')
# m3: kept. Review 30 read the confidence option as the paper's uncertainty condition; review 35 says it was not tested. Not changed until the full text settles it (open item in the handover).
# audit 47 / review 35: the effect-size measure in plain words
ch = C['manylabs-anchoring']['chart']; ch['note'] = ch['note'].replace('Anchoring effect size, Cohen’s d (unweighted replication estimate per question).', 'Anchoring effect size, standardized; the original study reported one overall size.')
# m6: the title does not break at "human-human"
for c in ('axb08',):
    a = C[c].get('allocate') or {}
    if a.get('valueName'): a['valueName'] = a['valueName'].replace('human-human', 'human‑human')
# m17: say what the scope covers; answer the follow-up
rep('forecast-training', 'boundary', 'the paper reports significance tests for the training effect', 'with tests of the training effect across seasons') if 'the paper reports significance tests for the training effect' in C['forecast-training']['boundary'] else None

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())
for c in B['challenges']:
    if c['id'] in K and c.get('options'):
        K[c['id']] = {'keyed': sorted(c['options'][i] for i in (c['multiAnswers'] if c['format'] == 'multi' else [c['answer']])), 'options': sorted(c['options'])}
kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('review 35 content applied')
