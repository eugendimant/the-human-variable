"""Fixes from independent review 4 (2026-10-31). Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']

def strip_answer(c):
    for k in ('options', 'answer', 'multiAnswers', 'rankAnswer', 'rankTies', 'rankValues', 'rankLabel', 'allocate', 'estimate', 'forecast', 'delegate', 'chart', 'dag'): c.pop(k, None)

# --- M1: no answers carried into other items of the same path
C['rollout3']['explain'] = 'Inside the frontier, consultants with GPT-4 completed 12.2% more tasks and finished them faster. On the outside-frontier case, correctness fell from 84.5% without AI to 70.6% with GPT-4 and 60.0% with GPT-4 plus a prompt overview.'
C['rollout2']['follow'][2] = {'q': 'Why might experts gain little?', 'a': 'The authors argue the assistant spreads the know-how of the most able agents, which experienced agents already have.'}
C['dimant-polarizednorms-choice']['explain'] = 'In polarized environments, most people preferred extreme actions that exposed them to considerable strategic risk over intermediate actions that minimized it.'
C['social01']['follow'][2] = {'q': 'Why does this matter for a manager?', 'a': 'Two teams with the same average norm can behave very differently once the spread of views differs, so report the spread as well as the mean.'}
C['dimant-hate-choice']['follow'][0] = {'q': 'What does "grim expectations" mean here?', 'a': 'Pessimistic beliefs about how cooperative the opposing faction would be, held before any interaction took place.'}
C['dimant-hate-choice']['follow'][1] = {'q': 'What is the lever for a manager?', 'a': 'Correcting what each side expects of the other targets the source of the gap more directly than appeals to goodwill.'}
C['social15']['follow'][1] = {'q': 'Was this about politics alone?', 'a': 'The studies compared political identity with other political and nonpolitical identities.'}
C['social15']['follow'][2] = {'q': 'Which outcomes counted as behavior?', 'a': 'How people helped, harmed and cooperated with members of each group in incentivized games.'}
C['social16']['follow'][1] = {'q': 'How large was the evidence base?', 'a': 'Five preregistered studies with 15 experiments and over 8,600 participants.'}
C['social16']['follow'][2] = {'q': 'What does this mean for a manager?', 'a': 'Raising overall goodwill can leave the gap between groups in place, so track the gap itself, not only the average.'}
for p in bank['paths']:
    if p['id'] == 'dimant-lab' and p['ids'][:2] == ['dimant-polarizednorms-choice', 'social01']: p['ids'][:2] = ['social01', 'dimant-polarizednorms-choice']

# --- M2 and M5: published numbers only; contested results enter as items about the contest
s13 = C['social13']
if s13['format'] != 'choice' or 'Suggestive' not in ' '.join(s13.get('options', [])):
    strip_answer(s13); s13.update({'format': 'choice', 'question': 'How strong was the evidence that screens helped women advance?',
      'options': ['Strong: large, precise gains in each round', 'No effect: screens made no difference', 'Suggestive: favorable, several estimates imprecise', 'Harmful: screens lowered women’s chances'], 'answer': 2,
      'answerTitle': 'Favorable, but several estimates were imprecise',
      'explain': 'Goldin and Rouse estimate that blind auditions explain about 30% of the increase in women among new hires, with large standard errors on several estimates and some in the opposite direction.'})
s13['follow'][1] = {'q': 'How much of the rise in women does it explain?', 'a': 'About 30% of the increase in the proportion of women among new hires, and possibly 25% of the increase in women in the orchestras.'}
b6 = C['bz06']
if b6['format'] == 'rank':
    strip_answer(b6); b6.update({'format': 'choice', 'title': 'The mug market, revisited',
      'scene': 'In classic classroom markets, students given a mug asked a median $7.12 to sell it, while buyers offered $2.87. Plott and Zeiler reran the design with procedures that remove misunderstandings: training, practice rounds and anonymous offers.',
      'question': 'What happened to the gap between sellers and buyers?',
      'options': ['It stayed about as large', 'It shrank by about half', 'It disappeared', 'It reversed: buyers valued more'], 'answer': 2,
      'answerTitle': 'Under careful procedures, the mug gap disappeared',
      'explain': 'Sellers’ median of $7.12 against buyers’ $2.87 in the original markets gave way to no gap under Plott and Zeiler’s procedures. Isoni, Loomes and Sugden later confirmed this for mugs but found a persistent gap for lotteries.',
      'implication': 'Before pricing on an "owners overvalue" story, test it with clear instructions and practice; the effect depends on how the choice is elicited.',
      'boundary': 'Student markets for mugs under two elicitation procedures, with the follow-up debate extending to lotteries.'})
    if 'plott05' not in b6['sources']: b6['sources'].append('plott05')
S['plott05']['takeaway'] = 'With procedures designed to remove misconceptions, the gap between willingness to accept and willingness to pay for mugs disappeared; Isoni, Loomes and Sugden (2011) confirmed this for mugs but found a persistent gap for lotteries.'
f6 = C['axf06']
if f6['format'] == 'allocate':
    strip_answer(f6); f6.update({'format': 'forecast', 'question': 'How likely is it that the study found this?',
      'forecast': {'claim': 'Physicians given GPT-4 scored clearly higher on diagnostic reasoning than physicians with usual resources.', 'truth': False},
      'answerTitle': '76% versus 74%: no clear gain for physicians',
      'explain': 'Physicians scored a median 76% with GPT-4 and 74% with usual resources only, a difference that was not statistically significant (P = .60).',
      'boundary': 'Fifty US physicians working six challenging clinical vignettes, graded on a structured reasoning rubric.'})

# --- M3: allocation is a probability split over which option worked best (scored with a proper rule)
C['axe04']['question'] = 'How likely is each version to have persuaded most? Spread 100 points.'
C['axe04']['allocate'].update({'label': 'Points placed', 'suffix': ''})
C['axe04']['allocate'].pop('pass', None)
C['axe04']['implication'] = 'Assume cheap AI copy can persuade nearly as well as professionals; review AI-written material for accuracy, not only tone.'
C['axf01']['question'] = 'Which setup kept people most honest? Spread 100 points by how likely each is.'
C['axf01']['allocate'].update({'label': 'Points placed', 'suffix': ''})
C['axf01']['allocate'].pop('pass', None)

# --- M5: delegate tasks rest on routings the papers measured
a2 = C['axe02']['delegate']
if any(t['text'].startswith('Replies to patients') for t in a2['tasks']):
    a2['choices'] = ['Person with an AI assistant', 'Person alone', 'AI first stage, person finishes']
    a2['tasks'] = [t for t in a2['tasks'] if not t['text'].startswith('Replies to patients')]
    for t in a2['tasks']:
        if t['text'].startswith('Outbound sales'): t['why'] = 'Undisclosed bots sold about as well as proficient staff, but disclosing the bot before the conversation cut purchase rates by more than 79.7%.'
    C['axe02']['explain'] = 'Disclosing a sales bot up front cut purchases by more than 79.7%, AI on the codified first stage of telemarketing raised sales, and a coding assistant raised completed tasks by 26.08%.'
    C['axe02']['boundary'] = 'Three field settings: outbound sales calls, a telemarketing firm, and software developers at three companies.'
if 'axe03' in C:
    bank['challenges'] = [c for c in bank['challenges'] if c['id'] != 'axe03']
    bank['retired'].append({'id': 'axe03', 'title': C['axe03']['title'], 'sources': C['axe03']['sources'], 'reason': 'Review 4: routings rested on author suggestions, and the abstracts report no effect sizes.'})
    for p in bank['paths']: p['ids'] = [i for i in p['ids'] if i != 'axe03']
    used = {x for c in bank['challenges'] for x in c['sources']}
    for sid in C['axe03']['sources']:
        if sid not in used and sid in S: bank['unused_sources'][sid] = S.pop(sid)

# --- minor 1: task order must not follow a pattern
t4 = C['axf04']['delegate']['tasks']; order = ['A discount larger', 'A renewal price', 'A delivery fee', 'A free upgrade']
C['axf04']['delegate']['tasks'] = sorted(t4, key=lambda t: next(i for i, o in enumerate(order) if t['text'].startswith(o)))

# --- minor 2: pick-two items get four options with no logical negations
b5 = C['biz05']
b5['options'] = ['Above-average households raised their electricity use', 'Some already-efficient households raised usage', 'Feedback had no effect on heavy users', 'A smiley face kept efficient homes steady']
b5['multiAnswers'] = [1, 3]
s16 = C['social16']
if len(s16['options']) == 3:
    s16['options'] = ['The nudges closed the partisan gap on most measures', 'The interventions improved prosociality', 'The norm nudge worked; the default did not', 'Measured polarization gaps persisted']
    s16['multiAnswers'] = [1, 3]

# --- minor 13 and 14
C['dimant-enforcers-rank']['implication'] = 'When you build a speak-up channel, tell staff that most colleagues object to bribes and back reporting; it raises reporting most for deals that create unfair advantages.'
C['genai1']['follow'][2] = {'q': 'How much did output rise?', 'a': 'The abstract reports that artists’ productivity rose 25% after adoption, alongside more favorable peer evaluations of their work.'}
C['axf04']['implication'] = 'If bots deliver price increases, review that choice for fairness and disclosure; deliver generous offers through people, where they earn more credit.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')

# --- M2 sweep (RULE G): numbers that rested on a working-paper text now cite a peer-reviewed report of them
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']
S['cribb20'] = {'id': 'cribb20', 'authors': 'Cribb & Emmerson', 'authors_full': 'Jonathan Cribb, Carl Emmerson', 'year': 2020,
  'title': 'What happens to workplace pension saving when employers are obliged to enrol employees automatically?', 'venue': 'International Tax and Public Finance',
  'volume': '27(3)', 'pages': '664-693', 'doi': '10.1007/s10797-019-09565-6', 'url': 'https://doi.org/10.1007/s10797-019-09565-6', 'kind': 'peer-reviewed',
  'takeaway': 'Reports Madrian and Shea’s cohort comparison: 86% enrolled after 3 to 15 months under automatic enrollment against 37% without it; finds large rises in UK workplace pension saving after mandated automatic enrollment.',
  'verification': {'status': 'verified_full_text', 'checked': '2026-10-31', 'metadata': 'matched Crossref record', 'text_read': 'full text, introduction (Springer)', 'text_url': 'https://link.springer.com/article/10.1007/s10797-019-09565-6'}}
b1 = C['biz01']
if 'cribb20' not in b1['sources']: b1['sources'].append('cribb20')
b1['chart']['note'] = 'Madrian & Shea (2001), cohorts at 3 to 15 months of tenure, as reported by Cribb & Emmerson (2020).'
S['defaults01']['verification']['text_read'] = 'QJE abstract; participation figures as reported in Cribb & Emmerson (2020, International Tax and Public Finance)'
S['defaults01']['verification']['status'] = 'verified_abstract'
S['defaults01']['verification'].pop('text_url', None)
ev = json.loads((ROOT / 'src/evidence.json').read_text())
ev['biz01'] = [q for q in ev.get('biz01', []) if 'NBER' not in q.get('location', '')] + [
  {'source': 'cribb20', 'quote': 'with 86% of employees enrolled in the 401(k) after 3–15 months', 'location': 'Introduction'},
  {'source': 'cribb20', 'quote': 'compared with only 37% of those who were not subject to automatic enrolment', 'location': 'Introduction'}]
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('biz01 sourced')

# --- numbers seen only in working-paper texts are removed from the content (versions of record only)
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
s13 = C['social13']
s13['explain'] = 'Goldin and Rouse found that the screen raised women’s chances of advancing and being hired, with several estimates imprecise and one running the other way.'
s13['follow'][1] = {'q': 'What did the authors conclude?', 'a': 'That blind auditions fostered impartiality in hiring and contributed to the rising share of women in orchestras.'}
a2 = C['ai02']
a2['boundary'] = 'Occupation-specific, incentivized writing tasks for 453 college-educated professionals.'
for i, f in enumerate(a2['follow']):
    if f['q'] == 'How long were the tasks?': a2['follow'][i] = {'q': 'Who took part?', 'a': '453 college-educated professionals in a preregistered online experiment, randomly given access to ChatGPT or not.'}
b2 = C['biz02']
b2['follow'] = [
  {'q': 'Did many keep the default rate?', 'a': 'Yes. A substantial share of employees hired under automatic enrollment kept the default contribution rate, which few earlier hires had chosen.'},
  {'q': 'Did they keep the default fund too?', 'a': 'Yes. Many also kept the default fund allocation, an outcome few employees hired before the switch picked.'},
  {'q': 'What does this mean for plan design?', 'a': 'The default sets the saving rate as well as participation, so choose a default contribution rate you would recommend.'}]
C['social12']['study']['n'] = 'Fictitious résumés sent to help-wanted ads in Boston and Chicago'
ev = json.loads((ROOT / 'src/evidence.json').read_text())
for k in list(ev):
    ev[k] = [q for q in ev[k] if not __import__('re').search(r'NBER|working paper', q.get('location', ''), __import__('re').I)]
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('wp numbers removed')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
C['social12']['follow'][0] = {'q': 'Was the gap the same across jobs?', 'a': 'Yes. The racial gap was uniform across occupation, industry and employer size.'}
C['social12']['follow'][2] = {'q': 'Did "Equal Opportunity Employer" ads differ?', 'a': 'No. Employers who listed that label in their ads discriminated as much as other employers.'}
C['ai01']['follow'][0] = {'q': 'Who took part?', 'a': '453 college-educated professionals, each given occupation-specific, incentivized writing tasks typical of their job.'}
C['ai02']['follow'][0] = {'q': 'Did quality really improve?', 'a': 'Yes. Average output quality rose 18%, alongside a 40% cut in time.'}
C['ai02']['follow'][1] = {'q': 'Which tasks?', 'a': 'Midlevel professional writing tasks matched to each participant’s occupation.'}
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('follow-ups fixed')
bank = json.loads((ROOT / 'src/bank.json').read_text())
for p in bank['paths']:
    if p['id'] == 'design' and p['ids'].index('judg05') > p['ids'].index('bz03'):
        p['ids'].remove('judg05'); p['ids'].insert(p['ids'].index('bz03'), 'judg05')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('paths ordered')
