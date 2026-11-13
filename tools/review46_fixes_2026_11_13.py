"""Review 46 fixes (iteration 74): a broken sentence in dimant-motivated-estimate (m-11). Idempotent. Wording only; no number changes."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}

def swap(obj, key, old, new):
    if new in obj[key]: return
    assert old in obj[key], (key, old); obj[key] = obj[key].replace(old, new)

swap(C['dimant-motivated-estimate'], 'explain', 'a self-serving tilt in which sources they consulted.', 'a self-serving tilt in the sources they consulted.')
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
