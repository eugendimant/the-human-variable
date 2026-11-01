"""Review 26 content fixes. Idempotent; options are edited by text, never by index."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp, ep, kp = ROOT / 'src/bank.json', ROOT / 'src/evidence.json', ROOT / 'tests/keyed_options.json'
B = json.loads(bp.read_text()); E = json.loads(ep.read_text()); K = json.loads(kp.read_text())
C = {c['id']: c for c in B['challenges']}

def swap(cid, old, new):
    c = C[cid]
    if new in c['options']: return
    c['options'][c['options'].index(old)] = new

# Minor 3 (I15): the projection rival is not refuted by the item's evidence; use one the 38.1% -> 62.7% shift refutes
swap('dimant-notalie-causal', 'People who planned to lie projected their own choice onto others', 'Beliefs about lying were fixed and the task did not move them')
# Minor 5: the scene no longer names the two kinds of change
C['biz07']['scene'] = 'In experiments, people were asked to improve things such as a Lego structure, a mini-golf hole or a written essay, and could change them however they liked.'
# Minor 6: key the mechanism, not a restatement of the question
swap('false-news-spread', 'People shared false stories more than true ones', 'Novel false stories drew more human shares')
# Minor 7: the headline states the finding
C['axe10']['answerTitle'] = 'An AI image beat the human one by up to 50%'

# Minor 4: the 11.99% sentence is in the published version (p. 10); quote it from there and drop the working-paper entry
full = ("The prosocial behavior toward one’s own political faction (14.97%, green bar in bottom-left panel) is indistinguishable from the behavior in MGP, "
        "regardless of whether their partners held the same (13.54%, green bar bottom-right panel, p = 0.78) or different (11.99%, red bar bottom-right panel, p = 0.56) painting preferences.")
ev = E['social15']
ev[:] = [q for q in ev if 'working-paper' not in q['location']]
if not any(q['quote'] == full for q in ev):
    ev.append({'source': 'hate23', 'quote': full, 'location': 'Dimant (2024), Management Science, published version (Articles in Advance PDF), author-hosted, p. 10, Section 3.1'})

for cid in ('dimant-notalie-causal', 'false-news-spread'):
    c = C[cid]
    K[cid] = {'keyed': sorted(c['options'][i] for i in (c['multiAnswers'] if c['format'] == 'multi' else [c['answer']])), 'options': sorted(c['options'])}

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(E, ensure_ascii=False, indent=1) + '\n'); kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('review 26 content applied')
