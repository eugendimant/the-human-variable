"""Rebalance formats: convert seven choice items whose evidence is a yes/no finding or a single number into forecasts and an estimate."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
def to_forecast(cid, claim, truth, scene=None):
    c = C[cid]
    if c['format'] == 'forecast': return
    for k in ('options', 'answer', 'multiAnswers'): c.pop(k, None)
    c['format'] = 'forecast'; c['question'] = 'Is this what the study found?'; c['forecast'] = {'claim': claim, 'truth': truth}
    if scene: c['scene'] = scene
to_forecast('social08', 'The behavior spread farther through networks with random long ties than through clustered networks with redundant ties.', False,
            'In an online health community, researchers built networks that were either clustered (neighbors share neighbors) or random (more long-range ties), then seeded a health behavior.')
to_forecast('biz06', 'Adding an approval cue (a smiley face) stopped already-efficient households from increasing their energy use.', True)
to_forecast('biz08', 'People juggling other tasks were more likely to find improvements that remove something.', False)
to_forecast('axb09', 'Labeling headlines “AI-generated” lowered belief in them even when the headlines were true and written by people.', True)
to_forecast('dimant-observability-choice', 'Simply letting another person watch each donation decision raised giving substantially.', False)
to_forecast('bz13', 'Where coworkers could not easily see who was more productive, paying them unequal wages raised output.', False)
c = C['ai10']
if c['format'] != 'estimate':
    for k in ('options', 'answer'): c.pop(k, None)
    c.update({'format': 'estimate', 'title': 'Advice from a person or a program',
              'scene': 'People estimated a person’s weight from a photo, then saw an advice estimate and could revise. The same advice was labeled as coming from other people for some and from an algorithm for others. With human-labeled advice, they moved 30% of the way toward it.',
              'question': 'How far did people move toward the same advice labeled as an algorithm’s?',
              'answerTitle': '45% of the way, versus 30% for human advice',
              'explain': 'Weight on advice averaged 0.45 when the advice was labeled algorithmic and 0.30 when labeled human, for identical advice.',
              'estimate': {'target': 45, 'min': 0, 'max': 100, 'tolerance': 7, 'label': 'Share of the distance moved toward algorithmic advice', 'unit': '%'},
              'chart': {'labels': ['Labeled as people', 'Labeled as an algorithm'], 'values': [30, 45], 'unit': '%', 'highlight': 1, 'note': 'Logg, Minson & Moore (2019), Experiment 1A, weight on advice.'}})
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
