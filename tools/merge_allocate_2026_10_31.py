"""Merge the checked allocate/delegate/rank draft (docs/audit/draft_allocate_2026_10_31.json) with editorial decisions.

- axf03 (AMIE) dropped: overlaps axf06, developers ran the study, and the key comparison was not tested formally.
- axf02 (pharmacy megastudy) becomes a forecast: differences between individual texts were not tested, so they are not scored.
- axf05 (Jabbour): two follow-ups rested on partial web excerpts; replaced with abstract-level answers."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); ev = json.loads((ROOT / 'src/evidence.json').read_text())
d = json.loads((ROOT / 'docs/audit/draft_allocate_2026_10_31.json').read_text())
items = {c['id']: c for c in d['challenges'] if c['id'] != 'axf03'}
f = items['axf02']
for k in ('options', 'allocate'): f.pop(k)
f.update({'format': 'forecast', 'title': 'Twenty-two flu-shot texts',
  'question': 'Did the scientists see it coming?',
  'forecast': {'claim': 'Scientists’ average predictions closely tracked which texts raised vaccination most.', 'truth': False},
  'answerTitle': 'Scientists’ predictions missed: r = 0.03',
  'explain': 'All 22 texts raised vaccination over the 29.4% control rate, by 2.0 points on average. Scientists’ predictions did not track the results (r = 0.03) and placed the top text 15th of 22.'})
f['follow'][0] = {'q': 'Which text did best?', 'a': 'Two texts saying a flu shot was waiting for the patient: +2.9 percentage points, a 9.9% lift. Lay raters tracked results better than scientists (r = 0.60) but still placed it 16th.'}
j = items['axf05']
j['follow'][0] = {'q': 'What was the bias?', 'a': 'The researchers built models that made systematic errors linked to patient characteristics, then showed their predictions to clinicians.'}
j['follow'][1] = {'q': 'What did the authors conclude?', 'a': 'Standard AI raised accuracy, systematically biased AI lowered it, and image explanations did not mitigate the harm from the biased model.'}
used = {s for c in items.values() for s in c['sources']}
for sid, s in d['sources'].items():
    if sid in used: bank['sources'][sid] = s
have = {c['id'] for c in bank['challenges']}
for c in items.values():
    e = c.pop('evidence', [])
    if c['id'] not in have: bank['challenges'].append(c)
    ev[c['id']] = e
for p in bank['paths']:
    if p['id'] == 'leading-ai':
        for cid in ('axf01', 'axf06'):
            if cid not in p['ids']: p['ids'].append(cid)
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
print('merged', sorted(items))
