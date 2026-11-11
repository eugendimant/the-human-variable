"""Review 38 content fixes. Idempotent; edits by text."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}
# m11: the two medians and the model-adjusted difference are different statistics
for f in C['axf06']['follow']:
    f['a'] = f['a'].replace('(a difference of −82 seconds, not statistically significant)', '(a model-adjusted difference of −82 seconds, not statistically significant)')
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
print('review 38 content applied')
