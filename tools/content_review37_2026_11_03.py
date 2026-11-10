"""Review 37 content fixes. Idempotent; edits by text. Keyed options are pinned by hand only (I11)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}
def rep(cid, field, old, new): C[cid][field] = C[cid][field].replace(old, new)
# m2 (I12): printed decimals as quoted
C['axf02']['chart']['decimals'] = 2
C['dimant-hate-choice']['chart']['decimals'] = 1
# m3: the figure colours neither drop: they are about equal, and the headline is about expectations
C['dimant-hate-choice']['chart']['highlight'] = None
C['dimant-hate-choice']['chart']['note'] = C['dimant-hate-choice']['chart']['note'].replace('Share who cooperate when they expect the partner to; the drop is about as large for a painting-taste outgroup.', 'Share who cooperate when they expect the partner to. The drop is about as large for a painting-taste outgroup as for a political one.')
# m12: copy
if not C['axe05']['answerTitle'].endswith('of evaluations'): rep('axe05', 'answerTitle', 'Raters preferred the chatbot in 78.6%', 'Raters preferred the chatbot in 78.6% of evaluations')
C['biz05']['chart']['note'] = C['biz05']['chart']['note'].replace('Daily electricity use of below-average homes, kWh per day.', 'Daily electricity use of below-average homes, kWh.')
rep('bz04', 'explain', 'Only 29.7% finished by their best-guess date, against an average prediction of 33.9 days, and', 'Only 29.7% finished by their best-guess date (on average they had predicted 33.9 days), and')
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
print('review 37 content applied')
