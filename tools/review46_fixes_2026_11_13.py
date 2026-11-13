"""Review 46 fixes (iteration 74): a broken sentence in dimant-motivated-estimate (m-11); review 49: novelty named in the false-news explain (m-11, verbatim quote already in evidence.json), the counting rule stated in the repro-msci question (m-8). Idempotent. Wording only; no number changes."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}

def swap(obj, key, old, new):
    if new in obj[key]: return
    assert old in obj[key], (key, old); obj[key] = obj[key].replace(old, new)

swap(C['dimant-motivated-estimate'], 'explain', 'a self-serving tilt in which sources they consulted.', 'a self-serving tilt in the sources they consulted.')
swap(C['false-news-spread'], 'explain', 'so humans drove the gap.', 'so humans drove the gap; false news was also more novel than true news.')
swap(C['repro-msci-estimate'], 'question', 'Of all articles published under the new policy, what share could be at least largely reproduced?', 'Of all articles under the new policy, what share could be at least largely reproduced, counting inaccessible data as not reproduced?')
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
