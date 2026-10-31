"""Review 16, minor 9: verbatim quotes for social10's meta-analysis and dell26's sample. Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; p = ROOT / 'src/evidence.json'; ev = json.loads(p.read_text())
def add(cid, q):
    if not any(x.get('quote') == q['quote'] for x in ev.setdefault(cid, [])): ev[cid].append(q)
for q in ('We find strong support for a general factor of CI using meta-analytic methods in a dataset comprising 22 studies,',
          'The proportion of women in a group is a significant predictor of group performance, mediated by social perceptiveness.'):
    add('social10', {'source': 'riedl21', 'quote': q, 'location': 'Abstract, PNAS 118(21), version of record (Crossref)'})
for cid in ('axb14', 'rollout3'):
    ev[cid] = [x for x in ev.get(cid, []) if x.get('quote') != 'Preregistered field experiment with 758 BCG consultants']
    add(cid, {'source': 'dell26', 'quote': 'The preregistered experiment involved 758 knowledge workers.', 'location': 'Abstract, Organization Science, version of record (Crossref)'})
p.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n'); print('ok')
