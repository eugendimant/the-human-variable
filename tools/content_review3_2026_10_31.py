"""Fixes from independent review 3 (2026-10-31): midpoint-proof estimates (M5), allocate wording (M6), titles and ties (M7), content minors."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}

def to_forecast(cid, claim, truth, question='How likely is it that the study found this?'):
    c = C[cid]; c.pop('estimate', None); c['format'] = 'forecast'; c['question'] = question; c['forecast'] = {'claim': claim, 'truth': truth}

# --- M5: a midpoint guess must not score above 50
C['ai01']['estimate']['tolerance'] = 5
C['lies-in-disguise']['estimate']['tolerance'] = 5
C['social12']['estimate'].update({'min': 0, 'max': 200})
C['bz02']['estimate'].update({'min': 0, 'max': 500})
b = C['biz11']
b['scene'] = 'People spun a wheel that landed on 10 or 65, then estimated the share of UN member countries that are African. The group that saw 65 gave a median of 45%.'
b['question'] = 'What median estimate did the group that saw 10 give?'
b['estimate'].update({'target': 25, 'label': 'Median estimate after seeing 10'})
b['answerTitle'] = '25%, pulled down by a random number'
to_forecast('ai10', 'People moved further toward identical advice when it was labeled as an algorithm’s rather than other people’s.', True)
C['ai10']['answerTitle'] = '45% of the way, versus 30% for human advice'
to_forecast('dimant-motivated-estimate', 'Without political labels, people chose lenient and strict peers’ information about equally often.', False)
C['dimant-motivated-estimate']['answerTitle'] = 'They tilted toward lenient peers: about 55%'
to_forecast('genai2', 'With an edited prompt and the best of three drafts, GPT-3 articles drew at least as much agreement as the human-written originals.', True)
C['genai2']['answerTitle'] = 'About 53%, against 47% for the originals'
C['genai2']['explain'] = 'Editing the prompt and choosing the best of three outputs reached 52.7% agreement, against 47.4% for the human-written originals and 43.5% for raw GPT-3.'

# --- M6: the allocate payoff rewards the best arm, so ask for that; a disguised single choice becomes a choice
a = C['axe04']; a['question'] = 'Put the testing budget where it buys the most agreement.'
x = C['axb08']
if x['format'] == 'allocate':
    x = C['axb08']; vals = x['allocate']['values']; best = vals.index(max(vals))
    x.pop('allocate'); x['format'] = 'choice'; x['answer'] = best
    x['question'] = 'Which opponent shifted agreement most, compared with human-human debates?'
    labels = {'Human opponent': 0, 'Human with demographic profile': -15.7, 'GPT-4': 21.9, 'GPT-4 with demographic profile': 81.2}
    x['chart'] = {'labels': list(x['options']), 'values': [labels[o] for o in x['options']], 'unit': '%', 'highlight': best,
                  'note': 'Change in odds of higher agreement vs human-human debates (Salvi et al. 2025). Only personalized GPT-4 differed significantly (+81.2%).'}

# --- M7: titles that claim untested differences
C['dimant-enforcers-rank']['answerTitle'] = 'Inequity raised reporting; norm information helped most there'
C['axe11']['answerTitle'] = 'GPT-3 tweets helped true claims; false ones were a toss-up'
C['civic-wallet-rank']['title'] = 'Lost wallets, different contents'

# --- content minors
C['dimant-enforcers-rank']['implication'] = 'When you build a speak-up channel, tell staff how many colleagues report and that most think reporting is right; it raises reporting most for unfair deals.'
C['biz02']['options'] = [o if o != 'Changing the default was not allowed' else 'The default had the best expected returns' for o in C['biz02']['options']]
C['axe06']['estimate']['tolerance'] = 10  # the study's standard error is 10.3
# path blurbs must not state findings
for p in bank['paths']:
    if p['id'] == 'trust-algo': p['blurb'] = 'Formulas against experts, models after an error, and the design choices that decide whether people accept algorithmic advice.'
    if p['id'] == 'measure': p['blurb'] = 'Matched ad lift, famous nudges and expert forecasts, each checked against a randomized test.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
# --- minor 4: boundaries state the study's scope, not what it left out
import re
for c in bank['challenges']:
    c['boundary'] = re.sub(r';\s[^;]*\b(were|was) not (tested|studied)\.$', '.', c['boundary'])
C['axe05']['boundary'] = 'Public forum answers by volunteer physicians, rated for quality and empathy by a team of licensed health care professionals.'
C['bz07']['boundary'] = 'One Chinese technology firm: a six-month randomized trial with 1,612 employees, with performance reviews over two years.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('boundaries ok')
