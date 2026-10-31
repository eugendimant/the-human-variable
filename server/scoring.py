"""Python mirror of src/scoring.js. tests/test_scoring_parity.py runs both on the same cases."""
from __future__ import annotations
import math

def _clamp(x, a, b): return min(b, max(a, x))

def score(c: dict, r) -> dict:
    f = c['format']
    if f in ('choice', 'causal'):
        ok = r == c['answer']; return {'score': 1.0 if ok else 0.0, 'correct': ok}
    if f == 'multi':
        s = set(r if isinstance(r, list) else []); hits = sum(1 for i in c['multiAnswers'] if i in s)
        return {'score': hits / len(c['multiAnswers']), 'correct': hits == len(c['multiAnswers']) and len(s) == len(c['multiAnswers'])}
    if f == 'estimate':
        e = c['estimate']; gap = abs(r - e['target'])
        sc = 1.0 if gap <= e['tolerance'] else _clamp(1 - (gap - e['tolerance']) / (2 * e['tolerance']), 0, 1)
        return {'score': sc, 'correct': gap <= e['tolerance']}
    if f == 'forecast':
        p = _clamp(float(r) / 100, 0, 1); t = 1 if c['forecast']['truth'] else 0; b = (p - t) ** 2
        return {'score': 1 - 2 * b, 'correct': (p > 0.5) == (t == 1) and p != 0.5}
    if f == 'rank':
        truth = c['rankAnswer']
        if not isinstance(r, list) or len(r) != len(truth): return {'score': 0.0, 'correct': False}
        pos = {v: i for i, v in enumerate(r)}; agree = total = 0
        ties = c.get('rankTies') or []
        for i in range(len(truth)):
            for j in range(i + 1, len(truth)):
                if any(truth[i] in g and truth[j] in g for g in ties): continue
                total += 1; agree += pos[truth[i]] < pos[truth[j]]
        sc = agree / total if total else 0.0; return {'score': sc, 'correct': sc == 1}
    if f == 'allocate':
        v = c['allocate']['values']; tot = sum(r or [])
        if not tot: return {'score': 0.0, 'correct': False}
        hi = max(v); best = [1 if x == hi else 0 for x in v]; nb = sum(best); p = [s / tot for s in r]
        sc = 1 - sum((x - best[i] / nb) ** 2 for i, x in enumerate(p)); top = max(p)
        return {'score': sc, 'correct': any(best[i] and x == top for i, x in enumerate(p))}
    if f == 'delegate':
        tasks = c['delegate']['tasks']; right = sum(1 for i, t in enumerate(tasks) if isinstance(r, list) and i < len(r) and r[i] == t['answer'])
        return {'score': right / len(tasks), 'correct': right == len(tasks)}
    raise ValueError('Unknown format ' + f)

def valid(c: dict, r) -> bool:
    """Server-side shape check for a submitted response."""
    f = c['format']; isint = lambda x: type(x) is int
    if f in ('choice', 'causal'): return isint(r) and 0 <= r < len(c['options'])
    if f == 'multi': return isinstance(r, list) and len(r) == len(c['multiAnswers']) and all(isint(x) and 0 <= x < len(c['options']) for x in r) and len(set(r)) == len(r)
    if f == 'estimate': return type(r) in (int, float) and math.isfinite(r) and c['estimate']['min'] <= r <= c['estimate']['max']
    if f == 'forecast': return type(r) in (int, float) and 0 <= r <= 100
    if f == 'rank': return isinstance(r, list) and sorted(r) == list(range(len(c['options']))) and all(isint(x) for x in r)
    if f == 'allocate': return isinstance(r, list) and len(r) == len(c['options']) and all(isint(x) and x >= 0 for x in r) and sum(r) == c['allocate']['total']
    if f == 'delegate': return isinstance(r, list) and len(r) == len(c['delegate']['tasks']) and all(isint(x) and 0 <= x < len(c['delegate']['choices']) for x in r)
    return False
