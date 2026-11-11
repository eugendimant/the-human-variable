"""Review 40 content fixes. Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())
# I-4: the rating scale's ends are not in the stored quotes, so no axis is invented; bars from zero on a round scale
C['axe12']['chart'].pop('axis', None)
# I-5: the same measure on one scale in consecutive path decisions
for cid in ('social01', 'dimant-polarizednorms-choice'):
    if 'chart' in C[cid]: C[cid]['chart']['max'] = 3
# I-8: the distractor answers the question asked
c = C['dimant-conspiracy-choice']
old, new = 'Sharing stayed flat across rounds, whatever feedback the posts earned', 'Habit: sharing did not respond to the feedback posts earned'
if old in c['options']:
    c['options'][c['options'].index(old)] = new
    K['dimant-conspiracy-choice'] = {'keyed': [c['options'][c['answer']]], 'options': sorted(c['options'])}
# dimant-deviant-choice: the manager line follows the finding (the normative message helps where compliance is cheap)
C['dimant-deviant-choice']['implication'] = C['dimant-deviant-choice']['implication'].replace('When a sanction is modest and compliance is costly, do not justify it with “everyone complies”; explain why the rule is right.', 'Where compliance is costly, do not back a modest sanction with “everyone complies”. Where it is cheap, pair the sanction with why the rule is right.')
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('review 40 content applied')
