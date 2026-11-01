"""Review 28 content fixes. Idempotent; edits by text, never by index."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp, ep = ROOT / 'src/bank.json', ROOT / 'src/evidence.json'
B = json.loads(bp.read_text()); E = json.loads(ep.read_text()); C = {c['id']: c for c in B['challenges']}

# m11: rollout3's scene no longer points at the task outside the frontier
C['rollout3']['scene'] = C['rollout3']['scene'].replace('a brand recommendation that hinges on details buried in interview notes', 'picking the brand to grow from interview notes and spreadsheets')
# m10: social20 asks for a method, not a prediction; it leaves play (the paper stays in the Library through its other decisions)
C['social20']['retired'] = True
C['social20']['retiredReason'] = 'Review 28: the question asks for the paper’s method, so there is no result to predict.'
# m8: the contagion follow-up names the later study without a year it cannot cite
f = C['dimant-contagion-multi']['follow'][3]
for old in ('Does the 2022 proximity study say the same?', 'Does the later proximity study say the same?'): f['q'] = f['q'].replace(old, 'Does the shared-identity study say the same?')
for old in ('The 2022 study varied', 'The later study varied'): f['a'] = f['a'].replace(old, 'The shared-identity study varied')   # no word the duration route reads as time
E['dimant-contagion-multi'] = [q for q in E['dimant-contagion-multi'] if q.get('quote') != 'Games and Economic Behavior 132 (2022) 59–72']
for q in E['genai3']:
    if q.get('location', '').startswith('Abstract (5.'):
        q['location'] = 'Abstract (the statement); the values ' + q['location'][len('Abstract '):] + ' are from Table 1'
E['social01'] = [q for q in E['social01'] if '1,200U.S.' not in q.get('quote', '')]
# m7: curly apostrophes in player text (evidence quotes stay verbatim)
def curl(s): return re.sub(r"(?<![\w])'([^']+)'(?![\w])", '\u2018\\1\u2019', re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=\s|$|[,.;:])", '\u2019', s))
def fix(o):
    if isinstance(o, dict): return {k: (v if k == 'quote' else fix(v)) for k, v in o.items()}
    if isinstance(o, list): return [fix(v) for v in o]
    return curl(o) if isinstance(o, str) else o
B['challenges'] = [fix(c) for c in B['challenges']]
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(E, ensure_ascii=False, indent=1) + '\n')
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())
for c in B['challenges']:
    if c['id'] in K and c.get('options'):
        K[c['id']] = {'keyed': sorted(c['options'][i] for i in (c['multiAnswers'] if c['format'] == 'multi' else [c['answer']])), 'options': sorted(c['options'])}
kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('review 28 content applied')
