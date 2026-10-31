"""Fixes from independent review 10 (2026-10-31). Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']
ev = json.loads((ROOT / 'src/evidence.json').read_text())
# --- minor 3: the paper tests norm information within each scenario, not every cross-cell pair
e = C['dimant-enforcers-rank']
if e['format'] == 'rank':
    for k in ('options', 'rankAnswer', 'rankTies', 'rankValues', 'rankLabel', 'permuted'): e.pop(k, None)
    e['format'] = 'forecast'; e['question'] = 'How likely is it that the study found this?'
    e['forecast'] = {'claim': 'Telling people that most others report bribery raised reporting of bribes that created inequity.', 'truth': True}
    e['answerTitle'] = 'Norm information raised reporting of unfair bribes'
# --- minor 4: only routes the study compared
d = C['axe01']['delegate']
if 'Human with AI input' in d['choices']:
    d['choices'] = ['AI recommender', 'Human recommender']
    for t in d['tasks']:
        t.pop('also', None)
        if t['text'].startswith('Pick a vacation spot'):
            t['answer'] = 1; t['why'] = 'For hedonic picks, people judged AI recommenders less competent than humans (Studies 1 to 4).'
    C['axe01']['scene'] = 'Your retail site can show product picks from an AI engine or from a human expert. Eight experiments tested which source consumers prefer.'
    C['axe01']['explain'] = 'Across Studies 1 to 7b, people saw AI as more competent for utilitarian attributes and less competent for hedonic ones, and the preference for AI reversed when a practical pick had to fit one person’s unique tastes.'
# --- minor 5: bz01 keeps only quotes from the version of record
ev['bz01'] = [q for q in ev.get('bz01', []) if not re.search(r'73%|222%|316%|factor of three', q['quote'])]
# --- minor 7: Dimant is a coauthor of the opioid study
if 'opioid26' in S:
    S['opioid26']['authors_full'] = 'Mattie Toma, Elizabeth Burnett, Akshay Debroy, Eugen Dimant, Lu Liu, Steven Safran, Meghan Saya, Elizabeth Schultz'
# --- minor 1: fewer null distractors, rival claims instead
def swap(cid, old, new): C[cid]['options'] = [new if o == old else o for o in C[cid]['options']]
swap('bz12', 'Everyone: more satisfied with transparency', 'Above-median earners: happier, job hunting less')
swap('bz14', 'Neither: gender drove both equally', 'Separate review, judged on more information')
swap('biz03', 'Neither changed reuse', 'Both signs worked about equally')
swap('biz05', 'Feedback had no effect on heavy users', 'Heavy users raised their use after feedback')
# --- minor 11: copy
C['social13']['question'] = 'How did the authors characterize their evidence?'
C['ai12']['answerTitle'] = 'People fear AI ignores what makes them unique'
for n in C['meta-perception-causal']['dag']['nodes']:
    if n['label'] == 'Meta-percept': n['label'] = 'Belief gap'
C['meta-perception-causal']['explain'] = C['meta-perception-causal']['explain'].replace('Across 4,282 participants people', 'Across 4,282 participants, people')
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
