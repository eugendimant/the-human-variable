"""Review 56 (m-8, m-9): option cues in four items and two title cues. Idempotent; the pinned options are updated here too."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; kp = ROOT / 'tests/keyed_options.json'
B = json.loads(bp.read_text()); K = json.loads(kp.read_text())
def swap(c, old, new):
    c['options'] = [new if o == old else o for o in c['options']]
    k = K.get(c['id'])
    if k: k['options'] = sorted(new if o == old else o for o in k['options']) if k['options'] == sorted(k['options']) else [new if o == old else o for o in k['options']]
for c in B['challenges']:
    i = c['id']
    if i == 'meta-perception-causal': swap(c, 'The same bias appeared in a national sample', 'A survey tracked the same partisans over several months')
    if i == 'biz07': swap(c, 'Automating an existing step', 'Replacing a step with a different one')
    if i == 'axb12': swap(c, 'Women scrolled past the ads more often', 'Advertisers bid less to reach women')
    if i == 'bz06': c['scene'] = c['scene'].replace(' Plott and Zeiler reran the design with training, practice rounds and anonymous offers.', ' Plott and Zeiler reran the design.')
    if i == 'dimant-contagion-multi': c['title'] = 'Peers and behavior'
    if i == 'biz08': c['title'] = 'A second task'
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
