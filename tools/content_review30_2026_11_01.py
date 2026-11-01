"""Review 30 and audit 38 content fixes. Idempotent; edits by text, never by index."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}

def swap(cid, old, new):
    o = C[cid]['options']
    if old in o: o[o.index(old)] = new

# audit 38, m2: false in both periods (above-average homes cut use)
swap('biz05', 'Above-average homes did not change their usage', 'Above-average homes raised their usage')
# audit 38, m5: the question no longer restates the scene
C['social13']['question'] = C['social13']['question'].replace('Orchestras put candidates behind a screen. ', '')
# review 30, m8: the chart shows the comparison the headline makes in money (closeness stays in the text)
ch = C['social15']['chart']
if len(ch['labels']) == 4:
    ch['labels'] = ['Given to allies', 'Given to a painting group-mate']; ch['values'] = [14.97, 13.54]; ch['highlight'] = 0
    ch['note'] = 'Share of the endowment given; allies got no more than a group-mate who shared only a painting preference.'
# review 30, m9: the explanation says what set the political divide apart, in the paper's terms
c = C['dimant-hate-choice']
c['explain'] = c['explain'].replace('Expectations differed: people predicted opponents would contribute less.',
    'What set the political divide apart was expectation: people expected less from opponents, and Dimant traces the gap to these beliefs rather than to preferences.')
# review 30, m10: the key names the family of forcing designs the paper analyses together
swap('axb10', 'Making users answer before seeing the AI', 'Engaging users before the AI answers')
swap('axb10', 'Making users engage before the AI’s answer appears', 'Engaging users before the AI answers')   # audit 39: not the longest option
# review 30, m11 and m12: implications stay honest
c = C['dimant-enforcers-rank']
c['implication'] = c['implication'].replace('When you build a speak-up channel, tell staff that most colleagues object to taking bribes;', 'When you build a speak-up channel and your own survey shows that most colleagues object to taking bribes, say so;')
c = C['axe01']
c['implication'] = c['implication'].replace('present taste-based picks as expert recommendations supported by AI.', 'where an expert actually reviews taste-based picks, present them as expert recommendations supported by AI.')
# review 30, m13: the two shortest options no longer solve a pick-two
swap('facebook-deactivation', 'Better factual news knowledge', 'Better news knowledge')
swap('social16', 'The norm nudge worked; the default did not', 'The default failed; norms worked')
swap('social16', 'Only the norm nudge worked', 'The default failed; norms worked')
swap('genai1', 'Output volume rose', 'Adopters’ output volume rose')
# review 30, optional 6: bz13's scope line says what the study covers
C['bz13']['boundary'] = C['bz13']['boundary'].replace('When workers clearly saw that higher-paid peers were more productive, pay gaps had no discernible effect.', 'One month of randomized daily pay among Indian manufacturing workers in production teams, including teams where coworkers’ productivity was easy to observe.')

# review 30, m5: meta-perception-causal's phone layout keeps the long Partisanship link clear of the Belief gap pill
PH = {'part': (70, 40), 'fix': (290, 40), 'meta': (250, 165), 'obs': (110, 290)}
for n in C['meta-perception-causal']['dag']['nodes']:
    if n['id'] in PH: n['px'], n['py'] = PH[n['id']]

ch = C['social15']['chart']; ch['note'] = ch['note'].replace('allies got no more than a group-mate', 'allies got about as much as a group-mate')   # audit 39: 14.97 against 13.54 is not "no more"
C['social15']['explain'] = C['social15']['explain'].replace('yet gave allies no more money (14.97% versus 13.54%)', 'yet gave allies about the same (14.97% versus 13.54%)')

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())
for c in B['challenges']:
    if c['id'] in K and c.get('options'):
        K[c['id']] = {'keyed': sorted(c['options'][i] for i in (c['multiAnswers'] if c['format'] == 'multi' else [c['answer']])), 'options': sorted(c['options'])}
kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('review 30 content applied')
