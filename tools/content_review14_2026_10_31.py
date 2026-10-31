"""Fixes from independent review 14 (2026-10-31). Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
# minor 2: no "not stated" sample lines
C['dimant-notalie-causal']['study']['n'] = 'Participants in an incentivized experiment'
C['social20']['study']['n'] = ''
# minor 3: the scene states that players could also take from the charity
C['dimant-observability-choice']['scene'] = 'To boost charity giving, an experiment let another person observe each decision to give to a charity or take from its account. In some versions the observer simply watched, with no rewards or consequences attached.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
# minor 4: causal items whose visible diagram rules a distractor out
c = C['axe12']
if any(n['id'] == 'quality' for n in c['dag']['nodes']):
    c['dag']['nodes'] = [n for n in c['dag']['nodes'] if n['id'] != 'quality']
    c['dag']['edges'] = [e for e in c['dag']['edges'] if 'quality' not in e[:2]]
    c['dag']['alt'] = re.sub(r'[^.]*[Ww]ork quality[^.]*\.\s*', '', c['dag']['alt']).strip() or 'Using AI leads raters to see a worker as lazy, which lowers the rating.'
c = C['dimant-notalie-causal']
c['options'] = [{'The belief is accurate information that drives lying': 'A taste for risk drives both the belief and lying'}.get(o, o) for o in c['options']]
c = C['bz01']
if c['format'] == 'causal':   # every node was visible, and the confounder gave the answer away: a plain call instead
    c['format'] = 'choice'; c.pop('dag', None)
# minor 5: scene and option cues
C['dimant-conspiracy-choice']['scene'] = 'In a multi-round sharing task, participants chose whether to share factual news or conspiracy theories, including ones they did not believe.'
c = C['dimant-conspiracy-choice']; c['options'] = [{'Low digital literacy among sharers': 'A hunch that the posts might be true after all'}.get(o, o) for o in c['options']]
c = C['ai12']; c['options'] = [{'It costs more than a human doctor': 'It feels less accountable when it errs'}.get(o, o) for o in c['options']]
# forecasts resolve both ways inside each path
F = {
 'opposing-views-bot': ('Republicans who followed a liberal bot became more liberal afterward.', False),
 'axb07': ('People told AI-written from human-written self-descriptions apart well above chance.', False),
 'axe10': ('In the live ad test, the human-made image beat the AI-generated images on click-through rate.', False),
 'bz09': ('A photo of an attractive woman raised loan demand far less than a 25% interest-rate cut did.', False),
}
for k, (claim, truth) in F.items(): C[k]['forecast'] = {'claim': claim, 'truth': truth}
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok2')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
d = C['axe12']['dag']; d['alt'] = 'Disclosed AI use leads raters to see the worker as lazy, which lowers the rating, even when the work is held constant.'
for n in d['nodes']: n['y'] = 100
d['height'] = 160
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok3')
