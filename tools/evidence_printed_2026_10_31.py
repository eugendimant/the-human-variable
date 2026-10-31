"""Review 14, minor 1: evidence entries are verbatim prose quotes ('quote') or values read from a table or figure ('printed').
Annotations (record ids, study labels, OCR notes) are not evidence and are removed. Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; p = ROOT / 'src/evidence.json'; ev = json.loads(p.read_text())
NOTE = re.compile(r'^(PubMed \d+|DOI:|Studies? \d[\w-]*$|Experiment \d\w*$|experiment \d$|Exps |Seven studies|OCR |continues:|publisher-supplied abstract|Economics Letters \d|\d+ recruited$|PMC\d+)', re.I)
dropped = moved = 0
for k, qs in ev.items():
    if not isinstance(qs, list): continue
    keep = []
    for q in qs:
        if 'quote' in q and NOTE.search(q['quote'].strip()): dropped += 1; continue
        if 'quote' in q and ('values as printed' in q.get('location', '') or re.match(r'(Table|Figure) \d', q['quote'])):
            q['printed'] = q.pop('quote'); moved += 1
        keep.append(q)
    ev[k] = keep
p.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n'); print('dropped', dropped, 'moved to printed', moved)
