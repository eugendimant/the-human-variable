"""Fixes from independent review 5 (2026-10-31). Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']
ev = json.loads((ROOT / 'src/evidence.json').read_text())

# --- M1: the start-here path must not answer its own later steps
C['rollout1']['follow'][0] = {'q': 'Why start with newer agents?', 'a': 'Less experienced and lower-skilled agents improved both speed and quality, so the assistant closed part of the gap to their more experienced colleagues.'}
for t in C['rollout3']['delegate']['tasks']:
    t['why'] = re.sub(r',?\s*(and )?\d+(\.\d+)?% faster', '', t['why'])
# --- M2: a route the study found equally good also counts
for t in C['axe01']['delegate']['tasks']:
    if t['text'].startswith('Pick a vacation spot'):
        t['also'] = [C['axe01']['delegate']['choices'].index('Human recommender')]
        t['why'] = 'Resistance to AI in hedonic choices disappeared when AI augmented a human decision maker, bringing trust up to the level of a human recommender (Study 6), so both routes count.'
# --- M3: axe02's routings were never compared against each other: retire
if 'axe02' in C:
    bank['challenges'] = [c for c in bank['challenges'] if c['id'] != 'axe02']
    bank['retired'].append({'id': 'axe02', 'title': C['axe02']['title'], 'sources': C['axe02']['sources'], 'reason': 'Review 5: its routings were not compared against each other in the cited studies.'})
    for p in bank['paths']: p['ids'] = [i for i in p['ids'] if i != 'axe02']
    used = {x for c in bank['challenges'] for x in c['sources']}
    for sid in C['axe02']['sources']:
        if sid not in used and sid in S: bank['unused_sources'][sid] = S.pop(sid)
# --- M6: forecast claims stated neutrally
C['dimant-masks-forecast']['forecast']['claim'] = 'One of the seven messages increased mask-wearing among Democrats or Republicans.'
C['dimant-observability-choice']['forecast']['claim'] = 'Letting another person watch each donation decision raised giving.'
C['axf02']['forecast']['claim'] = 'Scientists’ average predictions tracked which texts raised vaccination most.'
C['dimant-motivated-estimate']['forecast']['claim'] = 'Without political labels, people chose lenient and strict peers’ information equally often.'
f6 = C['axf06']
if f6['format'] == 'forecast':
    f6.pop('forecast'); f6['format'] = 'estimate'
    f6['scene'] = f6['scene'].rstrip() + ' Physicians with usual resources only scored a median 74%.'
    f6['question'] = 'What median score did physicians with GPT-4 reach?'
    f6['estimate'] = {'target': 76, 'min': 40, 'max': 100, 'tolerance': 3, 'label': 'Median diagnostic reasoning score with GPT-4', 'unit': '%'}
# --- minor 1 and 2: pick-two with four options and no negation pair; no duplicate or premise-breaking distractors
s1 = C['social01']
s1['options'] = ['People ignored the norm and played their own strategy', 'Loose norms generated more behavioral variation', 'Tight norms produced the most extreme choices', 'The spread of others’ behavior shaped choices, not just its mean']
s1['multiAnswers'] = [1, 3]
C['bz14']['options'] = [o if o != 'No difference between procedures' else 'Neither: both leaned on interview impressions' for o in C['bz14']['options']]
C['false-news-spread']['options'] = [o if o != 'False stories spread no faster overall' else 'Platform ranking pushed false stories up' for o in C['false-news-spread']['options']]
C['bz15']['options'] = [o if o != 'None: all three were similar' else 'Opt-in with a reminder letter' for o in C['bz15']['options']]
# --- minor 5: the authors' own description of their estimates
s13 = C['social13']
s13['question'] = 'How did the authors describe the weight of their own estimates?'
s13['options'] = ['Precise gains for women in each round', 'No effect of the screen on women', 'Favorable to women, some with large standard errors', 'Unfavorable to women overall']
s13['answer'] = 2
s13['answerTitle'] = 'Favorable to women, with some imprecise estimates'
# --- minor 6, 7, 8
C['genai1']['follow'][2] = {'q': 'How much did output rise?', 'a': 'Artists’ productivity rose 25% after adoption, alongside more favorable peer evaluations of their work.'}
for f in C['axe10']['follow']:
    f['a'] = f['a'].replace('No. The abstract says up to 50% higher click-through, an upper bound, not an average across images.', 'No. Up to 50% higher click-through is the best case across the images tested, not their average.')
C['axe07']['boundary'] = 'Nine forecasting experiments with 4,820 participants who chose between their own forecasts and an algorithm’s, under low and high uncertainty.'
C['axe09']['boundary'] = 'Online experiments in which people imagined jobs, their own or others’, being taken over by robots or by other workers.'
C['axe12']['boundary'] = 'Four preregistered vignette experiments with 4,439 online participants rating colleagues and candidates who used AI or other help.'
d = C['axf04']['delegate']
d['tasks'] = [t for t in d['tasks'] if t['text'].startswith(('A discount larger', 'A renewal price'))]
# --- minor 13: sources named in content are in the bank
S['isoni11'] = {'id': 'isoni11', 'authors': 'Isoni, Loomes & Sugden', 'authors_full': 'Andrea Isoni, Graham Loomes, Robert Sugden', 'year': 2011,
  'title': 'The Willingness to Pay—Willingness to Accept Gap, the “Endowment Effect,” Subject Misconceptions, and Experimental Procedures for Eliciting Valuations: Comment',
  'venue': 'American Economic Review', 'volume': '101(2)', 'pages': '991-1011', 'doi': '10.1257/aer.101.2.991', 'url': 'https://doi.org/10.1257/aer.101.2.991', 'kind': 'peer-reviewed',
  'takeaway': 'Under the Plott and Zeiler procedures, the willingness-to-pay/willingness-to-accept gap is absent for mugs but significant and persistent for lotteries.',
  'verification': {'status': 'verified_abstract', 'checked': '2026-10-31', 'metadata': 'matched Crossref record', 'text_read': 'abstract (Crossref)'}}
if 'isoni11' not in C['bz06']['sources']: C['bz06']['sources'].append('isoni11')
ev['bz06'] = [q for q in ev.get('bz06', []) if q.get('source') != 'isoni11'] + [{'source': 'isoni11', 'quote': 'exhibit a significant and persistent disparity when the same experimental procedures are applied to lotteries', 'location': 'Abstract'},
  {'source': 'isoni11', 'quote': 'the willingness-to-pay/willingness-to-accept disparity is absent for mugs in a particular experimental setting', 'location': 'Abstract'}]
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
b15 = C['bz15']
if b15['format'] == 'multi':
    b15.pop('multiAnswers'); b15['format'] = 'rank'
    b15['options'] = ['Opt-in (default: not a donor)', 'Neutral (must choose, no default)', 'Opt-out (default: donor)']
    b15['rankAnswer'] = [2, 1, 0]; b15['rankTies'] = [[1, 2]]; b15['rankLabel'] = 'Highest share consenting to be a donor'
    b15['question'] = 'Rank the three forms by the share who agreed to be donors.'
    b15['permuted'] = True
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('bz15 rank')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
C['dimant-notalie-causal']['scene'] = 'In an incentivized experiment, people could misreport for money. Those who misreported were also the most likely to say that most others misreport.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('scene ok')
