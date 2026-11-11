"""Review 38 m13: three decisions that were too easy. Idempotent; edits by text. social01 checked against the CESifo WP 10233 full text
(tight: choices centered on the mean; loose: larger variation; polarized: most prefer extreme actions; the mean is not the only relevant feature)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())

def setopts(cid, old_first, opts, keyed):
    c = C[cid]
    if sorted(c['options']) == sorted(opts): return   # already applied
    c['options'] = opts
    if c['format'] == 'multi': c['multiAnswers'] = [opts.index(k) for k in keyed]
    else: c['answer'] = opts.index(keyed[0])
    c.pop('permuted', None)
    K[cid] = {'keyed': sorted(keyed), 'options': sorted(opts)}   # pinned by hand, here, with the texts in view (I11)

# social01 (Dimant, Gelfand, Hochleitner & Sonderegger): the two keys are two distinct results; the scene no longer states the set-up as the answer
c = C['social01']
c['scene'] = 'People saw how a group had behaved in a contribution game before choosing their own contribution. The group’s average was held fixed; only its shape changed: tightly clustered, widely spread, or split between the two extremes.'
setopts('social01', 'Loose norms generated more behavioral variation',
        ['After a tight norm, choices clustered close to the average', 'After a polarized norm, most people chose extreme contributions', 'After a polarized norm, most people chose the middle contribution', 'Choices matched whenever the group average was the same, whatever its shape'],
        ['After a tight norm, choices clustered close to the average', 'After a polarized norm, most people chose extreme contributions'])
c['answerTitle'] = 'The shape of others’ behavior changed choices'
if 'polarized norm, most people' not in c['explain']: c['explain'] = c['explain'].rstrip() + ' After a polarized norm, most people chose extreme contributions.'

# social13 (Goldin & Rouse): the options differ in the finding, not in a hedge
setopts('social13', 'About 50% likelier to advance from some rounds; several estimates imprecise',
        ['About 50% likelier to advance from certain preliminary rounds', 'About 5% likelier to advance from preliminary rounds', 'No change in who advanced', 'Less likely to advance once screened'],
        ['About 50% likelier to advance from certain preliminary rounds'])
C['social13']['answerTitle'] = 'About 50% likelier to advance from certain early rounds'

# bz11 (Kristal et al.): the claim no longer telegraphs the twist; the truth is unchanged in the explanation
f = C['bz11']['forecast']
if f['truth'] is True:
    f['claim'] = 'A preregistered direct replication again found fewer dishonest reports when people signed first.'; f['truth'] = False

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('review 38b content applied')
