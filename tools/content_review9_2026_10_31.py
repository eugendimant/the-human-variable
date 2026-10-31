"""Fixes from independent review 9 (2026-10-31). Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
s20 = C['social20']
s20['question'] = 'How do you check whether their norms differ?'
s20['options'] = ['Ask each team’s manager to describe the norm', 'Ask each person what they think colleagues believe', 'Compare how often each team breaks the rule', 'Survey a larger sample and compare averages']
C['social04']['question'] = 'What did students report?'
a = C['axe12']
a['scene'] = 'An HR audit finds employees who say they use AI get lower peer ratings. Experiments then held the work itself constant.'
a['question'] = 'What explains the lower ratings?'
a['options'] = ['AI users’ work was simply weaker', 'The penalty came mainly from managers who use AI', 'AI use was penalized even for identical work', 'Raters could tell which work used AI']
a['answer'] = 2
s1 = C['social01']
s1['options'][s1['options'].index('The spread of others’ behavior shaped choices, not just its mean')] = 'The spread of behavior shaped choices'
C['biz07']['options'] = [o if o != 'Assigning a new owner to the process' else 'Automating an existing step' for o in C['biz07']['options']]
m = C['meta-perception-causal']
m['options'] = [o if len(o) < 52 else o for o in m['options']]
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
