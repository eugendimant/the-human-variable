"""Review 32 content fixes. Idempotent; edits by text, never by index."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp, ep = ROOT / 'src/bank.json', ROOT / 'src/evidence.json'
B = json.loads(bp.read_text()); E = json.loads(ep.read_text()); C = {c['id']: c for c in B['challenges']}

def rep(cid, field, old, new):
    c = C[cid]; c[field] = c[field].replace(old, new)
def frep(cid, old, new):
    for f in C[cid]['follow']: f['a'] = f['a'].replace(old, new)

# m1: bz16's false claim is about size, not direction ("not very sensitive" is weak, not zero)
C['bz16']['forecast']['claim'] = C['bz16']['forecast']['claim'].replace('In real plans, more equity funds on the menu meant more money in equity.', 'In real plans, the share put into equity rose roughly in step with the share of equity funds offered.')
# m2: statistical notation leaves player text; the Source tab carries the statistics
rep('social16', 'explain', 'The ally-opponent difference stayed highly significant (p < 0.001).', 'The ally-opponent difference stayed statistically reliable.')
rep('social16', 'explain', 'The ally-opponent difference stayed large and statistically reliable.', 'The ally-opponent difference stayed statistically reliable.')   # audit 43: the quote says nothing about size
rep('axb01', 'explain', 'Across 370 effect sizes, human-AI teams did worse than the best performer alone (g = −0.23). They gained when humans beat the AI (g = 0.46) and lost when the AI was better (g = −0.54).',
    'Across 370 effect sizes, human-AI teams did worse on average than the better of the human or the AI working alone. They gained when the human was the better performer and lost when the AI was.')
frep('axb01', 'Yes. Against humans alone, human-AI systems performed better (g = 0.64).', 'Yes. Against humans alone, human-AI systems performed better on average.')
frep('axb01', 'Decision tasks, where people choose from a fixed set of options, showed losses (g = −0.27). Creation tasks trended positive (g = 0.19, not significant).', 'Decision tasks, where people choose from a fixed set of options, showed losses. Creation tasks trended positive, though not reliably.')
frep('axb08', '(−15.7%, P = 0.38)', '(−15.7%, not statistically significant)')
rep('bz10', 'explain', 'found a mean effect size of virtually zero (D = 0.02), with considerable variance between studies.', 'found an average effect of virtually zero, with considerable variance between studies.')
rep('bz13', 'answerTitle', 'Output fell 0.45 SD;', 'Output fell 0.45 standard deviations;')
rep('accuracy-prompt', 'explain', 'More than 80% of 192 robustness analyses gave P < 0.05.', 'The result held in more than 80% of 192 robustness analyses.')
frep('misperceived-norms-action', 'Not significantly: current outside-the-home employment rose from 7.4% to 9.4% (p = 0.235).', 'Not reliably: current outside-the-home employment rose from 7.4% to 9.4%, a difference that was not statistically significant.')
frep('dimant-masks-forecast', 'Predicted and observed effects for Democrats were negatively correlated (r = −0.63, p = 0.0003).', 'Messages forecasters expected to work best for Democrats tended to do worst (a correlation of −0.63, statistically significant).')
frep('dimant-masks-forecast', 'Predicted and observed effects for Democrats ran in opposite directions, with a correlation of −0.63.', 'Messages forecasters expected to work best for Democrats tended to do worst (a correlation of −0.63, statistically significant).')   # audit 43: a negative correlation is not opposite signs
frep('dimant-enforcers-rank', 'vs 43.6% for lies that achieved equity (P < 0.001).', 'vs 43.6% for lies that achieved equity, a reliable difference.')
rep('axe06', 'explain', 'raised completed tasks by 26.08% (standard error 10.3%).', 'raised completed tasks by 26.08%.')
frep('axe11', 'P = 0.0032; the authors call the effect small.', 'a difference the authors call small.')
rep('axf02', 'explain', 'Scientists’ predictions did not track the results (r = 0.03)', 'Scientists’ predictions were essentially unrelated to the results (a correlation of 0.03)')
rep('axf02', 'answerTitle', 'Scientists’ predictions missed: r = 0.03', 'Scientists’ predictions missed the results')
frep('axf02', '(r = 0.60)', '(a correlation of 0.60)')
rep('axf06', 'explain', ', a difference that was not statistically significant (P = .60).', ', a difference that was not statistically significant.')
frep('axf06', '(difference −82 seconds, P = .20)', '(a difference of −82 seconds, not statistically significant)')
rep('manylabs-anchoring', 'explain', 'found anchoring effects of d = 1.27 to 2.60 on four estimation questions, against an overall 0.93 in the original study.', 'found large anchoring effects on four estimation questions, with standardized sizes of 1.27 to 2.60 against an overall 0.93 in the original study.')
frep('manylabs-anchoring', 'From d = 1.27 for distance to New York to d = 2.60 for babies born, against an overall 0.93 in the original study.', 'Standardized sizes ran from 1.27 for distance to New York to 2.60 for babies born, against an overall 0.93 in the original study.')
rep('social13', 'explain', 'Some estimates have large standard errors.', 'Some estimates are imprecise.')
frep('social13', 'some estimates have large standard errors', 'some estimates are imprecise')
# m3: a journal running header spliced into a quote
for k in E: E[k] = [q for q in E[k] if 'INFORMS' not in q.get('quote', '')]   # the same header sat in two items (RULE G)
# m4: rollout3 prints the number as quoted
rep('rollout3', 'explain', '60.0% with GPT-4 plus a prompt overview', '60% with GPT-4 plus a prompt overview')
for t in C['rollout3'].get('delegate', {}).get('tasks', []):
    if t.get('why'): t['why'] = t['why'].replace('60.0%', '60%')   # audit 43: the task note too
# m5: civic-wallet-rank's scope line names no critique it does not source
rep('civic-wallet-rank', 'boundary', ', a measure later questioned for cross-country rankings.', '.')
# m11: axe12's title states the measure; the citation lives in the source line; values keep their printed decimals
ch = C['axe12']['chart']; ch['note'] = 'Mean laziness rating; higher means lazier, and the three targets differ only in the help described.'; ch['decimals'] = 2
# m12: judg05's amber bar is the headline's 78% (share choosing the gamble, by frame)
ch = C['judg05']['chart']
if ch['labels'][0].startswith('Sure option'):
    ch['labels'] = ['Gamble, lives-saved frame', 'Gamble, deaths frame']; ch['values'] = [28, 78]; ch['highlight'] = 1; ch['note'] = 'Share choosing the gamble, by frame.'

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(E, ensure_ascii=False, indent=1) + '\n')
print('review 32 content applied')
