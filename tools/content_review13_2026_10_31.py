"""Fixes from independent review 13 (2026-10-31). Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
ev = json.loads((ROOT / 'src/evidence.json').read_text())
# minor 1: sibling spoilers
c = C['civic-wallet-experts']
c['question'] = 'How likely is it that the study found this?'
c['forecast'] = {'claim': 'Fewer than half of the surveyed economists predicted that return rates would rise with more money.', 'truth': True}
c['answerTitle'] = 'Fewer than a third of economists foresaw the pattern'
for f in c['follow']:
    f['a'] = f['a'].replace(' rather than the rise that occurred', '')
C['social15']['implication'] = 'When teams distrust each other, measure how they actually treat each other, not only how they feel about each other.'
for f in C['forecast-training']['follow']:
    if f['q'] == 'Does training replace teamwork?': f['a'] = 'No. The authors treat training as one of several interventions that raised accuracy.'
for f in C['rollout1']['follow']:
    if f['q'] == 'Why start with newer agents?': f['a'] = 'Less experienced and lower-skilled agents improved both speed and quality, which made them the natural first group.'
# minor 2 and 5: predictions resolve both ways, and no invented expectations
c = C['axf02']; c['forecast'] = {'claim': 'Scientists’ average predictions missed which texts raised vaccination most.', 'truth': True}
for k in ('axb13', 'dimant-opioid-forecast', 'axe10', 'rollout2'):
    C[k]['scene'] = re.sub(r'\s*(A common expectation is|Many marketers expect)[^.]*\.$', '', C[k]['scene'])
# minor 3: the scene must not state the mechanism the diagram asks about
C['axb05']['scene'] = 'A health system uses a widely sold algorithm to choose patients for an extra-care program.'
# minor 4: the keyed option is not the only hedged one
C['social13']['options'] = [{'Large gains, mostly in final rounds': 'Unfavorable to women, with tight estimates'}.get(o, o) for o in C['social13']['options']]
# minor 6: the study measured customer responses, not what a manager should do
C['axf04']['question'] = 'For each message, which messenger drew the better customer response?'
# minor 10: plain words for the audience; statistics stay in the source tab
C['forecast-teams-rank']['explain'] = 'In a tournament that began with 2,246 forecasters, teams were clearly more accurate than forecasters who saw the crowd’s beliefs, who in turn clearly beat forecasters working alone.'
C['forecast-training']['explain'] = 'In a tournament that began with 2,246 forecasters, about 45 minutes of probability training beat scenario training, and training was one of three interventions that raised accuracy.'
# minor 13: evidence hygiene; an unsourced replication claim leaves the follow-ups
ev['opposing-views-bot'] = [q for q in ev.get('opposing-views-bot', []) if not re.fullmatch(r'PMC\d+, Europe PMC full text', q['quote'])]
C['accuracy-prompt']['follow'] = [f for f in C['accuracy-prompt']['follow'] if 'Roozenbeek' not in f['a']]
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
ev = json.loads((ROOT / 'src/evidence.json').read_text())
# the replication quotes came from Roozenbeek et al. (2021), which is not a source of this decision
ev['accuracy-prompt'] = [q for q in ev['accuracy-prompt'] if not q['quote'].startswith('The first stage of the replication test')]
F = {'q': 'How was the Twitter test run?', 'a': 'In Study 7, 5,379 Twitter users who had recently shared news links got a private message asking them to rate the accuracy of one non-political headline; the researchers then tracked what they shared.'}
if not any(f['q'] == F['q'] for f in C['accuracy-prompt']['follow']): C['accuracy-prompt']['follow'].insert(0, F)
for k, qs in ev.items():   # RULE G: location strings posing as quotes, everywhere
    if isinstance(qs, list): ev[k] = [q for q in qs if not re.fullmatch(r'PMC\d+, Europe PMC full text', q['quote'])]
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok2')
