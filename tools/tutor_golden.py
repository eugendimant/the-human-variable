"""Regenerate tests/tutor_golden.json: the offline tutor's answer (first 90 characters) to a fixed battery of everyday questions on
every live decision. A route change that alters any of these answers fails tests/test_tutor.py until the change is reviewed and this
file is regenerated deliberately (invariant I16, regression audit 29)."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from server import tutor as T
BATTERY = ['What is the design?', 'What is the sample?', 'Who took part?', 'How big was the effect?', 'What should a manager do?',
           'Did it last?', 'Does this replicate?', 'Was this randomized?', 'What is the catch?', 'Who wrote this?', 'Explain it simply',
           'Would this work in Europe?', 'Was real money at stake?', 'Who benefited most?', 'Was the difference significant?',
           'Should we use this when we hire?', 'Should we roll this out right now?', 'Is it ethical to act on this?']
def snapshot():
    return {cid: {q: T.curated(q, cid)['answer'][:90] for q in BATTERY} for cid, c in sorted(T.CHALLENGES.items()) if not c.get('retired')}
def wide():
    """The audit-29 batteries: 'what is X' on every decision, and 'should we / is it' phrasings on 30 decisions (about 7,000 pairs)."""
    W = json.loads((ROOT / 'tests/tutor_wide_questions.json').read_text()); live = [cid for cid, c in sorted(T.CHALLENGES.items()) if not c.get('retired')]
    out = {cid: {q: T.curated(q, cid)['answer'][:60] for q in W['what_is']} for cid in live}
    for cid in W['ids_should']:
        if cid in T.CHALLENGES: out.setdefault(cid, {}).update({q: T.curated(q, cid)['answer'][:60] for q in W['should_ethics']})
    return out
if __name__ == '__main__':
    (ROOT / 'tests/tutor_golden.json').write_text(json.dumps(snapshot(), ensure_ascii=False, indent=0) + '\n')
    (ROOT / 'tests/tutor_golden_wide.json').write_text(json.dumps(wide(), ensure_ascii=False, separators=(',', ':')) + '\n'); print('written')
