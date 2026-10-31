"""Review 3, M2: bank order must not carry the answer. Shuffle option order per item (seeded by id) and remap every index.

Idempotent: items already marked with 'permuted' are skipped. Display order is shuffled again per player or per room."""
import json, random
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text())
n_done = 0
for c in bank['challenges']:
    if c.get('permuted') or c['format'] not in ('choice', 'causal', 'multi', 'rank', 'allocate'): continue
    n = len(c['options']); r = random.Random('thv-' + c['id'])
    for _ in range(50):
        perm = list(range(n)); r.shuffle(perm)          # new position k holds old option perm[k]
        new = {old: k for k, old in enumerate(perm)}
        if c['format'] == 'rank' and [new[i] for i in c['rankAnswer']] == list(range(n)): continue
        if c['format'] in ('choice', 'causal') and new[c['answer']] == c['answer'] and n > 2 and _ < 49: continue
        break
    c['options'] = [c['options'][i] for i in perm]
    if 'answer' in c: c['answer'] = new[c['answer']]
    if 'multiAnswers' in c: c['multiAnswers'] = sorted(new[i] for i in c['multiAnswers'])
    if 'rankAnswer' in c: c['rankAnswer'] = [new[i] for i in c['rankAnswer']]
    if 'rankTies' in c: c['rankTies'] = [sorted(new[i] for i in t) for t in c['rankTies']]
    if 'rankValues' in c: c['rankValues'] = [c['rankValues'][i] for i in perm]
    if 'allocate' in c:
        for k in ('values', 'valueLabels'):
            if k in c['allocate']: c['allocate'][k] = [c['allocate'][k][i] for i in perm]
    c['permuted'] = True; n_done += 1
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('permuted', n_done)
