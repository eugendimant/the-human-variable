"""Review 35 content fixes. Idempotent; edits by text, never by index."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}

def rep(cid, field, old, new):
    C[cid][field] = C[cid][field].replace(old, new)

# m2: the equity contrast is similar in size and not significant at 5%
rep('dimant-enforcers-rank', 'explain', ' when it restored equity, a weaker difference.', ' when it restored equity, a similar gap that was not statistically significant.')
rep('dimant-enforcers-rank', 'explain', 'a similar gap that was not significant at the 5% level.', 'a similar gap that was not statistically significant.')
# m3: kept. Review 30 read the confidence option as the paper's uncertainty condition; review 35 says it was not tested. Not changed until the full text settles it (open item in the handover).
# audit 47 / review 35: the effect-size measure in plain words
ch = C['manylabs-anchoring']['chart']; ch['note'] = ch['note'].replace('Anchoring effect size, Cohen’s d (unweighted replication estimate per question).', 'Anchoring effect size, standardized; the original study reported one overall size.')
# m6: the title does not break at "human-human"
for c in ('axb08',):
    a = C[c].get('allocate') or {}
    if a.get('valueName'): a['valueName'] = a['valueName'].replace('human‑human', 'human-human')   # audit 49, m7: the font lacks U+2011; the page keeps compounds whole instead
# m17: say what the scope covers; answer the follow-up
rep('forecast-training', 'boundary', 'the paper reports significance tests for the training effect', 'with tests of the training effect across seasons') if 'the paper reports significance tests for the training effect' in C['forecast-training']['boundary'] else None

rep('forecast-training', 'boundary', 'volunteers; with tests of the training effect', 'volunteers, with tests of the training effect')
rep('forecast-training', 'boundary', 'Geopolitical forecasts by tournament volunteers, with tests of the training effect across seasons.', 'Geopolitical forecasts by volunteers in a two-year tournament.')   # audit 49, m6: grounded in the stored quote
rep('dimant-enforcers-rank', 'implication', 'in the study this raised willingness to act most for deals that create unfair advantages.', 'in the study this reliably raised willingness to act against deals that create unfair advantages.')   # audit 49, m5
# m18: who rated the answers
rep('axe05', 'boundary', 'rated for quality and empathy by a team of licensed health care professionals.', 'rated for quality and empathy by licensed health care professionals on the author team.')
# m17: the boundary states the setting once, without repeating the explanation
rep('rollout2', 'boundary', 'One firm’s support chat; the declines for top agents were small, and other occupations may differ.', 'One firm’s customer-support chat.')

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
# audit 49, m8: keyed options are pinned by hand only (invariant I11)
print('review 35 content applied')
