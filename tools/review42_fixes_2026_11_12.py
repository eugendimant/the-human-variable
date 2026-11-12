"""Review 42 fixes (iteration 67): wrong figure note on dimant-hate-choice (M-3), the deterrence item's parallel options and scope (m-1, m-2),
competition option and caution (m-3), exploratory results (m-4), 'at least largely reproduced' (m-5), two quotes made verbatim (m-6),
an invented plan sentence in rollout4, 'blind' in ai02 (I-4). Idempotent. Every quote below was read in the published article (owner's PDF copies), 2026-11-12."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}
ep = ROOT / 'src/evidence.json'; E = json.loads(ep.read_text())
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())

def swap(obj, key, old, new):
    if new in obj[key]: return
    assert old in obj[key], (key, old); obj[key] = obj[key].replace(old, new)
def quote(cid, source, q, loc, replace=None):
    L = E[cid]
    if any(e['quote'] == q for e in L): return
    if replace:
        i = next(i for i, e in enumerate(L) if e['quote'] == replace); L[i] = {'source': source, 'quote': q, 'location': loc}
    else: L.append({'source': source, 'quote': q, 'location': loc})

# M-3: the plotted quantity is the share of conditional cooperators (Dimant 2024, Figures 5 and 6)
c = C['dimant-hate-choice']
c['chart']['note'] = 'Share of conditional cooperators, who cooperate if the partner does. The drop is about as large for a painting-taste outgroup as for a political one.'
quote('dimant-hate-choice', 'hate23', 'ingroup-love occurs in the perceptional domain (how close one feels toward others), whereas outgroup-hate occurs in the behavioral domain (how one helps/harms/cooperates with others).', 'Published abstract',
      replace='ingroup-love occurs in the perceptional domain whereas outgroup-hate occurs in the behavioral domain (how one helps/harms/cooperates with others).')
# m-6: the masks quote restored in full
quote('dimant-masks-forecast', 'masks22', 'negative and statistically significant for Democrat predictions (r(28) = −0.63, t(26) = −4.12, p = 0.0003)', 'Published version of record, Results',
      replace='negative and statistically significant for Democrat predictions (r(28) = -0.63, p = 0.0003)')

# m-1, m-2: deterrence. Four parallel clauses; the delay lasted two rounds; fines in experimental currency
c = C['dimant-deterrence-choice']
c['scene'] = 'In a lab experiment, 296 people played a card game for money and could cheat in some rounds. Cheaters were detected and fined with a set probability. The researchers varied whether people learned the verdict right away or two rounds later, and whether the fine followed right away or two rounds after that.'
c['options'] = ['Deterrence rose steadily the sooner the verdict and the fine came',
                'Deterrence rose steadily the later the verdict and the fine came',
                'Deterrence was best when the verdict or the fine, but not both, came late',
                'Deterrence was best with no delay or with the longest delay']
c['answer'] = 3
c['boundary'] = 'A laboratory cheating game in one session: delays of two rounds, and fines in experimental currency.'
c['implication'] = 'When you design a compliance process, keep the verdict and the sanction on one clock. In this lab game, a quick verdict with a slow penalty gave away deterrence.'
for f in c['follow']:
    if f['q'] == 'What exactly was delayed?': f['a'] = 'Two things: when people learned whether they would be punished, and when the punishment was imposed. Each delay lasted two rounds.'
quote('dimant-deterrence-choice', 'buck21', 'Resolution of uncertainty regarding whether cheating is detected (and hence whether there are sanctions) is either immediate (IR) or delayed by two periods (DR).', 'Section 2.2 (version of record)')
quote('dimant-deterrence-choice', 'buck21', 'Relative to the timing of resolution of uncertainty, punishment is either immediate (no delay or ND) or delayed by 2 rounds (delayed or D).', 'Section 2.2 (version of record)')
quote('dimant-deterrence-choice', 'buck21', 'A subject received 10 Experimental Currency Units (ECU) for a correct guess and 4 ECU for an incorrect guess.', 'Section 2.1 (version of record)')
K['dimant-deterrence-choice'] = {'keyed': [c['options'][3]], 'options': sorted(c['options'])}

# m-3: competition. One distractor now tests the heterogeneity half; the follow-up carries the authors' caution
c = C['dimant-competition-choice']
c['options'][3] = 'A small adverse effect, and the designs agreed closely'
for f in c['follow']:
    if f['q'] == 'How sure is the direction of the effect?':
        f['a'] = 'The 95% interval runs from −0.147 to −0.022 standard deviations, so it excludes zero but stays small. The authors call it suggestive evidence of an adverse effect.'
quote('dimant-competition-choice', 'huber23', 'There is suggestive evidence of an adverse effect of competition on moral behavior in the meta-analysis (d = −0.085, 95% CI [−0.147, −0.022], P = 0.008).', 'Figure 2 caption (version of record)')
K['dimant-competition-choice'] = {'keyed': [c['options'][2]], 'options': sorted(c['options'])}

# m-4: exploratory analyses
c = C['dimant-megastudy-estimate']
swap(c, 'explain', 'Any behaviorally informed nudge raised progress by 1.89% on average, and emails', 'In exploratory analyses, any behaviorally informed nudge raised progress by 1.89% on average, and emails')
for f in c['follow']:
    if f['q'] == 'Did personal data help?': f['a'] = 'In exploratory analyses, yes. Emails that cited classroom-specific statistics outperformed emails that did not by 2.26%.'
quote('dimant-megastudy-estimate', 'duckworth25', 'In exploratory analyses, teachers who received any behaviorally informed email nudge (vs. a reminder-only megastudy control) saw their students’ math progress boosted by an average of 1.89% during the 4-wk intervention period; emails referencing personalized data (i.e., classroom-specific statistics) outperformed emails that did not by 2.26%.', 'Abstract (version of record)')

# m-5: 'at least largely reproduced'
c = C['repro-msci-estimate']
c['question'] = 'Of all articles published under the new policy, what share could be at least largely reproduced?'
c['answerTitle'] = 'About 68% could be at least largely reproduced'
c['estimate']['label'] = 'Share at least largely reproduced'
swap(c, 'explain', 'which brings the share across all articles to 68%', 'which brings the share across all articles to about 68% that could be at least largely reproduced')
quote('repro-msci-estimate', 'fisar24', 'about 68% could be at least largely reproduced', 'Introduction (version of record)')

# rollout4: the invented plan sentence leaves; ai02: nothing stored says the graders were blind
swap(C['rollout4'], 'scene', ' Your plan gives new hires the same unrestricted access.', '')
swap(C['ai02'], 'scene', 'graded the finished work blind.', 'graded the finished work.')

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(E, ensure_ascii=False, indent=1) + '\n'); kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('ok')
