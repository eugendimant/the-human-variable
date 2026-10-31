"""Review 20 content fixes (idempotent)."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
bp, ep = R / 'src/bank.json', R / 'src/evidence.json'
b = json.loads(bp.read_text()); ev = json.loads(ep.read_text())
C = {c['id']: c for c in b['challenges']}
# minor 2: the scene's control (74) must not land inside the target band (76)
if 'estimate' in C['axf06']: C['axf06']['estimate']['tolerance'] = 1
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
# review 22, M2: axf06's 76 vs 74 was not significant (P = .60), so it is a forecast about the gain, not a point estimate
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
x = C['axf06']
if x['format'] == 'estimate':
    x['format'] = 'forecast'; x.pop('estimate', None)
    x['question'] = 'How likely is it that the study found this?'
    x['scene'] = 'Fifty physicians had 60 minutes for up to six hard clinical vignettes, randomized to GPT-4 plus usual resources or usual resources only. Researchers also had GPT-4 answer the cases alone.'
    x['forecast'] = {'claim': 'Physicians given GPT-4 reached clearly higher diagnostic reasoning scores than physicians with usual resources only.', 'truth': False}
    x['chart'] = {'labels': ['Physicians, usual resources', 'Physicians with GPT-4', 'GPT-4 alone'], 'values': [74, 76, 92], 'unit': '%', 'highlight': 1,
                  'note': 'Median diagnostic reasoning score per case; the physicians’ 2-point difference was not significant (P = .60).'}
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
C['axf06']['forecast']['claim'] = 'Physicians given GPT-4 reached significantly higher diagnostic reasoning scores than physicians with usual resources only.'
C['bz07']['estimate']['tolerance'] = 6   # keeps the constant-guess cap after axf06 left the estimates
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 22, m5 and m8: units, a marginal contrast drawn as such, and a headline the chart supports
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
C['biz05']['chart']['note'] = 'Daily electricity use of below-average homes, kWh per day.'
en = C['dimant-enforcers-rank']['chart']; en['ns'] = [2, 3]
en['note'] = 'Average chosen probability that the coworker is punished, Study 2 vignette. Outlined: the equalizing-bribe difference (P = 0.074).'
h = C['dimant-hate-choice']
h['answerTitle'] = 'Expectations, more than unwillingness, drove the gap'
h['chart']['note'] = 'Share who cooperate when they expect the partner to; the drop is about as large for a painting-taste outgroup.'
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 22, m12: the scene states the manipulation, not the result, and the strawman option becomes a real rival (projection)
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
n = C['dimant-notalie-causal']
n['scene'] = ('In an incentivized experiment, people could misreport a private outcome for money and were asked what most others do. '
              'Researchers varied whether people learned of the chance to misreport before or after stating that belief.')
n['question'] = 'What best explains the link between believing most people lie and misreporting?'
n['options'][1] = 'People who planned to lie projected their own choice onto others'
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 22, m15: scope states what this study covers, with nothing unsourced
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
C['judg09']['boundary'] = 'Hypothetical choices by 95 respondents per problem.'
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 22, m11: claim length must not predict truth (shorter false claims, longer true ones; same meaning)
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
NEW = {
 'bz02': 'The median experiment’s ROI confidence interval was under 50 percentage points wide.',
 'axf06': 'Physicians with GPT-4 scored significantly higher than physicians without it.',
 'bz16': 'In real plans, more equity funds on the menu meant more money in equity.',
 'biz04': 'In the German hotels, the norm sign beat the standard environmental sign.',
 'social08': 'Behavior spread farther through random long ties than through clustered ties.',
 'bz08': 'After the fine was removed, late pickups stayed at the higher level they had reached while the fine applied.',
 'dimant-opioid-forecast': 'Adding the reminder cards to the cash incentive lowered the program’s cost per pill of medication returned.',
 'accuracy-prompt': 'A single prompt to think about accuracy raised the average quality of the news sources that users shared.',
}
for k, v in NEW.items(): C[k]['forecast']['claim'] = v
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
