"""Review 52 (m-8): axb12's scene no longer names the delivery mechanism ("cost-effectively"). Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text())
for c in B['challenges']:
    if c['id'] == 'axb12': c['scene'] = c['scene'].replace(' deliver it cost-effectively.', ' deliver it.')
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
