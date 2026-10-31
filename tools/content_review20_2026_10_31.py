"""Review 20 content fixes (idempotent)."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
bp, ep = R / 'src/bank.json', R / 'src/evidence.json'
b = json.loads(bp.read_text()); ev = json.loads(ep.read_text())
C = {c['id']: c for c in b['challenges']}
# minor 2: the scene's control (74) must not land inside the target band (76)
C['axf06']['estimate']['tolerance'] = 1
# minor 3: no impossible negative half on the axis
for i in ('axb03', 'axb14'):
    C[i]['estimate'].update(min=0, max=40, tolerance=3)
# minor 8: the explanation must not carry a sample size the analysed result does not use
C['biz04']['explain'] = C['biz04']['explain'].replace('in the second (N = 204), ', 'in the second hotel, ')
# minor 9: the implication stays with what the study tested
C['opposing-views-bot']['implication'] = "Do not expect that feeding a divided team the other side's messages builds understanding."
# minor 11: a claim this specific reads as true; state it at the level of the finding
C['bz11']['forecast']['claim'] = 'The replications found no effect of signing first on honest reporting.'
# minor 7: store the bates17 finding the explanation relies on
q = {"source": "bates17", "quote": "Hypotheses that group-IQ increases with number of women in the group and with turn-taking were not supported.",
     "location": "Abstract, Intelligence (Bates & Gupta), published article PDF, doi:10.1016/j.intell.2016.11.004"}
for cid, c in C.items():
    if 'bates17' in c.get('sources', []) and not any(e.get('quote') == q['quote'] for e in ev.get(cid, [])):
        ev.setdefault(cid, []).append(q)
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
print('ok')
