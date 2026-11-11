"""Review 39 minors: axe10 claim, dimant-conspiracy-choice distractors, axe12 on a stated axis. Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())

# axe10: the claim is false on the paper's own result (an AI image achieved an up to 50% higher click-through rate)
f = C['axe10']['forecast']
f['claim'] = 'In the live ad test, no AI-generated image beat the human-made image on click-through rate.'; assert f['truth'] is False

# dimant-conspiracy-choice (Ren, Dimant & Schweitzer): distractors a careful reader could hold, each false by the item's own evidence
c = C['dimant-conspiracy-choice']
opts = ['Social engagement: they expected, and got, more feedback', 'A wish to warn others that the posts were false', 'Sharing stayed flat across rounds, whatever feedback the posts earned', 'Fading attention: by the later rounds they shared without reading']
if sorted(c['options']) != sorted(opts):
    c['options'] = opts; c['answer'] = 0; c.pop('permuted', None)
    K['dimant-conspiracy-choice'] = {'keyed': [opts[0]], 'options': sorted(opts)}   # pinned by hand (I11)

# axe12: ratings drawn as dots on a stated axis, not as bars from zero
C['axe12']['chart']['axis'] = [1.5, 3]

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('review 39b content applied')
