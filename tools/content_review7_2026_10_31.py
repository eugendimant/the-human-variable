"""Fixes from independent review 7 (2026-10-31). Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']

def retire(cid, reason):
    global C
    if cid not in C: return
    bank['challenges'] = [c for c in bank['challenges'] if c['id'] != cid]
    bank['retired'].append({'id': cid, 'title': C[cid]['title'], 'sources': C[cid]['sources'], 'reason': reason})
    for p in bank['paths']: p['ids'] = [i for i in p['ids'] if i != cid]

# --- M2: allocation items must test a prediction, not common sense
f1 = C['axf01']
if 'Report it yourself, no machine' in f1['options']:
    i = f1['options'].index('Report it yourself, no machine')
    for k in ('values', 'valueLabels'): del f1['allocate'][k][i]
    del f1['options'][i]
    f1['scene'] = 'Online participants privately rolled a die ten times and earned more for reporting higher numbers. They delegated the reports to a machine through one of three interfaces. About 95% reported honestly when they reported themselves.'
    f1['question'] = 'Which interface kept people most honest? Spread 100 points by how likely each is.'
a4 = C['axe04']
if a4['format'] == 'allocate':
    a4.pop('allocate'); a4.pop('options', None); a4.pop('permuted', None)
    a4['format'] = 'estimate'
    a4['question'] = 'With no article, 24.4% agreed with the claims. What share agreed after one unedited GPT-3 article?'
    a4['estimate'] = {'target': 43.5, 'min': 20, 'max': 100, 'tolerance': 6, 'label': 'Share agreeing after an unedited GPT-3 article', 'unit': '%'}
    a4['answerTitle'] = 'Unedited GPT-3 reached 43.5%, near the originals’ 47.4%'

# --- M4: the measurement path also holds tests that confirmed the claim
for p in bank['paths']:
    if p['id'] == 'measure':
        p['blurb'] = 'Ad lift, nudges, remote work and expert forecasts, each put to a randomized test.'
        p['ids'] = ['bz01', 'bz05', 'bz02', 'bz11', 'bz07', 'bz10', 'dimant-masks-forecast', 'dimant-requiem-forecast', 'civic-wallet-experts']

# --- M5: neutral scenes, rival distractors
retire('ai04', 'Review 7: repeats rollout1’s headline number from the same paper.')
C['biz07']['scene'] = 'A team has a slow approval process and is asked how to improve it.'
C['bz06']['scene'] = 'In classic classroom markets, students given a mug asked a median $7.12 to sell it, while buyers offered $2.87. Plott and Zeiler reran the design with training, practice rounds and anonymous offers.'
C['ai11']['title'] = 'Two jobs for an algorithm'
C['ai11']['options'] = [o for o in C['ai11']['options'] if o != 'Equally reluctant for both']
C['ai11']['answer'] = C['ai11']['options'].index('Judging a personal aesthetic preference')
C['misperceived-norms-action']['options'] = [o if o != 'Rose from about 6% to about 45%' else 'Rose from about 6% to about 8%, within noise' for o in C['misperceived-norms-action']['options']]
C['biz02']['options'] = [o if o != 'The default had the best expected returns' else 'Employees read the form as mandatory' for o in C['biz02']['options']]
C['social07']['options'] = [o if o != 'Identical views across parties' else 'Two opposed camps within each party' for o in C['social07']['options']]
s13 = C['social13']
s13['options'] = ['Large gains, mostly in final rounds', 'No effect, though estimates were noisy', 'Favorable to women, some with large standard errors', 'Unfavorable to women, mostly in early rounds']
s13['answer'] = 2
# --- minor 1, 2, 3, 4
C['axb01']['scene'] = C['axb01']['scene'].replace('three AI-supported tasks', 'two AI-supported tasks')
for cid in ('ai12', 'biz07', 'biz11', 'social10', 'axe09'):
    st = C[cid].get('study', {})
    if re.search(r'not read|^Eight experiments$|^Groups of|^Multiple', st.get('n', '')): st.pop('n', None)
C['ai01']['explain'] = re.sub(r'\s*Output quality also rose 18%\.', '', C['ai01']['explain'])
for f in C['ai02']['follow']:
    f['a'] = f['a'].replace(', alongside a 40% cut in time', '')
for f in C['axb13']['follow']:
    f['a'] = re.sub(r', alongside a 15% average rise in issues resolved[^.]*', '', f['a'])
for f in C['misperceived-norms-action']['follow']:
    if f['q'] == 'How wrong were the original beliefs?': f['a'] = 'Men had underestimated how many of their peers privately supported women working outside the home.'
for t in bank['themes']:
    if t['id'] == 'forecasting': t['principle'] = 'Forecasts improve with training, teaming and scoring, and fail through overconfidence and planning optimism. Who is in a group matters more than equal turn-taking.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
for i, f in enumerate(C['dimant-contagion-multi']['follow']):
    if f['q'] == 'Does closeness always make things worse?':
        C['dimant-contagion-multi']['follow'][i] = {'q': 'How was closeness varied?', 'a': 'By how socially close participants were to the peers whose earlier choices they saw.'}
C['genai2']['explain'] = 'Editing the prompt and choosing the best of three outputs reached 52.7% agreement, above the human-written originals and well above unedited GPT-3.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('contagion')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
s20 = C['social20']
s20['scene'] = 'Two departments report the same average rating of how acceptable a practice is. You suspect their norms still differ.'
s20['options'] = ['Ask each team’s manager to describe the norm', 'Compare how often each team breaks the rule', 'Collect each person’s view and look at the spread', 'Survey a larger sample and compare averages again']
s20['answer'] = 2
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('social20')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
C['social20']['options'] = ['Ask each team’s manager to describe the norm', 'Collect each person’s view and look at the spread', 'Compare how often each team breaks the rule', 'Survey a larger sample and compare averages again']; C['social20']['answer'] = 1
C['social13']['options'] = ['Large gains, mostly in final rounds', 'No effect, though estimates were noisy', 'Unfavorable to women, mostly in early rounds', 'Favorable to women, some with large standard errors']; C['social13']['answer'] = 3
g = C['genai2']['follow']
g[1]['a'] = 'Nearly. Editing the prompt alone brought it level with the originals; the small remaining difference was not statistically significant.'
g[2] = {'q': 'How much did curation matter?', 'a': 'Picking the best of three drafts added agreement beyond what prompt editing alone achieved.'}
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('order')
# --- minor 5: scope lines say what each study covers
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
B = {
 'biz03': 'Field studies in one US hotel; later replications found smaller effects, with the norm sign sometimes matching a plain environmental sign.',
 'axb01': 'Covers experiments published January 2020 to June 2023 across very different tasks; the averages describe that range of tasks.',
 'axb03': 'Policy simulations on past bail cases; crime outcomes exist only for released defendants.',
 'axb04': 'Studies of clinical and behavioral prediction up to 2000 using statistical formulas; many studies showed ties.',
 'axb12': 'One field test of how STEM career ads were delivered, with the same pattern on other major platforms.',
 'axb13': 'One firm’s customer-support chat operation, with a staggered rollout across agents.',
 'bz01': 'Fifteen US Facebook campaigns; observational methods both over- and underestimated lift across campaigns.',
 'bz03': 'Early company implementations with employees who chose to join.',
 'bz10': 'Large variance between studies: overload appears in some settings and is absent in others.',
 'bz11': 'Tests one form-design nudge on experimental self-reports.',
 'bz16': 'Combines hypothetical allocation tasks with plan-level data; investors differ in how evenly they split.',
 'lies-in-disguise': 'One-shot lab die task; the shares are inferred from the distribution of reports.',
 'rule-violations-honesty': '2,568 students in 23 countries; a cross-society correlation with a country index measured years earlier.',
 'false-news-spread': 'Twitter from 2006 to 2017, with stories verified by fact-checkers; it describes how true and false stories diffused.',
 'forecast-teams-rank': 'Geopolitical questions scored with Brier scores, with volunteers in one tournament; the paper reports test statistics.',
 'forecast-training': 'Geopolitical forecasts by tournament volunteers; the paper reports significance tests for the training effect.',
 'dimant-opioid-forecast': 'US veterans in one cash buyback program for opioid pills; the cards came on top of the cash incentive.',
 'axe01': 'Consumer experiments on recommendations, measuring how competent people judged AI and human recommenders.',
 'axe06': 'Developers at three firms; single experiments were noisy and varied, and the outcome is completed tasks.',
 'axe13': 'Short ChatGPT prompts with minimal profile data, measuring stated willingness to pay.',
 'genai1': 'Artists who chose to adopt AI on one platform; favorites measure peer reactions.'}
for k, v in B.items():
    if k in C: C[k]['boundary'] = v
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('scope')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
C['misperceived-norms-action']['boundary'] = 'One city and one cohort of married men; employment itself rose from 7.4% to 9.4%, a difference within statistical noise.'
C['meta-perception-causal']['boundary'] = 'Found in competitive contexts; at an exploratory one-week follow-up the correction had faded.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('scope2')
