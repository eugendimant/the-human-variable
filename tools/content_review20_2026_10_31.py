"""Review 20 content fixes (idempotent)."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
bp, ep = R / 'src/bank.json', R / 'src/evidence.json'
b = json.loads(bp.read_text()); ev = json.loads(ep.read_text())
C = {c['id']: c for c in b['challenges']}
# minor 2: the scene's control (74) must not land inside the target band (76)
C['axf06']['estimate']['tolerance'] = 1
# minor 3: no impossible negative half on the axis
for i in ('axb03', 'axb14'):
    C[i]['estimate'].update(min=0, max=40, tolerance=3)
# minor 8: the explanation must not carry a sample size the analysed result does not use
C['biz04']['explain'] = C['biz04']['explain'].replace('in the second (N = 204), ', 'in the second hotel, ')
# minor 9: the implication stays with what the study tested
C['opposing-views-bot']['implication'] = "Do not expect that feeding a divided team the other side's messages builds understanding."
# minor 11: a claim this specific reads as true; state it at the level of the finding
C['bz11']['forecast']['claim'] = 'The replications found no effect of signing first on honest reporting.'
# minor 7: store the bates17 finding the explanation relies on
q = {"source": "bates17", "quote": "Hypotheses that group-IQ increases with number of women in the group and with turn-taking were not supported.",
     "location": "Abstract, Intelligence (Bates & Gupta), published article PDF, doi:10.1016/j.intell.2016.11.004"}
for cid, c in C.items():
    if 'bates17' in c.get('sources', []) and not any(e.get('quote') == q['quote'] for e in ev.get(cid, [])):
        ev.setdefault(cid, []).append(q)
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
print('ok')
# own audit after review 20: judg05's scene value 72 sat inside the band 78 ± 6
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
C['judg05']['estimate']['tolerance'] = 5
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 21, minor 9: bz02's answer is a threshold, so it becomes a forecast; round axes for axb04 and axe04
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
z = C['bz02']
if z['format'] == 'estimate':
    z['format'] = 'forecast'; z.pop('estimate', None)
    z['question'] = 'How likely is it that the study found this?'
    z['forecast'] = {'claim': 'In the median experiment, the confidence interval on return on investment was narrower than 50 percentage points.', 'truth': False}
C['axb04']['estimate'].update(min=0, max=60)
C['axe04']['estimate'].update(min=0, max=60)
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 21, minor 3: key the polarized-norms item on the printed variance, and attribute the abstract's "most" to the authors
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
c = C['dimant-polarizednorms-choice']
c['question'] = 'After a split, two-camp norm, how did people contribute?'
c['options'] = ['Far more spread out, toward both ends', 'Clustered at the safe middle option', 'Much as they did after a tight norm', 'Close to the average of what they saw']
c['answer'] = 0
c['answerTitle'] = 'Contributions split toward the extremes'
c['explain'] = ('With 1,203 US adults, Dimant and colleagues show that a polarized, two-camp norm produced far more dispersed contributions '
                'than a tight norm (variance 2.68 against 1.26). In the authors’ words, in polarized environments most individuals prefer extreme actions despite the strategic risk.')
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 21, minor 4: subtract21 was read on the publisher page, abstract plus Extended Data legends
b = json.loads(bp.read_text())
S = b['sources'] if isinstance(b['sources'], dict) else {s['id']: s for s in b['sources']}
v = S['subtract21']['verification']
v.update(status='verified_published_excerpts', text_read='publisher article page: abstract and Extended Data figure legends', text_url='https://www.nature.com/articles/s41586-021-03380-y')
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 21, minor 5: the published text for the "kept using it" follow-up was not reachable; ask what the stored quotes answer
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
for f in C['ai01']['follow']:
    if f['q'] in ('Did people keep using it?', 'Did quality suffer for the speed?'):   # the quality figure is ai02's answer, so it stays off ai01
        f['q'] = 'What kind of tasks were they?'
        f['a'] = 'Occupation-specific, incentivized writing tasks, each typical of the participant’s own job.'
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 21, minor 14: titles that describe the item and are not near twins
C['dimant-requiem-forecast']['title'] = 'Four honesty messages'
C['social01']['title'] = 'Tight, loose or split'
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
