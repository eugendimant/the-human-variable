"""Review 7, M3: replace paraphrased evidence with verbatim quotes from published texts (or accepted manuscripts, labelled),
and change or remove numbers that no such text supports. Inputs: docs/audit/evidence_repair_{A,B}_2026_10_31.json. Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
ev = json.loads((ROOT / 'src/evidence.json').read_text())
WEAK = re.compile(r'paraphrase|as recorded|audit|fetch-tool|summary|as extracted|rendering', re.I)
SKIP = {'bz01'}  # handled by hand below: the proposed options broke the distractor gates
for name in ('A', 'B'):
    f = ROOT / f'docs/audit/evidence_repair_{name}_2026_10_31.json'
    if not f.exists(): continue
    for cid, v in json.loads(f.read_text()).items():
        if cid not in C: continue
        good = [q for q in ev.get(cid, []) if not WEAK.search(q.get('location', '') + ' ' + q['quote'])]
        new = [{'source': q.get('source') or C[cid]['sources'][0], 'quote': q['quote'], 'location': q['location']} for q in v.get('quotes', [])]
        seen = set(); ev[cid] = [q for q in good + new if not (q['quote'] in seen or seen.add(q['quote']))]
        if cid in SKIP: continue
        for u in v.get('unsupported', []):
            fld, rep = u['field'], u.get('replacement')
            m = re.fullmatch(r'follow\[(\d)\]\.a', fld)
            if m and isinstance(rep, str): C[cid]['follow'][int(m.group(1))]['a'] = rep
            elif fld in ('scene', 'question', 'answerTitle', 'explain', 'implication', 'boundary') and isinstance(rep, str): C[cid][fld] = rep
            elif fld == 'chart' and u.get('action') == 'remove': C[cid].pop('chart', None)
            elif fld == 'study.n' and isinstance(rep, str): C[cid].setdefault('study', {})['n'] = rep
            else: print('not applied:', cid, fld)
# bz01: the 73%, 222% and 316% figures appear only in a 2018 authors' copy, not the version of record
b = C['bz01']
b['scene'] = 'Your agency compares Facebook users who saw a campaign with users who did not, after matching on demographics and behavior. A randomized holdout ran at the same time.'
b['question'] = 'How did the matched estimates compare with the randomized tests across 15 campaigns?'
b['options'] = ['They matched the randomized lift', 'They often missed the randomized lift', 'They understated the lift every time', 'They matched once enough data were added']
b['answer'] = 1; b.pop('chart', None)
b['answerTitle'] = 'Matching often missed the experiment’s answer'
b['explain'] = 'Across 15 Facebook ad experiments with 1.6 billion impressions, observational methods often failed to reproduce the randomized estimates, even after conditioning on extensive demographic and behavioral data.'
b['follow'][1] = {'q': 'Did adding data fix it?', 'a': 'No. Across the 15 experiments, observational methods often failed to match the randomized results, even with rich demographic and behavioral data.'}
# wording the published texts do not support, and verification notes
C['meta-perception-causal']['boundary'] = 'Found in competitive intergroup contexts; the correction was tested in one online experiment with 1,122 participants.'
if 'former clients' in C['bz09']['scene']: C['bz09']['scene'] = C['bz09']['scene'].replace('former clients', 'clients')
for cid in ('bz09', 'lies-in-disguise'):
    n = C[cid].get('study', {}).get('n', '')
    if re.search(r'former clients|Swiss university students', n): C[cid]['study'].pop('n')
S = bank['sources']
if 'fischbacher13' in S: S['fischbacher13']['verification']['text_read'] = 'abstract of the published JEEA article'
if 'lees20' in S: S['lees20']['verification']['text_read'] = 'Harvard DASH manuscript of the Nature Human Behaviour article (whether it is the final accepted version is unconfirmed)'
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
