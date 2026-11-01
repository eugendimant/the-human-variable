"""Regenerate tests/tutor_golden.json: the offline tutor's answer (first 90 characters) to a fixed battery of everyday questions on
every live decision. A route change that alters any of these answers fails tests/test_tutor.py until the change is reviewed and this
file is regenerated deliberately (invariant I16, regression audit 29)."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from server import tutor as T
BATTERY = ['What is the design?', 'What is the sample?', 'Who took part?', 'How big was the effect?', 'What should a manager do?',
           'Did it last?', 'Does this replicate?', 'Was this randomized?', 'What is the catch?', 'Who wrote this?', 'Explain it simply',
           'Would this work in Europe?', 'Was real money at stake?', 'Who benefited most?', 'Was the difference significant?']
def snapshot():
    return {cid: {q: T.curated(q, cid)['answer'][:90] for q in BATTERY} for cid, c in sorted(T.CHALLENGES.items()) if not c.get('retired')}
if __name__ == '__main__':
    (ROOT / 'tests/tutor_golden.json').write_text(json.dumps(snapshot(), ensure_ascii=False, indent=0) + '\n'); print('written')
