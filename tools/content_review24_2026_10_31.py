"""Review 24 content fixes. Idempotent; edits by text, never by option index (invariant I11)."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
bp, ep = R / 'src/bank.json', R / 'src/evidence.json'
b = json.loads(bp.read_text()); ev = json.loads(ep.read_text()); C = {c['id']: c for c in b['challenges']}

# minor 3: Science erratum of 22 Oct 2026 (doi:10.1126/science.aem1178); the corrected abstract reads 2190
x = C['axb15']
for k in ('scene', 'boundary'): x[k] = x[k].replace('2,044', '2,190')
x['study']['n'] = x['study']['n'].replace('2,044', '2,190')
for e in ev['axb15']:
    if e.get('quote', '').startswith('engaged 2044'):
        e['quote'] = 'engaged 2190 conspiracy believers in personalized evidence-based dialogues with GPT-4 Turbo'
        e['location'] = 'Abstract as corrected by the erratum (Science, 22 Oct 2026, doi:10.1126/science.aem1178); Europe PMC record of PMID 39264999'
for e in ev['axb15']:
    if 'Crossref record' in e.get('location', ''): e['location'] = 'Abstract, corrected version (Europe PMC record of PMID 39264999)'
v = b['sources']['costello24'].setdefault('verification', {})
v['erratum'] = 'Erratum, Science 22 Oct 2026 (doi:10.1126/science.aem1178): the corrected abstract gives 2190 participants; the erratum body could not be read.'

# minor 4: the follow-ups attribute the original claim and name what "it" is
for f in C['bz06']['follow']:
    if f['q'] == 'Is it just reluctance to pay?':
        f['q'] = 'What did the 1990 study conclude?'
        f['a'] = f['a'].replace('the gap reflects reluctance to give up the mug', 'Kahneman, Knetsch and Thaler read the gap as reluctance to give up the mug') if 'Kahneman' not in f['a'] else f['a']
    if f['q'] == 'Did it reduce trading?': f['q'] = 'Did the gap reduce trading in the 1990 markets?'
    if f['q'] == 'What did the 1990 study conclude?' and f['a'].startswith('No. '): f['a'] = f['a'][4:]

# minor 5: rivals a manager could believe, not strawmen
def swap(cid, old, new):
    c = C[cid]; c['options'] = [new if o == old else o for o in c['options']]
swap('social01', 'People ignored the norm and played their own strategy', 'The average of what others did explained choices')
swap('social01', 'Only the average of what others did changed choices', 'The average of what others did explained choices')
swap('biz05', 'Above-average households raised their electricity use', 'The smiley made above-average households use more')

# minor 11: headlines state the finding
C['ai09']['answerTitle'] = 'Seeing the model err drove people away from it'
C['biz02']['answerTitle'] = 'People took the default as advice'

# minor 7 and 8: true minus signs and en-dash ranges in reader-facing text (quotes stay verbatim)
import re
MINUS = re.compile(r'(?<![\w\d])-(?=\d)')
def fix(s): return re.sub(r'(\d)-(\d)', r'\1–\2', MINUS.sub('−', s)) if isinstance(s, str) else s
for c in b['challenges']:
    for k in ('explain', 'answerTitle', 'implication', 'boundary', 'scene'): c[k] = fix(c.get(k)) if c.get(k) else c.get(k)
    for f in c.get('follow', []): f['a'] = fix(f['a'])
    if c.get('rankValues'): c['rankValues'] = [fix(v) for v in c['rankValues']]
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
print('ok')
# minor 5: ai11 offered two options and a scene that named the answer's dimension; a null rival joins and the scene stays neutral
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
a = C['ai11']
a['scene'] = 'In online lab and field studies, people decided whether to rely on an algorithm or a person for different tasks, from recommending a product for its practical use to judging an aesthetic preference.'
if 'Reliance was about the same for both' not in a['options']: a['options'].append('Reliance was about the same for both')
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# the stronger number gate (negatives now checked) found axb01's g = −0.54 only in a location note: store the published sentence
ev = json.loads(ep.read_text())
q = {'source': 'vaccaro24', 'quote': 'But when the AI alone outperformed the human alone, performance losses occurred in the combined system relative to the AI alone, with a negative effect size for human–AI synergy of g = −0.54',
     'location': 'Results, moderators; Nature Human Behaviour, published article (Europe PMC full text, PMC11659167)'}
if not any(e.get('quote') == q['quote'] for e in ev['axb01']): ev['axb01'].append(q)
ep.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
# minor 6: option form carries no clue (a keyed option is never the only two-part one); edits by text (I11)
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
def swap(cid, old, new):
    c = C[cid]; c['options'] = [new if o == old else o for o in c['options']]
swap('biz02', 'Few employees knew they could change it', 'Few employees knew they could change it, and few asked')
swap('social14', 'Both sides said they mainly feared being rejected', 'Both sides feared rejection; neither lacked interest')
swap('axb02', 'Could adjust each forecast by up to 2', 'Could adjust each forecast, but only by up to 2')
swap('bz15', 'Opt-in (default: not a donor)', 'Opt-in (default: non-donor)')
swap('dimant-hate-choice', 'Expecting the other side not to cooperate', 'Low expectations of the other side’s cooperation')
swap('genai3', 'Human replies feel more heard, whatever the label', 'Human replies feel more heard; the label changes nothing')
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
swap('axb02', 'Could adjust each forecast, but only by up to 2', 'Could adjust each forecast, though by up to 2')
swap('genai3', 'Human replies feel more heard; the label changes nothing', 'Human replies feel more heard; the label matters little')
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# minor 11: the headline states the finding
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
C['ai11']['answerTitle'] = 'People relied on algorithms less for matters of taste'
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# audit 29, M1 and M2: a distractor must be false by the item's own evidence; the two new ones were the papers' findings
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
swap('social01', 'The average of what others did explained choices', 'Polarized norms pulled choices toward the middle')
swap('social14', 'Both sides feared rejection; neither lacked interest', 'Each side blamed its own lack of interest')
swap('axb02', 'Could adjust each forecast, though by up to 2', 'Could adjust each forecast by up to 2 points')
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
swap('axb02', 'Could adjust each forecast by up to 2 points', 'Could adjust each forecast by up to 2')
swap('axb02', 'Could not change the model at all', 'Had to use the model’s forecasts unchanged')
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# re-audit 29b: axb02's keyed option reads with its question and matches its chart; social14 regains a two-part distractor the evidence contradicts
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
swap('axb02', 'Had to use the model’s forecasts unchanged', 'Could use the model only unchanged')
ch = C['axb02']['chart']; ch['labels'][0] = 'Could use the model only unchanged'; ch['highlight'] = 0
swap('social14', 'Each side said it feared open conflict', 'Own side lacks interest; other fears conflict')
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
