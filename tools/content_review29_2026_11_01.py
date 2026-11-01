"""Review 29 content fixes. Idempotent; edits by text, never by index."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp, ep = ROOT / 'src/bank.json', ROOT / 'src/evidence.json'
B = json.loads(bp.read_text()); E = json.loads(ep.read_text()); C = {c['id']: c for c in B['challenges']}
PDF = 'Dimant, Gelfand, Hochleitner & Sonderegger, Management Science 71(3):2245-2263 (March 2025), published version, hosted by coauthor: https://www.michelegelfand.com/_files/ugd/6df109_20edd4d076c5479b8c7221bf8a8b7552.pdf'

# m3: the explanation states what the body reports, with its number (full text read, p. 2247 and pp. 2256-2257)
c = C['dimant-polarizednorms-choice']
c['explain'] = c['explain'].replace(
    'In the authors’ words, in polarized environments most individuals prefer extreme actions despite the strategic risk.',
    'Reactions concentrated at the extremes: people contributed a lot or very little. When most others gave zero and the rest gave the maximum of four, 46% still contributed more than the risk-free two.')
q = 'when confronted with a polarized descriptive norm, the participants’ reactions are concentrated at the extremes of the distribution: they either choose to contribute a lot or very little.'
if not any(x.get('quote') == q for x in E[c['id']]):
    E[c['id']].append({'source': 'norms24', 'quote': q, 'location': PDF + ' [Introduction, p. 2247]'})
q = 'a share p < 1/2 of the population contributes the maximum of four and a share 1 − p contributes zero.'
if not any(x.get('quote') == q for x in E[c['id']]):
    E[c['id']].append({'source': 'norms24', 'quote': q, 'location': PDF + ' [Section 5.1, p. 2256]'})
q = 'choosing a contribution of two allows eliminating all strategic risk'
if not any(x.get('quote') == q for x in E[c['id']]):
    E[c['id']].append({'source': 'norms24', 'quote': q, 'location': PDF + ' [Section 5.1, p. 2256]'})

# m4: biz05's third option no longer contradicts the keyed first; above-average homes cut use, so "did not change" is false
o = C['biz05']['options']
if 'Descriptive feedback alone kept low users steady' in o:
    o[o.index('Descriptive feedback alone kept low users steady')] = 'Above-average homes did not change their usage'

# m6: social13 asks for the decision-relevant estimate and how firm it is, not the authors' adjectives
c = C['social13']
c['question'] = 'Orchestras put candidates behind a screen. What did the authors estimate for women?'
c['options'] = ['About 50% likelier to advance from some rounds; several estimates imprecise',
                'About 50% likelier to advance, with precise estimates throughout',
                'Advancement unchanged by the screen',
                'Less likely to advance once screened']
c['answer'] = 0

# o3: experiments find, they do not predict
C['genai3']['question'] = C['genai3']['question'].replace('What does the experiment predict for labeled AI replies?', 'What did the experiment find for labeled AI replies?')

# m11: figures name their measure and their scope
ch = C['axe12']['chart']; ch['note'] = 'Mean laziness rating, higher means lazier; the three targets differ only in the help described. Values reported in Reif, Larrick & Soll 2025, Study 2.'
ch = C['social15']['chart']
ch['labels'] = ['Given to allies', 'Given to a painting group-mate', 'Given to a painting out-group', 'Taken from political opponents']
ch['note'] = 'Share of the endowment moved: given to the first three, taken from political opponents.'
C['bz08']['chart']['note'] = 'Late pickups per week at center 1, one of the six fined centers.'

# m7: bz12 asks which group the peer-pay disclosure moved; that is a pick-one, not a causal diagram
c = C['bz12']
if c['format'] == 'causal':
    c['format'] = 'choice'; c.pop('dag', None)

# m5: judg02 is quarantined (its source is not verified), so it is never served; it stays in the bank as the quarantine test's case.
# m2 / o2: ai01's tasks follow-up restated the scene; the study's second result (quality) gets the slot. rollout3 names its own term.
f = C['ai01']['follow']
for x in f:
    if x['q'] in ('What kind of tasks were they?', 'Did quality improve too?'):
        x['q'] = 'Did quality improve too?'; x['a'] = 'Yes. Graders rated the ChatGPT group’s work higher as well; how much higher is a separate decision in this game.'   # the figure itself is ai02's answer (sibling leak test)
f = C['rollout3']['follow']
if not any(x['q'] == 'What is the jagged frontier?' for x in f):
    f.append({'q': 'What is the jagged frontier?', 'a': 'The authors’ name for the uneven edge of what AI does well. Tasks that look alike can sit on either side of it: inside, GPT-4 made consultants faster and better; on the task just outside, those using GPT-4 reached the right answer less often.'})

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(E, ensure_ascii=False, indent=1) + '\n')
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())
for c in B['challenges']:
    if c['id'] in K and c.get('options'):
        K[c['id']] = {'keyed': sorted(c['options'][i] for i in (c['multiAnswers'] if c['format'] == 'multi' else [c['answer']])), 'options': sorted(c['options'])}
kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('review 29 content applied')
