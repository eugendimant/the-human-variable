"""Review 41 content fixes (iteration 65). Idempotent. One distractor reworded; no keyed option changes."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())
# I: the rollout4 scene stated the design wrongly (students were split across arms); the bz02 scene gave the mechanism away
C['rollout4']['scene'] = 'Last step: training. In a field experiment with nearly 1,000 high school students, some practiced math with unrestricted GPT-4, and everyone then took exams without it. Your plan gives new hires the same unrestricted access.'
C['bz02']['scene'] = 'Twenty-five large randomized experiments tested digital ad campaigns at major US retailers and brokerages, covering $2.8 million of ad spending. Each one estimated its campaign’s return on investment.'
# I: the figure line says only what the figure shows
C['dimant-hate-choice']['chart']['note'] = 'Share who cooperate when they expect the partner to. The drop is about as large for a painting-taste outgroup as for a political one.'
# I: the tutor can state the two callback rates; the amber bar is the group the headline is about (m13)
c = C['social12']; c['chart']['highlight'] = 1
if not any(f['q'] == 'What were the two callback rates?' for f in c['follow']):
    c['follow'].insert(0, {'q': 'What were the two callback rates?', 'a': '9.65% for White-sounding names and 6.45% for African-American-sounding names, a gap of 3.20 percentage points.'})
v = B['sources']['resume04']['verification']
v.update({'status': 'verified_full_text', 'checked': '2026-11-11', 'text_read': 'full text of the published article (AER 94(4), pp. 991-1013): abstract, Section III.A and Table 1', 'text_url': 'https://users.ssc.wisc.edu/~gwallace/Papers/Bertrand%20&%20Mullainathan%20(2004).pdf'})
# m4: biz02's reworded distractor was near-true; it is now plainly a different mechanism, and two-part like the key
c = C['biz02']
for old in ('Changing the rate took more paperwork than most would do',):
    if old in c['options']:
        assert c['options'].index(old) != c['answer']
        c['options'][c['options'].index(old)] = 'Higher rates were closed to newer staff, and few asked'
        K['biz02']['options'] = sorted(c['options'])
assert K['biz02']['keyed'] == [c['options'][c['answer']]]
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('review 41b content applied')
