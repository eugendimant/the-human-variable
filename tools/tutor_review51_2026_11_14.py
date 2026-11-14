"""Review 51 (m-1): four wrong tutor answers. Data only: one follow-up question reworded, two follow-ups added, one regex
alternative added to tutorRoutes.subgroupFollow. Idempotent. Run tools/tutor_golden.py after."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text())
T = B['tutorRoutes']
alt = r'|^did (experts?|experienced \w+|professionals?|novices?|women|men|older \w+|younger \w+) '
if alt not in T['subgroupFollow']: T['subgroupFollow'] += alt
C = {c['id']: c for c in B['challenges']}
for f in C['social04']['follow']:
    if f['q'] == 'Did beliefs change over time?': f['q'] = 'Did beliefs change later in the semester?'
fb = C['facebook-deactivation']['follow']
if not any(f['q'].startswith('How long did people stay off') for f in fb):
    fb.insert(1, {'q': 'How long did people stay off Facebook?', 'a': 'The deactivation lasted four weeks. The payment figure asks what people needed to be paid to deactivate for that long.'})
ax = C['axb01']['follow']
if not any(f['q'] == 'When does a human reviewer help?' for f in ax):
    ax.insert(1, {'q': 'When does a human reviewer help?', 'a': 'When the human was the better performer. Teams gained then, and lost when the AI was the better performer.'})
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
