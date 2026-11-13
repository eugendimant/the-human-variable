"""Review 46 fixes (iteration 74): a broken sentence in dimant-motivated-estimate (m-11); review 49: novelty named in the false-news explain (m-11, verbatim quote already in evidence.json), the counting rule stated in the repro-msci question (m-8). Idempotent. Wording only; no number changes."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}

def swap(obj, key, old, new):
    if new in obj[key]: return
    assert old in obj[key], (key, old); obj[key] = obj[key].replace(old, new)

swap(C['dimant-motivated-estimate'], 'explain', 'a self-serving tilt in which sources they consulted.', 'a self-serving tilt in the sources they consulted.')
# review 50 (I-2): the explain keeps its wording (the novelty finding is the follow-up "Why might people share falsehoods more?"); the key states only what the paper measured.
if 'so humans drove the gap; false news was also more novel than true news.' in C['false-news-spread']['explain']:
    swap(C['false-news-spread'], 'explain', 'so humans drove the gap; false news was also more novel than true news.', 'so humans drove the gap.')
OLD_KEY, NEW_KEY = 'Novel false stories drew more human shares', 'False stories were more novel, and humans spread them'
fo = C['false-news-spread']
fo['options'] = [NEW_KEY if o == OLD_KEY else o for o in fo['options']]
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())
k = K['false-news-spread']; k['keyed'] = [NEW_KEY if o == OLD_KEY else o for o in k['keyed']]; k['options'] = [NEW_KEY if o == OLD_KEY else o for o in k['options']]
kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
# review 50 (I-1): the counting rule moves from the question (a 6-line heading at 1280x720) to the scene.
if 'counting inaccessible data as not reproduced' in C['repro-msci-estimate']['question']:
    C['repro-msci-estimate']['question'] = 'Of all articles published under the new policy, what share could be at least largely reproduced?'
swap(C['repro-msci-estimate'], 'scene', 'requires authors to disclose both.', 'requires authors to disclose both. Articles whose data the reviewers could not access count as not reproduced.')
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
