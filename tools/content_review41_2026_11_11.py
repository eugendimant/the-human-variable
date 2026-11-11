"""Review 40's remaining content Minors (iteration 63). Idempotent. Three distractors reworded; no keyed option changes."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}
ep = ROOT / 'src/evidence.json'; E = json.loads(ep.read_text())
def quote(cid, src, q, loc):
    if not any(x['quote'] == q for x in E[cid]): E[cid].append({'source': src, 'quote': q, 'location': loc})
# invented scenes: the scene is the study's own setting (abstract quotes already stored)
C['bz02']['scene'] = 'Twenty-five large randomized experiments tested digital ad campaigns at major US retailers and brokerages, covering $2.8 million of ad spending. A customer’s weekly sales swing far more than an ad can move them.'
C['rollout4']['scene'] = 'Last step: training. In a field experiment, nearly 1,000 high school students practiced math with unrestricted GPT-4, then took exams without it. Your plan gives new hires the same unrestricted access.'
# dimant-hate-choice: the figure's line says what the figure shows about the headline
C['dimant-hate-choice']['chart']['note'] = 'Share who cooperate if the partner does. The drop is as large for painting taste, so expectations set politics apart.'
# ai02: a manager line in plain words; the follow-up no longer repeats the screen
c = C['ai02']
c['implication'] = 'When you pilot an AI writing tool, measure speed and quality together, and have graders judge the work without knowing who used AI.'
for f in c['follow']:
    if f['q'] == 'Did quality really improve?':
        f['q'] = 'How did workers feel about AI afterwards?'; f['a'] = 'Concern and excitement about AI both rose, and the rise was temporary.'
quote('ai02', 'noy23', 'Inequality between workers decreased, and concern and excitement about AI temporarily rose.', 'Science abstract (version of record)')
# index charts: ai02's unused 100-to-118 index goes; social12 shows the two measured callback rates
for cid in ('ai02', 'social12'):
    for k in ('visual', 'values', 'labels', 'unit'): C[cid].pop(k, None)
C['social12']['chart'] = {'labels': ['African-American-sounding names', 'White-sounding names'], 'values': [6.45, 9.65], 'unit': '%', 'highlight': None, 'decimals': 2, 'max': 10,
                          'note': 'Share of résumés that got a callback. 9.65 is 50% more than 6.45.'}
quote('social12', 'resume04', 'Resumes with White names have a 9.65 percent chance of receiving a callback.', 'Section III.A, p. 997 (version of record)')
quote('social12', 'resume04', 'This represents a difference in callback rates of 3.20 percentage points, or 50 percent,', 'Section III.A, p. 997 (version of record)')
if not any(x.get('printed') == '6.45' for x in E['social12']): E['social12'].append({'source': 'resume04', 'printed': '6.45', 'location': 'Table 1, African-American names, percent callback (9.65 minus 3.20)'})
# wording cue: comparative words sat in keyed options more often than in distractors (30% against 18%); three distractors now carry one
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())
for cid, old, new in (('axb05', 'The model had too little training data', 'The model had less training data on Black patients'),
                      ('biz02', 'Few employees knew they could change it, and few asked', 'Changing the rate took more paperwork than most would do'),
                      ('social20', 'Compare how often each team breaks the rule', 'Check which team breaks the rule more often')):
    c = C[cid]
    if old in c['options']:
        assert c['options'].index(old) != c['answer']
        c['options'][c['options'].index(old)] = new
        assert K[cid]['keyed'] == [c['options'][c['answer']]]
        K[cid]['options'] = sorted(c['options'])
kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(E, ensure_ascii=False, indent=1) + '\n')
print('review 41 content applied')
