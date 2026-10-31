"""Sharpen legacy questions: ask for a prediction about a measured result, and keep scenes from giving the answer away."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
def up(cid, **kw): C[cid].update(kw)
up('ai01', question='How much less time did the ChatGPT group take?')
up('ai02', question='By how much did graded quality change with ChatGPT?')
up('ai07', question='Which two results did the study find?')
up('ai11', question='For which task were people more reluctant to rely on an algorithm?', options=['Judging a personal aesthetic preference', 'Recommending a practical product', 'Equally reluctant for both'], answer=0)
up('ai12', question='What mainly drove consumers’ resistance?')
up('biz02', scene='After automatic enrollment, a large share of new hires kept both the default contribution rate and the default fund, a combination few earlier hires had chosen.',
   question='Why did so many keep the default?', options=['They had each worked out it was best', 'Inertia, and the default read as advice', 'Changing the default was not allowed'], answer=1)
up('biz03', question='Which sign got more towels reused?', options=['The conservation sign', 'The “most guests reuse” sign', 'Neither changed reuse'], answer=1)
up('biz04', question='Which comparison raised reuse most?', options=['Guests across the whole hotel', 'Guests who stayed in this same room', 'Neither beat the conservation sign'], answer=1)
up('biz05', question='Which two results did the study find?')
up('biz07', question='Which kind of fix do people tend to miss?', options=['Adding a review step', 'Removing an existing step', 'Assigning a new owner'], answer=1)
up('social01', question='Which two results did the experiments find?')
up('social07', question='What did drawing each party’s norm reveal?', options=['Near-uniform views within each party', 'Several coexisting views within each party', 'Identical views across parties'], answer=1)
up('social13', question='What happened to women’s chances once screens were used?')
up('social14', scene='White and Black students were asked how interested they were in contact with the other group, and why each side might hold back.',
   question='How did each group explain the hesitation?', options=['Own side fears rejection; the other side is not interested', 'Both sides fear rejection', 'Neither side wants more contact'], answer=0)
up('social15', scene='Across 15 experiments, Trump supporters and opponents rated how close they felt to each side and made costly choices that helped or hurt members of each side.',
   question='Where did in-group love and out-group hate show up?')
up('social16', question='Which two results did the nudges produce?')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
