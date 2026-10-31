"""Fixes from independent review 18 (2026-10-31). Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']
ev = json.loads((ROOT / 'src/evidence.json').read_text())
# M1: the fund-menu effect is contested by large real-plan data, so bz16 becomes an item about the contest
S.setdefault('huberman06', {'id': 'huberman06', 'authors': 'Huberman & Jiang', 'authors_full': 'Gur Huberman, Wei Jiang', 'year': 2006,
  'title': 'Offering versus Choice in 401(k) Plans: Equity Exposure and Number of Funds', 'venue': 'Journal of Finance', 'volume': '61(2)', 'pages': '763-801',
  'doi': '10.1111/j.1540-6261.2006.00854.x', 'url': 'https://doi.org/10.1111/j.1540-6261.2006.00854.x', 'kind': 'peer-reviewed',
  'takeaway': 'In real 401(k) records, participants split contributions evenly across the few funds they use, but their equity share moves little with the share of equity funds offered.',
  'verification': {'status': 'verified_abstract', 'checked': '2026-10-31', 'metadata': 'matched RePEc record of the published article', 'text_read': 'Published abstract (IDEAS/RePEc)'}})
c = C['bz16']
if c['format'] != 'forecast':
    for k in ('options', 'answer', 'permuted'): c.pop(k, None)
    c.update(format='forecast', title='Two fund menus, revisited', question='How likely is it that the study found this?',
      scene='Benartzi and Thaler (2001) reported that the share invested in stocks rose with the share of stock funds on a 401(k) menu. Huberman and Jiang (2006) then examined administrative records of participants in many real 401(k) plans.',
      forecast={'claim': 'In the real-plan records, the share of equity funds on the menu was a strong predictor of how much participants put into equity.', 'truth': False},
      answerTitle='In real plans, the menu’s mix mattered little',
      explain='Huberman and Jiang found that participants split contributions evenly across the funds they use, typically three or four, yet their propensity to put money into equity funds was not very sensitive to the fraction of equity funds offered.',
      implication='Before redesigning a plan menu to steer risk, check your own participants’ records; in large real-plan data, equity exposure moved little with the menu’s mix.',
      boundary='Administrative records of 401(k) participants across many plans, set against earlier evidence from hypothetical allocation tasks and plan-level comparisons.',
      sources=['huberman06', 'benartzi01'], study={'design': 'Administrative 401(k) records', 'n': 'Participants in many 401(k) plans'},
      follow=[{'q': 'What did the original study find?', 'a': 'Benartzi and Thaler reported that some investors split contributions evenly across whatever funds are offered, so the stock share rose with the share of stock funds on the menu.'},
              {'q': 'Why do the results differ?', 'a': 'The designs differ: hypothetical allocation tasks and comparisons across plans, versus records of individual participants inside real plans.'},
              {'q': 'Does the even split still happen?', 'a': 'Yes. Participants tend to allocate evenly across the funds they use, but they use only a few, and that number does not track how many are offered.'}])
    c.pop('chart', None)
ev['bz16'] = [q for q in ev.get('bz16', []) if q.get('source') == 'benartzi01']
for q in ('participants tend to allocate their contributions evenly across the funds they use',
          'The number of funds used, typically between three and four, is not sensitive to the number of funds offered',
          "A participant's propensity to allocate contributions to equity funds is not very sensitive to the fraction of equity funds among offered funds."):
    if not any(x.get('quote') == q for x in ev['bz16']): ev['bz16'].append({'source': 'huberman06', 'quote': q, 'location': 'Published abstract, Journal of Finance 61(2) (IDEAS/RePEc)'})
# minor 2: rollout1 no longer marks the randomized answer wrong
c = C['rollout1']
if c['question'] != 'Which agents gained the most from the assistant?':
    c['question'] = 'Which agents gained the most from the assistant?'
    c['options'] = [{'A random sample across tenure': 'Agents with middling tenure', 'Team leads, who coach others': 'Agents handling the most common problems'}.get(o, o) for o in c['options']]
# minor 3: neutral titles
C['bz04']['title'] = 'Thesis deadlines'; C['rollout4']['title'] = 'Tutoring with GPT-4'; C['judg09']['title'] = 'Paired gambles'
# minor 4: rank items appear in paths
P = {p['id']: p for p in bank['paths']}
for pid, cid in (('trust-algo', 'axf05'), ('measure', 'forecast-teams-rank'), ('people', 'civic-wallet-rank')):
    if cid in C and cid not in P[pid]['ids']: P[pid]['ids'].append(cid)
# optional: editorial rules
bank['editorialRules'] = [r for r in bank.get('editorialRules', []) if 'stylized' not in r.lower()] if isinstance(bank.get('editorialRules'), list) else bank.get('editorialRules')
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
# minor 5: claim verbs no longer predict truth
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
C['biz08']['forecast'] = {'claim': 'People juggling other tasks were more likely to overlook improvements that remove something.', 'truth': True}
C['opposing-views-bot']['forecast'] = {'claim': 'Republicans who followed a liberal bot became more conservative afterward.', 'truth': True}
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok2')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
C['social08']['forecast'] = {'claim': 'The behavior spread farther through networks with random long ties than through clustered networks with redundant ties.', 'truth': False}
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok3')
