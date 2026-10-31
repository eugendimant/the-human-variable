"""Fixes from independent review 16 (2026-10-31). Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
# minor 1: claim wording no longer predicts truth (positive claims resolve both ways, as do negative ones)
F = {
 'axe07': 'People were more willing to use the best algorithm in more predictable domains.',
 'axb06': 'Hires made against the test’s recommendation more often turned out worse.',
 'social08': 'The behavior spread farther through clustered networks with redundant ties than through networks with random long ties.',
}
for k, claim in F.items(): C[k]['forecast'] = {'claim': claim, 'truth': True}
# minor 2
C['axe10']['answerTitle'] = 'No: AI images won by up to 50%'
# minor 3
C['dimant-hate-choice']['explain'] = C['dimant-hate-choice']['explain'].replace('dropped no more for a Trump opponent (72.8% to 59.0%) than for a painting-preference outgroup (73.2% to 62.4%)', 'dropped by a similar amount for a Trump opponent (72.8% to 59.0%) and for a painting-preference outgroup (73.2% to 62.4%)')
# minor 6 and 8: scenes describe the real designs
C['biz07']['scene'] = 'In experiments, people were asked to improve things such as a Lego structure, a mini-golf hole or a written essay, and could change them by adding or by removing elements.'
C['biz08']['scene'] = 'In one experiment, people improved a pattern on a grid; some did it while keeping track of a second task at the same time.'
C['overconfidence-hard-task']['scene'] = 'In a lab study, 82 students took a hard trivia quiz. Before scores came out, each estimated their own score and their rank among the others.'
c = C['axe12']; c['scene'] = 'In a series of experiments, people evaluated workers, some of them described as getting help from AI.'
c['options'] = [{'AI use was penalized even for identical work': 'Raters saw AI users as lazier'}.get(o, o) for o in c['options']]
# minor 7: no cross-item answer in a follow-up
for f in C['genai3']['follow']:
    if f['q'] == 'What about colleagues who use AI?': f['a'] = 'How colleagues judge people who use AI is a separate decision in the lab (Reif et al. 2025).'
# minor 10: aversion and appreciation items say how their designs differ
R = {'q': 'Why do other studies find people prefer algorithms?', 'a': 'Designs differ. Here people watched the model make errors before choosing; in Logg, Minson and Moore (2019) people weighed advice labeled as an algorithm’s without seeing it fail, and leaned on it more.'}
if not any(f['q'] == R['q'] for f in C['ai09']['follow']): C['ai09']['follow'].append(R)
# minor 12: rank items that scored one or two pairs become plain calls
c = C['axb02']
if c['format'] == 'rank':
    for k in ('rankAnswer', 'rankTies', 'rankValues', 'rankLabel', 'permuted'): c.pop(k, None)
    c['format'] = 'choice'; c['question'] = 'Which group chose to use the model least often?'; c['answer'] = c['options'].index('Could not change the model at all')
c = C['bz15']
if c['format'] == 'rank':
    for k in ('rankAnswer', 'rankTies', 'rankValues', 'rankLabel', 'permuted'): c.pop(k, None)
    c['format'] = 'choice'; c['question'] = 'Which form produced the fewest donors?'; c['answer'] = c['options'].index('Opt-in (default: not a donor)')
# minor 13: consumer-credit caveat
C['bz09']['implication'] = 'Test creative content against price in randomized offers before giving up margin on discounts, and review creative for fairness: in consumer credit, imagery that sways borrowers raises consumer-protection questions.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
C['social13']['options'] = [{'Clear gains, precisely estimated in every round': 'Clear gains, precisely estimated across rounds'}.get(o, o) for o in C['social13']['options']]
C['dimant-conspiracy-choice']['options'] = [{'A hunch that the posts might be true after all': 'A hunch that the posts might be true'}.get(o, o) for o in C['dimant-conspiracy-choice']['options']]
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok2')
