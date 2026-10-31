"""Evidence figures for decisions that had none (drafted in docs/audit/draft_charts_2026_10_31.json; every value checked
against that decision's own evidence). Charts with bars below zero or a paraphrased source are left out. Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
draft = json.loads((ROOT / 'docs/audit/draft_charts_2026_10_31.json').read_text())
SKIP = {'_skipped', 'judg02', 'social15', 'opposing-views-bot', 'dimant-observability-choice', 'axf05'}
n = 0
for cid, ch in draft.items():
    if cid in SKIP or cid not in C or C[cid].get('chart'): continue
    if any(v < 0 for v in ch['values']): continue
    if ch.get('unit') not in ('%', '', '$'): ch['unit'] = ''
    C[cid]['chart'] = ch; n += 1
if 'axb02' in C and C['axb02'].get('chart'): C['axb02']['chart']['highlight'] = 1
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('charts added', n)
