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
# review 23, M2: evidence figures from numbers the explanations already quote; headline-style answer titles (Burn-Murdoch)
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
CH = {
 'ai07': {'labels': ['More novel', 'More useful', 'More similar to each other'], 'values': [8.1, 9.0, 8.9], 'unit': '%', 'highlight': 2,
          'note': 'Stories by writers with access to up to five AI ideas, against writers without; similarity as a share of its range.'},
 'social07': {'labels': ['Democrats on same-sex rights', 'Republicans on gun policy'], 'values': [95, 50], 'unit': '%', 'highlight': 1,
              'note': 'Share of a party including the same view in their drawing, the highest and the lowest issue.'},
 'social15': {'labels': ['Gave to allies', 'Gave to a painting group-mate', 'Took from opponents'], 'values': [14.97, 13.54, 22.9], 'unit': '%', 'highlight': 0,
              'note': 'Share of the endowment given or taken.'},
 'social16': {'labels': ['Taking from opponents, no default', 'Taking from opponents, default nudge'], 'values': [20, 0], 'unit': '%', 'highlight': 1,
              'note': 'Share of the endowment taken from political opponents (about 20% without the nudge).'},
 'opposing-views-bot': {'labels': ['Republicans, intent to treat', 'Republicans, full compliers'], 'values': [0.12, 0.60], 'unit': '', 'highlight': 1,
                        'note': 'Shift toward conservatism on a seven-point scale.'},
 'dimant-observability-choice': {'labels': ['Unobserved', 'Observed', 'Observed, asked first about others'], 'values': [-18.4, -28.3, 9.3], 'unit': '%', 'highlight': 1,
                                 'note': 'Change in the charity account.'},
}
for k, v in CH.items(): C[k]['chart'] = v
C['ai07']['explain'] = C['ai07']['explain'].replace('when given five AI ideas', 'with access to up to five AI ideas')
C['social15']['answerTitle'] = 'Closer to allies, but no more generous to them'
C['social07']['answerTitle'] = 'Each party holds several distinct views'
C['social01']['answerTitle'] = 'The spread of others’ behavior changed choices'
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 23, minor 13: the stored option order carries no positional cue (the served JSON keeps bank order; the page shuffles)
b = json.loads(bp.read_text())
PAIRS = [(0, 2), (1, 3), (0, 3), (1, 2), (2, 3), (0, 1)]
for fmt in ('choice', 'causal', 'multi'):
    items = sorted((c for c in b['challenges'] if c['format'] == fmt and not c.get('retired')), key=lambda c: c['id'])
    for k, c in enumerate(items):
        n = len(c['options']); keyed = sorted(c['multiAnswers']) if fmt == 'multi' else [c['answer']]
        want = list(PAIRS[k % len(PAIRS)]) if fmt == 'multi' and n == 4 else [k % n] if fmt != 'multi' else keyed
        others = [i for i in range(n) if i not in keyed]
        order = [None] * n
        for pos, i in zip(want, keyed): order[pos] = i
        it = iter(others)
        order = [i if i is not None else next(it) for i in order]
        c['options'] = [c['options'][i] for i in order]
        if fmt == 'multi': c['multiAnswers'] = sorted(order.index(i) for i in keyed)
        else: c['answer'] = order.index(keyed[0])
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 23: banned stock phrasing, a baseline splice, an overclaimed null, contest titles that cue the answer, hate23 game difference
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
C['biz04']['implication'] = 'Before rolling out a famous nudge, test it against the plain message you would otherwise use as well as against doing nothing.'
C['misperceived-norms-action']['implication'] = 'Share accurate peer-support data to move stalled behavior, then track actual outcomes for months alongside stated intentions.'
for f in C['axb06']['follow']:
    f['a'] = f['a'].replace('so differences in overrides were not just differences in who applied.', 'so differences in overrides did not come from differences in who applied.')
for f in C['dimant-polarizednorms-choice']['follow']:
    f['a'] = f['a'].replace('the whole distribution of peer behavior, not just its mean, shapes reactions.', 'the whole distribution of peer behavior shapes reactions, beyond its mean.')
C['dimant-proximity-estimate']['explain'] = C['dimant-proximity-estimate']['explain'].replace(
    'With observation alone, participants took an additional 21.9 ECUs and donations fell by about 20% compared with no observation.',
    'With observation alone, participants took 21.9 ECUs more than in the earlier part of the experiment, and donations fell by about 20% against no observation.')
C['axe13']['answerTitle'] = 'Trip spending rose $117; the sneaker effect was not significant'
C['bz06']['title'] = 'Mugs, sellers and buyers'
C['bz16']['title'] = 'Fund menus and real plans'
q = {'q': 'Which games were these?', 'a': 'Giving and taking games, in which one person moved money to or from another; a public goods game in the same project measured cooperation separately.'}
if not any(f['q'] == q['q'] for f in C['social15']['follow']): C['social15']['follow'].append(q)
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 23, minor 17: one forecast prompt everywhere; the notalie diagram's last node inside the frame at phone width
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
for c in b['challenges']:
    if c['format'] == 'forecast': c['question'] = 'How likely is it that the study found this?'
for n in C['dimant-notalie-causal']['dag']['nodes']:
    if n['id'] == 'lie': n['x'] = 430
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# review 23, minor 8: the measure as the title, a simulation labelled as one, the source only once
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
C['axb05']['chart']['labels'] = ['Current algorithm', 'If the spending gap were removed (simulated)']
C['axb05']['chart']['note'] = 'Share of Black patients flagged for extra help.'
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
