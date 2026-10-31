"""Review 15, m1: annotations stored as 'printed' are replaced by verbatim sentences or Table cells found in the papers
(docs/audit/evidence_numbers_r15_2026_10_31.json), and printed entries must name a Table or Figure. Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; p = ROOT / 'src/evidence.json'; ev = json.loads(p.read_text())
found = json.loads((ROOT / 'docs/audit/evidence_numbers_r15_2026_10_31.json').read_text())
live = {c['id'] for c in json.loads((ROOT / 'src/bank.json').read_text())['challenges']}
for k, qs in ev.items():
    if isinstance(qs, list) and k in live:
        ev[k] = [q for q in qs if not ('printed' in q and not re.search(r'Table|Fig', q.get('location', '') + q['printed']))]
for k, qs in found.items():
    if k.startswith('_'): continue
    for q in qs:
        key = 'quote' if 'quote' in q else 'printed'
        if not any(x.get(key) == q[key] for x in ev.setdefault(k, [])): ev[k].append(q)
# norms24: the sample size as printed in the paper's introduction (the PDF renders "=" as a replacement character)
q = {'source': 'norms24', 'quote': 'through the lens of a well-powered (n = 1,203) and preregistered study.', 'location': 'Introduction, Management Science 71(3), published article as hosted by the coauthor; "=" restored from a replacement character'}
if not any(x.get('quote') == q['quote'] for x in ev.setdefault('dimant-polarizednorms-choice', [])): ev['dimant-polarizednorms-choice'].append(q)
p.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n'); print('ok')
