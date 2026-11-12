"""Four decisions from papers in the owner's own folder (iteration 67). Idempotent.
Every number was read in the published article (owner's PDF copies), 2026-11-12."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text()); C = {c['id']: c for c in B['challenges']}
ep = ROOT / 'src/evidence.json'; E = json.loads(ep.read_text())
kp = ROOT / 'tests/keyed_options.json'; K = json.loads(kp.read_text())
V = lambda what: {'status': 'verified_full_text', 'checked': '2026-11-12', 'metadata': 'matched Crossref record', 'text_read': what, 'text_url': None}
SRC = {
 'fisar24': dict(authors='Fišar, Greiner, Huber, Katok, Ozkes & the Management Science Reproducibility Collaboration', year=2024, title='Reproducibility in Management Science', venue='Management Science', doi='10.1287/mnsc.2023.03556', volume='70(3)', pages='1343-1356',
                 takeaway='Under a data and code disclosure policy, 68% of all articles and more than 95% of those with accessible data could be reproduced.'),
 'huber23': dict(authors='Huber et al.', authors_full='Huber, Dreber, Huber, Johannesson, Kirchler, Weitzel and co-authors, including Dimant', year=2023, title='Competition and moral behavior: A meta-analysis of forty-five crowd-sourced experimental designs', venue='Proceedings of the National Academy of Sciences', doi='10.1073/pnas.2215572120', volume='120(23)', pages='e2215572120',
                 takeaway='Across 45 crowd-sourced designs, competition had a small adverse effect on moral behavior, and effects varied widely by design.'),
 'duckworth25': dict(authors='Duckworth et al.', authors_full='Duckworth, Ko, Milkman, Kay, Dimant, Gromet and co-authors', year=2025, title='A national megastudy shows that email nudges to elementary school teachers boost student math achievement, particularly when personalized', venue='Proceedings of the National Academy of Sciences', doi='10.1073/pnas.2418616122', volume='122(13)', pages='e2418616122',
                 takeaway='In a megastudy with 140,461 teachers, the best email nudge raised students’ math progress by 5.06%, or 3.30% after a winner’s-curse adjustment.'),
 'buck21': dict(authors='Buckenmaier, Dimant, Posten & Schmidt', year=2021, title='Efficient Institutions and Effective Deterrence: On Timing and Uncertainty of Formal Sanctions', venue='Journal of Risk and Uncertainty', doi='10.1007/s11166-021-09352-x', volume='62(2)', pages='177-201',
                 takeaway='In a lab cheating game, either no delay or maximum delay of the verdict and the fine deterred cheating most.'),
}
for sid, s in SRC.items():
    if sid not in B['sources']:
        v = V('full text of the published article (PDF copy supplied by Eugen Dimant)'); v['text_url'] = 'https://doi.org/' + s['doi']
        B['sources'][sid] = {'id': sid, **s, 'url': 'https://doi.org/' + s['doi'], 'kind': 'peer-reviewed', 'verification': v}
NEW = [
 dict(id='repro-msci-estimate', format='estimate', track='Business', concept='Reproducibility', theme='evidence', title='Can the result be rerun?',
      scene='More than 700 reviewers tried to reproduce the results of nearly 500 Management Science articles from the authors’ data and code. Since 2019 the journal requires authors to disclose both.',
      question='Of all articles published under the new policy, what share could be reproduced?',
      estimate={'target': 68, 'min': 0, 'max': 100, 'tolerance': 6, 'label': 'Share of articles reproduced', 'unit': '%'},
      answerTitle='68% could be reproduced',
      explain='When data access and hardware or software were no obstacle, the results of more than 95% of articles under the new policy could be fully or largely reproduced. For 29% of articles at least part of the data set was not accessible to the reviewer, which brings the share across all articles to 68%. Before the policy, only 12% of articles provided replication materials, and 55% of those could be reproduced.',
      implication='Before you act on an analysis, ask for the data and code behind it. A disclosure rule made most results checkable.',
      boundary='Computational reproducibility for articles in one journal: rerunning the authors’ data and code to get the same results.',
      sources=['fisar24'], study={'design': 'Reproduction attempts by more than 700 reviewers', 'n': 'Nearly 500 articles in Management Science'},
      follow=[{'q': 'What stopped the failed attempts?', 'a': 'Mostly data the reviewer could not access. Other reasons were missing code, unresolvable code errors, weak or missing documentation, and software and hardware requirements.'},
              {'q': 'How did things look before the policy?', 'a': 'Only 12% of articles voluntarily provided replication materials, and 55% of those could be largely reproduced.'},
              {'q': 'Is reproduced the same as replicated?', 'a': 'No. A reproduction reruns the authors’ own data and code. A replication collects new data.'}]),
 dict(id='dimant-competition-choice', format='choice', track='Business', concept='Competition and morals', theme='evidence', title='Does competition corrupt?',
      scene='Independent research teams submitted 95 experimental designs to test whether competition changes moral behavior. Researchers drew 45 of them at random and ran them with 18,123 online participants.',
      question='What did the pooled data show?',
      options=['A large adverse effect, and the designs agreed closely', 'A small favorable effect, and the designs disagreed widely', 'A small adverse effect, and the designs disagreed widely', 'A large favorable effect, and the designs agreed closely'], answer=2,
      answerTitle='A small adverse effect, and designs disagreed',
      explain='Pooled over the 45 designs, competition lowered moral behavior by 0.085 standard deviations (95% confidence interval: −0.147 to −0.022). Effects varied across designs about 1.6 times as much as the sampling noise in one design’s estimate, so a single experiment says little about the general effect.',
      implication='Do not build a policy on one experiment’s design. Test the claim in several designs before you treat it as a rule.',
      boundary='Online experiments; each design was one research team’s way of measuring competition and moral behavior.',
      sources=['huber23'], study={'design': 'Crowd-sourced meta-analysis of 45 experimental designs', 'n': '18,123 online participants'},
      follow=[{'q': 'What is design heterogeneity?', 'a': 'Variation in true effect sizes across reasonable ways of running the same test.'},
              {'q': 'Where did the designs come from?', 'a': 'Independent research teams submitted 95 designs, and 45 were drawn at random.'},
              {'q': 'How sure is the direction of the effect?', 'a': 'The 95% interval runs from −0.147 to −0.022 standard deviations, so it excludes zero but stays small.'}]),
 dict(id='dimant-megastudy-estimate', format='estimate', track='Business', concept='Megastudy nudges', theme='evidence', title='Fifteen nudges, one winner',
      scene='In a megastudy, 140,461 elementary school teachers of 2,992,027 students were randomly assigned weekly emails for four weeks: one of 15 behaviorally informed nudges, or a plain reminder.',
      question='By how much did the best nudge raise students’ math progress, compared with the reminder?',
      estimate={'target': 5, 'min': 0, 'max': 40, 'tolerance': 2, 'label': 'Increase in math progress', 'unit': '%'},
      answerTitle='The best nudge added about 5%',
      explain='The best email invited teachers to log in for an updated report on how their students were doing that week. It raised math progress by 5.06%, or 3.30% after accounting for the winner’s curse. Any behaviorally informed nudge raised progress by 1.89% on average, and emails with classroom-specific data beat the others by 2.26%.',
      implication='Expect small gains from one nudge. Test many versions at once, and discount the winner’s result before you scale it.',
      boundary='Emails to US elementary school teachers on one math platform, Zearn Math, in fall 2021. Progress was measured on the platform.',
      sources=['duckworth25'], study={'design': 'National megastudy, randomized', 'n': '140,461 teachers of 2,992,027 students'},
      follow=[{'q': 'What is the winner’s curse here?', 'a': 'The best of many options looks better than it is, partly by luck. Adjusted for that, the top nudge’s gain was 3.30%.'},
              {'q': 'Did personal data help?', 'a': 'Yes. Emails that cited classroom-specific statistics outperformed emails that did not by 2.26%.'},
              {'q': 'Did the effect last?', 'a': 'Yes. The effects persisted in the 8-week period after the intervention.'}]),
 dict(id='dimant-deterrence-choice', format='choice', track='Culture & Society', concept='Swift sanctions', theme='honesty', title='Punish now or later?',
      scene='In a lab experiment, 296 people played a card game for money and could cheat in some rounds. Cheaters were detected and fined with a set probability. The researchers varied how soon people learned the verdict and how soon the fine was imposed.',
      question='Which timing deterred cheating best?',
      options=['The faster the verdict and the fine, the stronger the deterrence', 'An immediate verdict with a delayed fine', 'Verdict and fine both immediate, or both delayed as far as possible', 'The longer the verdict and the fine were delayed, the stronger the deterrence'], answer=2,
      answerTitle='No delay or full delay worked best',
      explain='Among 296 participants, deterrence did not rise or fall steadily with delay. Either no delay, with the verdict and the fine both immediate, or maximum delay, with both pushed back as far as possible, was most effective at deterring cheating and repeat cheating.',
      implication='When you design a compliance process, set the verdict and the sanction on the same clock. A quick verdict with a slow penalty gives away deterrence.',
      boundary='A laboratory cheating game with monetary fines.',
      sources=['buck21'], study={'design': 'Laboratory experiment with a cheating game', 'n': '296 participants'},
      follow=[{'q': 'What was new in this study?', 'a': 'It is the first controlled experiment on the swiftness of formal sanctions, next to their severity and certainty.'},
              {'q': 'Did timing also affect repeat cheating?', 'a': 'Yes. The same two timings were most effective against recidivism.'},
              {'q': 'What exactly was delayed?', 'a': 'Two things: when people learned whether they would be punished, and when the punishment was imposed.'}]),
]
have = set(C)
for c in NEW:
    if c['id'] not in have: B['challenges'].append(c)
    else: C[c['id']].clear(); C[c['id']].update(c)
    if c['format'] == 'choice': K[c['id']] = {'keyed': [c['options'][c['answer']]], 'options': sorted(c['options'])}
P = {p['id']: p for p in B['paths']}
for pid, ids in (('measure', ['repro-msci-estimate', 'dimant-competition-choice', 'dimant-megastudy-estimate']), ('dimant-lab', ['dimant-deterrence-choice'])):
    for i in ids:
        if i not in P[pid]['ids']: P[pid]['ids'].insert(P[pid]['ids'].index('bz10'), i) if i == 'dimant-megastudy-estimate' else P[pid]['ids'].append(i)
Q = {
 'repro-msci-estimate': [('fisar24', 'With the help of more than 700 reviewers, we assess the reproducibility of nearly 500 articles published in the journal Management Science before and after the introduction of a new Data and Code Disclosure policy in 2019.', 'Abstract'),
   ('fisar24', 'the results of more than 95% of articles under the new disclosure policy could be fully or largely computationally reproduced. However, for 29% of articles, at least part of the data set was not accessible to the reviewer.', 'Abstract'),
   ('fisar24', 'Considering all articles in our sample reduces the share of reproduced articles to 68%.', 'Abstract'),
   ('fisar24', 'where only 12% of articles voluntarily provided replication materials, of which 55% could be (largely) reproduced.', 'Abstract'),
   ('fisar24', 'Other reasons for unsuccessful reproduction attempts include missing code, unresolvable code errors, weak or missing documentation, and software and hardware requirements and code complexity.', 'Abstract')],
 'dimant-competition-choice': [('huber23', 'In a large-scale online data collection, 18,123 experimental participants were randomly allocated to 45 randomly selected experimental designs out of 95 submitted designs.', 'Abstract'),
   ('huber23', 'We find a small adverse effect of competition on moral behavior in a meta-analysis of the pooled data.', 'Abstract'),
   ('huber23', 'The meta-analytic effect size in Cohen’s d units is −0.085 (95% CI [−0.147, −0.022], P = 0.008) for analytic approach A and −0.086 (95% CI [−0.144, −0.027], P = 0.004) for analytic approach B.', 'Results'),
   ('huber23', 'We find substantial design heterogeneity—estimated to be about 1.6 times as large as the average standard error of effect size estimates of the 45 research designs', 'Abstract'),
   ('huber23', 'A potential source of ambivalent empirical results on the same hypothesis is design heterogeneity—variation in true effect sizes across various reasonable experimental research protocols.', 'Abstract')],
 'dimant-megastudy-estimate': [('duckworth25', 'we conducted a national megastudy in which 140,461 elementary school teachers who collectively taught 2,992,027 students were randomly assigned to receive a variety of behaviorally informed email nudges', 'Abstract'),
   ('duckworth25', 'Specifically, we partnered with the nonprofit educational platform Zearn Math to compare the impact of 15 different interventions with a reminder-only megastudy control condition.', 'Abstract'),
   ('duckworth25', 'All 16 conditions entailed weekly emails delivered to teachers over 4-wk in the fall of 2021.', 'Abstract'),
   ('duckworth25', 'The best-performing intervention, which encouraged teachers to log into Zearn Math for an updated report on how their students were doing that week, produced a 5.06% increase in students’ math progress (3.30% after accounting for the winner’s curse).', 'Abstract'),
   ('duckworth25', 'saw their students’ math progress boosted by an average of 1.89% during the 4-wk intervention period; emails referencing personalized data (i.e., classroom-specific statistics) outperformed emails that did not by 2.26%.', 'Abstract'),
   ('duckworth25', 'these intervention effects were consistent across school socioeconomic status and school type (public, private, etc.) and, further, persisted in the 8-wk post-intervention period.', 'Abstract')],
 'dimant-deterrence-choice': [('buck21', 'This paper presents the first controlled experiment to study a third important factor that has been mainly overlooked: the swiftness of formal sanctions.', 'Abstract'),
   ('buck21', 'we find a surprising non-monotonic relation with deterrence: either no delay (immediate resolution and immediate punishment) or maximum delay (both resolution and punishment as much as possible delayed) emerge as most effective at deterring deviant behavior and recidivism.', 'Abstract'),
   ('buck21', 'A total of 296 subjects (46.6% male) participated in the experiment', 'Section 2'),
   ('buck21', 'These cheating periods are followed by an investigation such that cheaters will be detected and fined with a given probability.', 'Section 1')],
}
for cid, qs in Q.items():
    E[cid] = []
    for s, q, loc in qs:
        if not any(x.get('quote') == q for x in E[cid]): E[cid].append({'source': s, 'quote': q, 'location': loc + ' (version of record)'})
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(E, ensure_ascii=False, indent=1) + '\n'); kp.write_text(json.dumps(K, ensure_ascii=False, indent=1) + '\n')
print('owner papers applied:', len(NEW), 'decisions')
