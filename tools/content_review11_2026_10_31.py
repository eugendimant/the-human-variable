"""Fixes from independent review 11 (2026-10-31). Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
ev = json.loads((ROOT / 'src/evidence.json').read_text())
# M1: the 2019 contagion paper and the 2022 proximity paper agree once the designs are told apart
c = C['dimant-contagion-multi']
c['sources'] = ['contagion19']
c['implication'] = 'In tight-knit teams people copy what close peers do, and bad conduct most of all: act on visible misconduct quickly and make good conduct just as visible.'
REC = {'q': 'Does the 2022 proximity study say the same?', 'a': 'It fits. Here closeness meant being near the observed peer, and close peers’ bad choices spread most. In Bicchieri, Dimant, Gächter and Nosenzo (2022), a minimal shared-identity cue made people copy good examples as well as bad ones, which halted the erosion of compliance.'}
if not any(f['q'] == REC['q'] for f in c['follow']): c['follow'].append(REC)
c = C['dimant-proximity-estimate']
REC2 = {'q': 'Does this match Dimant’s 2019 contagion study?', 'a': 'Yes. Both find that people copy bad examples more readily than good ones. Here a minimal shared-identity cue made good examples spread too; in the 2019 study, closeness to the observed peer amplified the spread of bad choices.'}
if not any(f['q'] == REC2['q'] for f in c['follow']): c['follow'].append(REC2)
ev['dimant-proximity-estimate'] = [q for q in ev['dimant-proximity-estimate'] if q['quote'] != 'Observation, p < 0.001']
# M2: 33.9% is the arm with a prompt-engineering overview
c = C['axb14']
c['explain'] = 'Consultants with GPT-4 completed 12.2% more tasks and worked 25.1% faster. Graded quality rose 33.9% with GPT-4 and a prompt-engineering overview, and 29.9% with GPT-4 alone.'
ev['axb14'] = [q for q in ev['axb14'] if not q['quote'].startswith('representing a 33.9% increase')]
for q in ('GPT + overview leads to a 1.48 increase in scores over the control mean of 4.37, representing a 33.9% increase, with GPT only producing a 1.31 (or 29.9%) increase.',):
    if not any(x['quote'] == q for x in ev['axb14']): ev['axb14'].append({'source': 'dell26', 'quote': q, 'location': 'Section 4.1, Inside the frontier'})
# minor 4: distractor cues
def swap(cid, old, new): C[cid]['options'] = [new if o == old else o for o in C[cid]['options']]
swap('biz05', 'Heavy users raised their use after feedback', 'Descriptive feedback alone kept low users steady')
swap('genai1', 'Peers rated their work lower', 'Prior originality decided who gained')
swap('judg02', 'Every loss must hurt twice as much as a matching gain', 'Loss aversion held steady when gamble ranges changed')
swap('social13', 'Favorable to women, some with large standard errors', 'Favorable to women, with imprecise estimates')
# minor 2: predictions and famous results that held, so a framed prediction is not a cue for "false"
SCENE = {
 'axb13': 'A firm rolls out a generative-AI assistant that suggests replies to its customer-support agents, in stages across 5,172 agents. The support director predicts calmer customers.',
 'dimant-opioid-forecast': 'A program paid US veterans cash to return unused opioid pills. Researchers randomly added two reminder cards built on timely reminders, planning prompts and loss framing. The program director expects the cards to pay for themselves.',
 'axe10': 'Researchers generated 10,320 marketing images with seven text-to-image models from 2,400 human-made images, then ran a live ad test with over 173,000 impressions. The creative team predicts a machine-made image can win.',
 'bz08': 'In a famous field experiment, ten Israeli day-care centers tracked late pickups for 20 weeks. In week 5, six centers began fining parents NIS 10 for arriving 10+ minutes late. In week 17 the fine was dropped.',
}
for k, s in SCENE.items(): C[k]['scene'] = s
# minor 9
st = C['axb05'].get('study', {})
pass  # study line joins design and sample as sentences (app.js studyLine)
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')

# M2 (extended): numbers in follow-up answers appear in quotes too
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
ev = json.loads((ROOT / 'src/evidence.json').read_text())
def add(cid, src, quote, loc):
    if not any(q.get('quote') == quote for q in ev.setdefault(cid, [])): ev[cid].append({'source': src, 'quote': quote, 'location': loc})
add('social15', 'hate23', 'comprising 15 well-powered behavioral experiments and a diverse set of over 8,600 participants.', 'Abstract')
add('social16', 'hate23', 'comprising 15 well-powered behavioral experiments and a diverse set of over 8,600 participants.', 'Abstract')
add('rollout3', 'dell26', 'Preregistered field experiment with 758 BCG consultants', 'Design (journal PDF)')
add('genai1', 'zhou24', 'our research shows that over time, text-to-image AI significantly enhances human creative productivity by 25%', 'Abstract')
add('forecast-teams-rank', 'mellers14', 'Eighty-five and 114 questions closed and were included in the Brier scores in Years 1 and 2, respectively', 'Method')
add('forecast-teams-rank', 'mellers14', 'Year 1 began with 2,246 participants', 'Method')
def fol(cid, q, a):
    for f in C[cid]['follow']:
        if f['q'] == q: f['a'] = a
fol('ai01', 'Did people keep using it?', 'Yes. Two weeks and two months later, people who had ChatGPT access were more likely to report using it in their real jobs.')
fol('axb08', 'Could people tell they faced an AI?', 'Often. Participants identified AI opponents in about three of four cases; for human opponents, identification was near chance.')
fol('bz02', 'How much spending was tested?', 'The experiments represented $2.8 million in digital advertising expenditure.')
fol('bz04', 'How far off was the average?', 'Students predicted 33.9 days on average; actual completion took about three weeks longer.')
fol('bz11', 'When was the original retracted?', 'PNAS retracted the original paper in 2021.')
fol('truth-telling-gains', 'How large is the evidence base?', 'Experimental studies from economics, psychology and sociology, covering 270,616 decisions by 44,390 subjects.')
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('follow numbers ok')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
for f in C['forecast-teams-rank']['follow']:
    f['a'] = f['a'].replace('of 199 questions posted, 85 (Year 1)', 'of 199 questions posted, eighty-five (Year 1)')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
# minor 8: provenance labels say what was read
bank = json.loads((ROOT / 'src/bank.json').read_text()); S = bank['sources']
S['plural24']['verification']['text_read'] = 'Full text (OUP HTML version of record); quoted sentences rechecked verbatim on 2026-10-31'
S['hui24']['verification']['text_read'] = 'Published abstract, as indexed word by word in the OpenAlex record of the Organization Science article'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
bank = json.loads((ROOT / 'src/bank.json').read_text())
for s in bank['sources'].values():   # RULE G: every source with the same label
    v = s.get('verification', {})
    if v.get('text_read') == 'Abstract reconstructed from OpenAlex record': v['text_read'] = 'Published abstract, as indexed word by word in its OpenAlex record'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
