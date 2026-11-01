"""Review 27 content fixes. Idempotent; edits by text, never by index."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}

# m6: axb02 is a choice item; the rank-format leftover goes
C['axb02']['explain'] = C['axb02']['explain'].replace('The two adjustable groups did not differ meaningfully, so their order is not scored.', 'The adjustable groups (68% to 71%) did not differ meaningfully.')
# m8: one scale: No AI is the baseline the other four are measured from
rv = C['axf05']['rankValues']
if '73.0%' in rv: rv[rv.index('73.0%')] = 'Baseline, 73.0%'
# m9: curly quotes like the rest of the game
c = C['dimant-notalie-causal']
for n in c['dag']['nodes']:
    if n['label'] == '"Most lie"': n['label'] = '“Most lie”'
c['implication'] = c['implication'].replace('"everyone games it"', '“everyone games it”')
# m10: the two delegate tasks are the meta-analysis's worked examples; say so where the player reads them
s = C['axb01']['scene']
if 'worked examples' not in s:
    C['axb01']['scene'] = s + ' The two tasks below are the worked examples the authors use to illustrate that pattern.'

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
print('review 27 content applied')

# m9 (RULE G): every straight double quote in player-facing text becomes a curly pair; evidence quotes stay verbatim
import re
B = json.loads(bp.read_text())
def curl(s):
    return re.sub(r'"([^"]*)"', '“\\1”', s) if s.count('"') % 2 == 0 else s
def fix(o, key=''):
    if isinstance(o, dict): return {k: (v if k in ('quote',) else fix(v, k)) for k, v in o.items()}
    if isinstance(o, list): return [fix(v, key) for v in o]
    if isinstance(o, str): return curl(o)
    return o
B['challenges'] = [fix(c) for c in B['challenges']]
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())
for c in B['challenges']:
    if c['id'] in K and c.get('options'):
        K[c['id']] = {'keyed': sorted(c['options'][i] for i in (c['multiAnswers'] if c['format'] == 'multi' else [c['answer']])), 'options': sorted(c['options'])}
kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('curly quotes applied')
