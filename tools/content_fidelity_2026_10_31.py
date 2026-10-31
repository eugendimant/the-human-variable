"""In-house design-fidelity audit (docs/audit/design_fidelity_2026_10_31.json): items now describe each study's
manipulation, outcome measure and population as the evidence states them. Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
audit = json.loads((ROOT / 'docs/audit/design_fidelity_2026_10_31.json').read_text())
EDIT = {   # where the proposal added detail the evidence file does not quote, the plainer version is used
 ('dimant-observability-choice', 'boundary'): 'Give-or-take charity games in the lab and online (n = 1,650), where a decision maker chose with or without a passive observer watching.',
 ('dimant-notalie-causal', 'scene'): 'In an incentivized experiment, people could misreport for money. Those who learned of this chance before stating what others do more often said most people lie, and more often reported winning.',
}
n = 0
for x in audit:
    cid, field = x['id'], x['field']; new = EDIT.get((cid, field), x['proposed_text'])
    c = C[cid]; m = re.fullmatch(r'follow\[(\d+)\]\.a', field)
    if m: c['follow'][int(m.group(1))]['a'] = new
    else: c[field] = new
    n += 1
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('applied', n)
