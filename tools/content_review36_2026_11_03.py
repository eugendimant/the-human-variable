"""Review 36 content fixes. Idempotent; edits by text, never by index. Keyed options are pinned by hand only (I11)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}

# m3: the key is the one arm that beat human-human debates by a clear margin; the question asks exactly that
C['axb08']['question'] = C['axb08']['question'].replace('Which opponent shifted agreement most?', 'Which opponent clearly beat human-human debates at shifting agreement?')

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
print('review 36 content applied')
