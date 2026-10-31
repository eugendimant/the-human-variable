"""Rewrite four classic items as measured predictions, using numbers verified on 2026-10-31 (docs/audit/verify_classics.json)."""
import json, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
S = bank['sources']
if 'loss79' not in S: S['loss79'] = bank['unused_sources'].pop('loss79')
def ver(sid, status, text, url):
    S[sid]['verification'].update({'status': status, 'text_read': text, 'text_url': url, 'checked': '2026-10-31'})
ver('frame81', 'verified_full_text', 'full text scan, p. 453 (Problems 1 and 2)', 'https://www.gwern.net/doc/psychology/1981-tversky.pdf')
ver('anchor74', 'verified_full_text', 'full text scan, p. 1128', S['anchor74']['verification'].get('text_url', ''))
ver('loss79', 'verified_full_text', 'full text transcription, p. 266 (Problem 3) and Table I p. 268 (Problem 3prime)', 'https://www.dmi-ida.org')
ver('defaults01', 'verified_full_text', 'QJE abstract; numbers from the paper\'s NBER working-paper version (WP 7682, p. 12)', 'https://www.nber.org/papers/w7682')
def keep(c, **kw):
    for k in ('options', 'answer', 'multiAnswers'): c.pop(k, None)
    c.update(kw)

keep(C['biz01'], format='estimate', title='The enrollment default',
  scene='A US firm switched its 401(k) from sign-up-yourself to automatic enrollment for new hires. Among the earlier cohort, who had to opt in, 37% participated at similar tenure.',
  question='What share of the automatically enrolled hires participated?',
  answerTitle='86% under the default, against 37%',
  explain='At 3 to 15 months of tenure, 86% of automatically enrolled hires participated, against 37% of the previous cohort who had to sign up.',
  estimate={'target': 86, 'min': 0, 'max': 100, 'tolerance': 8, 'label': 'Participation under automatic enrollment', 'unit': '%'},
  chart={'labels': ['Had to opt in', 'Enrolled by default'], 'values': [37, 86], 'unit': '%', 'highlight': 1, 'note': 'Madrian & Shea (2001); cohort comparison at similar tenure (NBER version, p. 12).'},
  study={'design': 'Natural experiment in one firm', 'n': 'Employees of a large US corporation'})
keep(C['judg05'], format='estimate', title='Same numbers, other frame',
  scene='A disease will kill 600 people. Framed as lives saved, 72% chose a sure plan (200 saved) over a gamble. Others saw the same plans framed as deaths: 400 die for sure, or a one-third chance nobody dies.',
  question='In the deaths frame, what share chose the gamble?',
  answerTitle='78% gambled once the frame was losses',
  explain='With identical outcomes, 72% chose the sure option when it was framed as lives saved; 78% chose the gamble when the same options were framed as deaths.',
  estimate={'target': 78, 'min': 0, 'max': 100, 'tolerance': 8, 'label': 'Share choosing the gamble in the deaths frame', 'unit': '%'},
  chart={'labels': ['Sure option, lives-saved frame', 'Sure option, deaths frame'], 'values': [72, 22], 'unit': '%', 'highlight': 1, 'note': 'Tversky & Kahneman (1981), p. 453; N = 152 and 155.'},
  study={'design': 'Survey experiment', 'n': '152 and 155 students'})
keep(C['biz11'], format='estimate', title='The wheel of fortune',
  scene='People spun a wheel that landed on 10 or 65, then estimated the share of UN member countries that are African. The group that saw 10 gave a median of 25%.',
  question='What median estimate did the group that saw 65 give?',
  answerTitle='45%, pulled up by a random number',
  explain='Median estimates were 25% after the wheel showed 10 and 45% after it showed 65, though everyone could see the number was random.',
  estimate={'target': 45, 'min': 0, 'max': 100, 'tolerance': 7, 'label': 'Median estimate after seeing 65', 'unit': '%'},
  chart={'labels': ['Wheel showed 10', 'Wheel showed 65'], 'values': [25, 45], 'unit': '%', 'highlight': 1, 'note': 'Tversky & Kahneman (1974), p. 1128.'},
  study={'design': 'Classroom experiment', 'n': 'Groups of participants'})
C['biz11']['implication'] = 'In negotiations and forecasts, write down your own estimate before you see anyone else’s number.'
new = {'id': 'judg09', 'track': 'Judgment', 'concept': 'Loss aversion', 'theme': 'choice', 'format': 'estimate', 'title': 'Gains and losses flip risk',
  'scene': 'Offered a sure $3,000 or an 80% chance of $4,000, 80% of people took the sure money. A second group faced the mirror image: a sure loss of $3,000 or an 80% chance of losing $4,000.',
  'question': 'What share chose the gamble when both options were losses?',
  'answerTitle': '92% gambled to avoid a sure loss',
  'explain': 'With gains, 80% chose the sure $3,000. With the same amounts as losses, 92% chose the gamble. People avoid risk for gains and seek it to escape a sure loss.',
  'implication': 'Expect teams behind on a target to take bigger risks. Review risky catch-up plans with the reference point in view.',
  'boundary': 'Hypothetical choices by 95 respondents per problem; real-stakes studies show the same pattern with varying size.',
  'sources': ['loss79'], 'estimate': {'target': 92, 'min': 0, 'max': 100, 'tolerance': 7, 'label': 'Share choosing the gamble with losses', 'unit': '%'},
  'chart': {'labels': ['Gamble chosen, gains', 'Gamble chosen, losses'], 'values': [20, 92], 'unit': '%', 'highlight': 1, 'note': 'Kahneman & Tversky (1979), Problem 3 (p. 266) and Problem 3prime (Table I, p. 268).'},
  'study': {'design': 'Hypothetical choice problems', 'n': '95 respondents per problem'},
  'follow': [{'q': 'Is this the reflection effect?', 'a': 'Yes. Kahneman and Tversky called it the reflection effect: preferences between gambles reverse when gains become losses.'},
             {'q': 'Were the stakes real?', 'a': 'No. These were hypothetical choices. The paper argues people generally know how they would behave in such situations.'},
             {'q': 'What else did the paper introduce?', 'a': 'Prospect theory: outcomes are judged as gains or losses from a reference point, and losses weigh more than gains of the same size.'}]}
if 'judg09' not in C: bank['challenges'].append(new)
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
print('ok')
