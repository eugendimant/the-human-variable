"""Review 39: social01 no longer answers its path sibling; social13's distractors are false for the rounds asked about. Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())
ep = ROOT / 'src/evidence.json'; E = json.loads(ep.read_text())

def setopts(cid, opts, keyed):
    c = C[cid]
    if sorted(c['options']) == sorted(opts): return
    c['options'] = opts
    if c['format'] == 'multi': c['multiAnswers'] = [opts.index(k) for k in keyed]
    else: c['answer'] = opts.index(keyed[0])
    c.pop('permuted', None)
    K[cid] = {'keyed': sorted(keyed), 'options': sorted(opts)}   # pinned by hand, with the texts in view (I11)

# social01: tight-versus-loose and the level of the average; the polarized result stays with dimant-polarizednorms-choice (next in the path)
c = C['social01']
c['scene'] = 'People saw how a group had behaved in a contribution game before choosing their own contribution. The researchers varied the group’s average and how tightly its choices clustered around that average.'
setopts('social01', ['After a tight norm, choices clustered close to the average', 'A higher group average raised contributions', 'After a loose norm, choices clustered more closely than after a tight one', 'Choices matched whenever the group average was the same, whatever its spread'],
        ['After a tight norm, choices clustered close to the average', 'A higher group average raised contributions'])
c['explain'] = c['explain'].replace(' After a polarized norm, most people chose extreme contributions.', '')
if 'higher average' not in c['explain']: c['explain'] = c['explain'].rstrip() + ' People also contributed more when the group they saw had a higher average.'
q = 'Individuals contribute significantly more when the descriptive norm has a higher mean.'   # Result 4, read in the published article
E['social01'] = [x for x in E['social01'] if not x['quote'].startswith('Participants contribute significantly more')]
if not any(x['quote'] == q for x in E['social01']): E['social01'].append({'quote': q, 'location': 'Full text, author PDF (michelegelfand.com), Management Science 71(3), p. 2255', 'source': 'norms24'})

# social13: the question names the rounds, so no distractor is true for another round
c = C['social13']
c['question'] = 'What did the authors estimate for women in certain preliminary rounds?'
setopts('social13', ['About 50% likelier to advance', 'About 5% likelier to advance', 'No change in who advanced', 'About 50% less likely to advance'], ['About 50% likelier to advance'])

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(E, ensure_ascii=False, indent=1) + '\n')
print('review 39 content applied')
