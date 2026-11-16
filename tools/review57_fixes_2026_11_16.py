"""Review 57 (m-9): dimant-masks-forecast's explanation says only what the stored quotes say. Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text())
for c in B['challenges']:
    if c['id'] == 'dimant-masks-forecast':
        c['explain'] = 'Across 4,931 participants, there was no evidence that any of the 7 nudges promoted mask-wearing among Democrats or Republicans. Forecasters overestimated the effects in the pooled sample, and for Democrats too.'
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
