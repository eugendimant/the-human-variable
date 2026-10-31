"""Replace templated follow-ups on 31 legacy items with grounded, specific ones (agent draft, checked), plus sharper scope and action lines."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
ev = json.loads((ROOT / 'src/evidence.json').read_text())
out = json.loads(Path(sys.argv[1]).read_text())
# ai12: drop a follow-up that cites a commentary outside the lab's sources; use the paper's own mechanism.
out['ai12']['follow'][2] = {'q': 'What drives the resistance?', 'a': 'Uniqueness neglect: the worry that an AI provider cannot account for a person’s unique characteristics and circumstances as well as a human provider can.'}
for cid, o in out.items():
    c = C[cid]; c['follow'] = o['follow']
    for k in ('implication', 'boundary', 'study'):
        if o.get(k): c[k] = o[k]
    if o.get('evidence'): ev[cid] = ev.get(cid, []) + o['evidence']
for c in C.values():
    if c['format'] == 'multi': c.pop('answer', None)
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'docs/audit/legacy_followups_2026-10-31.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(len(out), 'items updated')
