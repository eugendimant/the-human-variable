"""Review 33 content fixes. Idempotent; edits by text, never by index."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}

def rep(cid, field, old, new):
    C[cid][field] = C[cid][field].replace(old, new)

# m2: sample sizes, test statistics and "n.s." in plain words
rep('biz04', 'explain', 'In the first (N = 724),', 'In the first, with 724 observations,')
rep('bz11', 'explain', 'Across five conceptual replications (n = 4,559) and a preregistered direct replication (n = 1,235),', 'Across five conceptual replications with 4,559 participants and a preregistered direct replication with 1,235,')
rep('axe12', 'explain', 'In Study 2 (n = 1,203),', 'In Study 2, with 1,203 participants,')
rep('dimant-conspiracy-choice', 'explain', 'Ren, Dimant and Schweitzer (N = 4,128) show', 'With 4,128 participants, Ren, Dimant and Schweitzer show')
rep('axe07', 'explain', 'Across nine studies (N = 4,820),', 'Across nine studies with 4,820 participants,')
for c in B['challenges']:
    a = c.get('allocate') or {}
    if a.get('valueLabels'): a['valueLabels'] = [v.replace(' (n.s.)', ' (not significant)') for v in a['valueLabels']]
rv = C['forecast-teams-rank'].get('rankValues') or []
C['forecast-teams-rank']['rankValues'] = [v.replace('Beat independents, t(1120) = 5.92', 'More accurate than independents').replace('Beat crowd-belief, t(1036) = 5.52', 'More accurate than crowd-belief') for v in rv]
C['forecast-teams-rank']['rankLabel'] = C['forecast-teams-rank']['rankLabel'].replace('Forecast accuracy (Brier scores)', 'Forecast accuracy')   # no Brier values are drawn (m7)
ch = C['facebook-deactivation']['chart']
if ch.get('unit') == ' SD': ch['unit'] = ''   # the note names the unit once
# m8: both of facebook-deactivation's proofs carry the evidence colour
ch['highlight'] = 0   # rule 29 (one amber mark per chart) wins over review 33 m8; the headline's first finding carries the colour
# m11 (RULE G): chart notes state the measure; citations stay in the source line
for c in B['challenges']:
    n = (c.get('chart') or {}).get('note')
    if n and 'Values reported in' in n: c['chart']['note'] = re.sub(r'\s*Values reported in [^.]*(\.[^.]*)?\.$', '', n).strip()
# m12: social13's key is no longer the only hedged option
o = C['social13']['options']
if 'Advancement unchanged by the screen' in o: o[o.index('Advancement unchanged by the screen')] = 'Little change in who advanced; several estimates imprecise'
# m13: the allocate instruction leaves the heading (the instrument says how to answer)
for cid in ('axb08', 'axf01'): rep(cid, 'question', ' Spread 100 points by how likely each is.', '')

ch = C['dimant-enforcers-rank']['chart']; ch['note'] = ch['note'].replace('Outlined: the equalizing-bribe difference (P = 0.074).', 'Outlined: the equalizing-bribe difference, the weaker of the two.')
ch = C['axf06']['chart']; ch['note'] = ch['note'].replace(' was not significant (P = .60).', ' was not statistically significant.')

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())
for c in B['challenges']:
    if c['id'] in K and c.get('options'):
        K[c['id']] = {'keyed': sorted(c['options'][i] for i in (c['multiAnswers'] if c['format'] == 'multi' else [c['answer']])), 'options': sorted(c['options'])}
kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('review 33 content applied')
