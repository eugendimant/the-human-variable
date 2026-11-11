"""Review 38 m10 and m12. Idempotent; edits by text."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}
# m10: one form for weight on advice (the paper defines it on a 0% to 100% scale)
C['ai10']['explain'] = C['ai10']['explain'].replace('Weight on advice averaged 0.45 when the advice was labeled algorithmic and 0.30 when labeled human, for identical advice.', 'Weight on advice, how far people moved toward it, averaged 45% when the advice was labeled algorithmic and 30% when labeled human, for identical advice.')
C['ai10']['explain'] = C['ai10']['explain'].replace('People moved 45% of the way toward the advice when it was labeled algorithmic and 30% when it was labeled human, for identical advice.', 'Weight on advice, how far people moved toward it, averaged 45% when the advice was labeled algorithmic and 30% when labeled human, for identical advice.')
# m12: the first-week figures come from the households measured that week
for f in C['biz05']['follow']:
    f['a'] = f['a'].replace('Below-average households that saw only the neighborhood average rose from 10.38 to 11.27 kWh per day in the first week, and stayed higher three weeks later.', 'Among the below-average households measured in the first week, those that saw only the neighborhood average rose from 10.38 to 11.27 kWh per day, and they stayed higher three weeks later.')
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
print('review 38c content applied')
