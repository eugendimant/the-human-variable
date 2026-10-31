"""Fixes from independent review 1 (2026-10-31) plus merge of cluster E (AI x Business)."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
ev = json.loads((ROOT / 'src/evidence.json').read_text())
E = json.loads(Path(sys.argv[1]).read_text())
log = []
def opts(cid, new, ans=None, why='Review 1 M8: plausible, length-balanced options'):
    c = C[cid]; c['options'] = new
    if ans is not None:
        if c['format'] == 'multi': c['multiAnswers'] = ans
        else: c['answer'] = ans
    log.append((cid, 'options', why))
# ---- M8 strawmen and length cues
opts('ai07', ['AI-assisted stories were rated more creative', 'AI-assisted stories were more similar to each other', 'Gains were largest for the most creative writers', 'The AI-assisted set was more varied overall'], [0, 1])
C['ai09']['question'] = 'After seeing the model err, whom did people choose for paid forecasts?'
opts('ai09', ['Themselves, though the model beat them', 'The model, since it beat them', 'The model more often than before', 'Each about half of the time'], 0)
opts('social03', ['Their choices varied more', 'Their choices clustered on the average', 'Their choices split into two camps'], 0)
opts('ai12', ['It costs more than a human doctor', 'It cannot account for my situation', 'It takes longer than a human doctor'], 1)
C['social04']['question'] = 'Students rated their own comfort with campus drinking and the average student’s. What did they report?'
opts('social04', ['Peers were more comfortable than they were', 'Peers were as comfortable as they were', 'Peers were less comfortable than they were'], 0)
C['social10']['question'] = 'Which group feature predicted performance across many different tasks?'
opts('social10', ['More equal turn-taking in conversation', 'The smartest member’s individual score', 'The average intelligence of members', 'Group satisfaction and motivation'], 0)
opts('social13', ['Women more likely to advance and be hired', 'No measurable change for women', 'Women less likely to advance'], 0)
opts('social15', ['Love showed in feelings, hate in behavior', 'Hate showed in feelings, love in behavior', 'Both showed in feelings, not in behavior'], 0)
opts('social20', ['Keep each person’s view, not just the mean', 'Compare the two team averages', 'Ask each manager to describe the norm', 'Count past policy violations'], 0)
opts('bz01', ['About 222%', 'About 73%', 'About 316%', 'No measurable lift'], 1)
opts('bz12', ['Below-median earners: less satisfied, job hunting', 'Everyone: more satisfied with transparency', 'Above-median earners: more satisfied', 'No change: staff already knew peer pay'], 0)
opts('meta-perception-causal', ['Randomly correcting beliefs cut obstructionism ratings', 'The most inaccurate partisans were also the most hostile', 'The same bias appeared in a national sample', 'Inaccuracy tracked heavy political news consumption'], 0)
opts('dimant-observability-choice', ['Raised giving sharply', 'Did little and could backfire', 'Raised giving among the best-paid', 'Raised giving only at first'], 1)
opts('dimant-polarizednorms-choice', ['Chose the safe middle option', 'Chose an extreme, despite the risk', 'Copied the average behavior', 'Acted as in tight settings'], 1)
# ---- B2: estimate and forecast items carry no options (some stated the answer)
for c in C.values():
    if c['format'] in ('estimate', 'forecast'):
        for k in ('options', 'answer', 'multiAnswers'):
            if k in c: c.pop(k); log.append((c['id'], k, 'B2: stale field could reveal the answer'))
# ---- M2: estimate ranges independent of the target
for c in C.values():
    e = c.get('estimate')
    if e and e.get('unit', '%') == '%' and e['min'] >= 0 and 0 <= e['target'] <= 100 and (e['min'], e['max']) != (0, 100):
        log.append((c['id'], 'estimate range', f"{e['min']}-{e['max']} -> 0-100")); e['min'], e['max'] = 0, 100
# ---- M6: non-significant differences are not scored as evidence
a = C['axb08']['allocate']; a['values'] = [0, 0, 0, 81.2]; a['valueName'] = 'change in odds of higher post-debate agreement vs human-human debates (non-significant changes count as zero)'
C['axb02']['rankTies'] = [[0, 1]]; C['axb02']['explain'] += ' The two adjustable groups did not differ meaningfully, so their order is not scored.'
C['dimant-enforcers-rank']['rankTies'] = [[2, 3], [1, 2]]
C['axb01']['delegate']['tasks'] = C['axb01']['delegate']['tasks'][:2]
log += [('axb08', 'values', 'M6'), ('axb02', 'rankTies', 'M6'), ('dimant-enforcers-rank', 'rankTies', 'M6'), ('axb01', 'tasks', 'M6: dropped task resting on a non-significant estimate')]
# ---- M7: the causal diagram must not draw the answer before the reveal
for n in C['axb05']['dag']['nodes']:
    if n['id'] == 'cost': n['mask'] = True
# ---- Minor fixes
C['ai02']['scene'] = 'In an online experiment, 453 professionals did short writing tasks for their occupation, half with ChatGPT. Independent professionals graded the finished work blind.'
C['axb06']['answerTitle'] = 'Overruling the test went with worse hires'
# ---- Merge cluster E
for sid, s in E['sources'].items():
    if sid not in bank['sources']:
        s = dict(s); s.setdefault('kind', 'peer-reviewed'); s.setdefault('url', 'https://doi.org/' + s['doi']); bank['sources'][sid] = s
THEME = {'luo19': 'ai-trust', 'ayers23': 'ai-work', 'zhou24': 'ai-work', 'goldstein24': 'persuasion', 'spitale23': 'persuasion', 'matz24': 'persuasion', 'hui24': 'ai-work',
         'longoni22': 'ai-trust', 'dietvorst20': 'ai-trust', 'granulo19': 'ai-work', 'yin24': 'ai-trust', 'reif25': 'ai-work', 'fugener22': 'ai-work', 'tong21': 'ai-trust', 'jia24': 'ai-work', 'cui26': 'ai-work', 'hartmann25': 'persuasion'}
for c in E['challenges']:
    c = dict(c); e = c.pop('evidence', None)
    if e: ev[c['id']] = e
    if c['format'] == 'forecast': c['question'] = 'Is this what the study found?'
    c['theme'] = THEME.get(c['sources'][0], 'ai-work')
    if c['id'] not in C: bank['challenges'].append(c); C[c['id']] = c; log.append((c['id'], 'added', 'cluster E'))
# genai2: an allocation would score small, possibly non-significant gaps as evidence; ask for the headline number instead.
g = C['genai2']; g['format'] = 'estimate'
for k in ('options', 'allocate'): g.pop(k, None)
g['question'] = 'With an edited prompt and the best of three drafts, what share agreed with the claim?'
g['estimate'] = {'target': 52.7, 'min': 0, 'max': 100, 'tolerance': 5, 'label': 'Share agreeing after reading the curated GPT-3 article', 'unit': '%'}
g['answerTitle'] = 'About 53%, above the original propaganda'
C['axe11']['rankTies'] = [[2, 3]]
paths = {p['id']: p for p in bank['paths']}
if 'ai-customers' not in paths:
    bank['paths'].insert(1, {'id': 'ai-customers', 'title': 'AI meets your customers', 'case': True, 'blurb': 'Disclose the bot or not, label AI content, personalize ads, answer patients. What customers do when AI is on the other side.', 'ids': ['genai1', 'genai2', 'genai3', 'axe14', 'axe05', 'axe01', 'axe10', 'axe13']})
for p in bank['paths']:
    if p['id'] == 'leading-ai':
        for x in ('axe06', 'axe03'):
            if x not in p['ids']: p['ids'].append(x)
    if p['id'] == 'trust-algo' and 'axe07' not in p['ids']: p['ids'].append('axe07')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'docs/audit/review1_fixes_2026-10-31.json').write_text(json.dumps(log, ensure_ascii=False, indent=1))
(ROOT / 'docs/audit/draft_clusterE.json').write_text(Path(sys.argv[1]).read_text())
print(len(log), 'changes;', len(bank['challenges']), 'challenges')
