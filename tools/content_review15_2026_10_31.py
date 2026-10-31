"""Fixes from independent review 15 (2026-10-31). Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']
ev = json.loads((ROOT / 'src/evidence.json').read_text())
# m2: lees20 is checked on the version-of-record abstract and figure legend; the DASH manuscript may be the preprint
v = S['lees20']['verification']; v['status'] = 'verified_abstract'; v.pop('text_url', None)
v['text_read'] = 'Version-of-record abstract and Figure 4 legend on nature.com'
ev['meta-perception-causal'] = [q for q in ev['meta-perception-causal'] if 'DASH' not in q.get('location', '')]
ev['judg02'] = [q for q in ev.get('judg02', []) if not re.search(r'paraphrase|Walasek|Andre|de Langhe|reply', json.dumps(q), re.I)]
# m3: axes where a third of the range scored full marks
# negative values mean the change went the other way, so the true value no longer sits at the top of its axis
C['axb03']['estimate'].update(min=-30, max=30)
C['axb14']['estimate'].update(min=-25, max=35)
# m4: a clear rival claim
C['social13']['options'] = [{'Large gains, concentrated in early rounds': 'Clear gains, precisely estimated in every round'}.get(o, o) for o in C['social13']['options']]
# m5: sibling spoilers
for f in C['axb14']['follow']:
    if f['q'] == 'Is there a downside?': f['a'] = 'Yes. The same study built a task outside the frontier, where AI users did worse; the "Leading with AI" case covers that result.'
for f in C['rollout2']['follow']:
    if f['q'] == 'Did anyone gain on both?': f['a'] = 'The earlier steps of this case show which agents gained on speed and quality.'
# m6: the boomerang is a small, short study
C['biz05']['boundary'] = 'Two doorhanger messages to 290 California households, with electricity read from meters over about four weeks.'
C['biz05']['implication'] = 'When sending peer comparisons, add explicit approval for customers already doing better than average, and check in a pilot whether low users drift up.'
# m9: disclosure is not something to delay
C['axe14']['implication'] = 'Disclose the bot at the start of the call, as transparency rules require, and treat the measured drop in purchases as a cost to manage through service quality, not through hiding the bot.'
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
C['axe06']['estimate']['max'] = 100   # tolerance 10 follows the paper's standard error; a wider axis keeps a random guess low
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
