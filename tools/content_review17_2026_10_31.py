"""Fixes from independent review 17 (2026-10-31). Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
ev = json.loads((ROOT / 'src/evidence.json').read_text())
def add(cid, q):
    if not any(x.get('quote') == q['quote'] for x in ev.setdefault(cid, [])): ev[cid].append(q)
# M1: Dimant & Gesche (2023): the nudge was injunctive (most previous participants objected to taking bribes);
# the outcome was the chosen likelihood that the coworker is punished, set by how much evidence people submitted
c = C['dimant-enforcers-rank']
c['scene'] = 'US adults read about a coworker accepting a bribe and chose how much evidence to submit, which set how likely the coworker was to be punished. The bribe either created inequity or restored equity; half also learned what most previous participants thought of taking bribes.'
c['forecast'] = {'claim': 'Telling people that most others object to taking bribes raised the punishment they chose for bribes that created inequity.', 'truth': True}
c['answerTitle'] = 'Norm information raised punishment of unfair bribes'
c['explain'] = 'Norm information raised the chosen probability of punishment from 73.3% to 82.8% when the bribe created inequity (P < 0.005), and from 57.9% to 67.2% when it restored equity (marginal, P = 0.074). Inequity-creating bribes drew more punishment overall (77.8% vs 62.3%, P < 0.001).'
c['implication'] = 'When you build a speak-up channel, tell staff that most colleagues object to taking bribes; in the study this raised willingness to act most for deals that create unfair advantages.'
c['chart']['note'] = 'Average chosen probability that the coworker is punished, Study 2 vignette.'
for q in ('information about the majority of participants in a previous study objecting to bribe acceptance',
          'They could choose among different actions (submitting varying amounts of evidence)'):
    add('dimant-enforcers-rank', {'source': 'enforcers23', 'quote': q, 'location': 'Study 2, Europe PMC full text, version of record'})
# minor 2: study lines without repeats
C['biz08']['study']['n'] = ''
C['dimant-notalie-causal']['study']['n'] = ''
# minor 5: every path mixes true and false forecasts
C['ai10']['forecast'] = {'claim': 'People moved further toward identical advice when it was labeled as other people’s rather than an algorithm’s.', 'truth': False}
# minor 9: credible rivals in social13
C['social13']['options'] = [{'Unfavorable to women, with tight estimates': 'Favorable to women, precisely estimated',
                             'Clear gains, precisely estimated across rounds': 'Mixed by round, precisely estimated'}.get(o, o) for o in C['social13']['options']]
# minor 10
C['dimant-proximity-estimate']['implication'] = 'Before publishing peer compliance dashboards, add even a minimal shared-identity cue among peers; without one, bad examples spread faster than good ones.'
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
# minor 6: numbers in scenes and scope lines are quoted too
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
ev = json.loads((ROOT / 'src/evidence.json').read_text())
def add(cid, src, q, loc):
    if not any(x.get('quote') == q for x in ev.setdefault(cid, [])): ev[cid].append({'source': src, 'quote': q, 'location': loc})
add('social01', 'norms24', 'through the lens of a well-powered (n = 1,203) and preregistered study.', 'Introduction, Management Science 71(3), published article as hosted by the coauthor; "=" restored from a replacement character')
add('axb14', 'dell26', 'For each one of a set of 18 realistic knowledge tasks within the frontier of AI capabilities', 'Abstract, Organization Science, version of record (Crossref)')
add('rollout4', 'bastani25', 'We conducted four 90-min sessions for about fifty 9th, 10th, and 11th-grade classes, comprising nearly 1,000 students.', 'Methods, PNAS, Europe PMC full text, version of record')
add('civic-wallet-experts', 'cohn19', 'rising from 40% in the NoMoney condition to 51% in the Money condition', 'Science 365(6448), published article')
add('dimant-enforcers-rank', 'enforcers23', 'The Punisher Experiment featured n=1,240 subjects.', 'Methods, Europe PMC full text, version of record')
add('axf05', 'jabbour23', 'Four hundred fifty-seven clinicians were randomized and completed at least 1 vignette,', 'Abstract, JAMA (Europe PMC record)')
C['rollout1']['scene'] = 'A firm rolled out a generative-AI reply assistant to its customer-support agents in waves. You decide which agents get the first licenses.'
C['bz04']['boundary'] = re.sub(r'tracked 37 psychology honors students', 'tracked psychology honors students', C['bz04']['boundary'])
C['truth-telling-gains']['scene'] = C['truth-telling-gains']['scene'].replace('Across 90 experiments', 'Across many experiments')
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok2')
