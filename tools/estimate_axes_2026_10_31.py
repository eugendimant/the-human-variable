"""Review 8, M2: spread estimate targets along their axes so no fixed slider position pays.
Only effect-size axes (changes, gains, drops) are moved; shares of people keep 0-100. Deterministic search; idempotent."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from server import scoring
bank = json.loads((ROOT / 'src/bank.json').read_text()); S = bank['sources']
E = [c for c in bank['challenges'] if c['format'] == 'estimate' and all(S[s]['verification']['status'] != 'quarantined' for s in c['sources'])]
CAP = {'axb03': 100, 'axb15': 100, 'dimant-proximity-estimate': 100, 'bz07': 100, 'ai01': 100, 'ai02': 100, 'axb04': 100, 'axe06': 150, 'axb14': 150, 'social12': 200, 'bz02': 500, 'bz03': 60}  # plausible ranges
MOVABLE = ['ai02', 'axb04', 'axb14', 'axb03', 'ai01', 'axb15', 'dimant-proximity-estimate', 'bz07', 'axe06', 'social12', 'bz02', 'bz03']
def mid_ok(c): e = c['estimate']; return scoring.score(c, (e['min'] + e['max']) / 2)['score'] <= 0.5
def pos_best(items):
    return max(sum(scoring.score(c, c['estimate']['min'] + f / 100 * (c['estimate']['max'] - c['estimate']['min']))['score'] for c in items) / len(items) for f in range(101))
def abs_best(items):
    return max(sum(scoring.score(c, min(max(x, c['estimate']['min']), c['estimate']['max']))['score'] for c in items) / len(items) for x in range(-50, 501))
by = {c['id']: c for c in E}
# shares near the top of 0-100 are precise numbers: a tighter band keeps a fixed high position from paying
for cid, tol in {'biz01': 5, 'judg05': 6, 'misperceived-norms-support': 5, 'axe05': 6, 'judg09': 5, 'truth-telling-gains': 7}.items():
    if cid in by: by[cid]['estimate']['tolerance'] = tol
for _ in range(3):
    for cid in MOVABLE:
        c = by.get(cid)
        if not c: continue
        e = c['estimate']; t = e['target']; best = None
        for mx in range(int(t // 5 + 2) * 5, CAP.get(cid, 100) + 1, 5):
            e['max'] = mx
            if not mid_ok(c): continue
            sc = pos_best(E)
            if best is None or sc < best[0] - 1e-9: best = (sc, mx)
        e['max'] = best[1]
print('best fixed position', round(pos_best(E), 3), 'best constant value', round(abs_best(E), 3))
for cid in MOVABLE:
    if cid in by: e = by[cid]['estimate']; print(cid, e['target'], e['min'], e['max'])
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
