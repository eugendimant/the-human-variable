"""Merge the verified drafts (clusters A-D) into src/bank.json, retire weak items, assign themes and paths.
Idempotent on a fresh copy of the iteration-3 bank. Evidence quotes go to src/evidence.json (not embedded in the page)."""
import json, sys, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
D = Path(sys.argv[1])
bank = json.loads((ROOT / 'src/bank.json').read_text())
evidence = json.loads((ROOT / 'src/evidence.json').read_text()) if (ROOT / 'src/evidence.json').exists() else {}
log = []
C = {c['id']: c for c in bank['challenges']}

RETIRE = {
 'biz09': 'Duplicate of judg05 framing item; concept label only.', 'biz10': 'Advice the paper did not test as a remedy.',
 'biz12': 'Concept-label question with a non-serious distractor.', 'biz13': 'Concept-label question; no measured outcome.',
 'biz14': 'Concept-label question; no measured outcome.', 'judg01': 'Concept-label question.', 'judg03': 'Concept-label question.',
 'judg04': 'Advice the paper did not test as a remedy.', 'judg06': 'Concept-label question.', 'judg07': 'Concept-label question.',
 'judg08': 'Concept-label question.', 'ai03': 'Superseded by the rollout case (same source, sharper design).',
 'ai05': 'Superseded by axb14 and rollout3 with measured outcomes.', 'ai06': 'Superseded by rollout3 with measured outcomes.',
 'ai08': 'Advice item without a measured outcome.', 'ai13': 'Duplicate of ai09.', 'ai14': 'Advice item without a measured outcome.',
 'ai15': 'Duplicate of rollout case.', 'ai16': 'Generic advice; replaced by axb05 and axb12 with measured outcomes.',
 'ai17': 'Advice item without a measured outcome.', 'social02': 'Superseded by dimant-polarizednorms-choice.',
 'social05': 'Advice item without a measured outcome.', 'social06': 'Concept-label question.', 'social09': 'Duplicate of social08.',
 'social11': 'Duplicate of social10.', 'social17': 'Superseded by dimant-hate-choice.', 'social18': 'Superseded by dimant-contagion-multi.',
 'social19': 'Superseded by dimant-contagion-multi.', 'social21': 'Concept-label question.',
}
retired = bank.get('retired', [])
for cid, why in RETIRE.items():
    if cid in C:
        c = C.pop(cid); retired.append({'id': cid, 'title': c['title'], 'sources': c['sources'], 'reason': why}); log.append(('retired', cid, why))
bank['retired'] = retired

def edit(cid, field, val, why):
    c = C[cid]; old = c.get(field); c[field] = val; log.append(('edit', cid, field, why))

# Stronger options for items kept
edit('ai12', 'options', ['It costs more than a doctor', 'It cannot account for my unique case', 'It takes longer than a doctor'], 'Replace a non-serious distractor.')
edit('biz08', 'options', ['They find subtractive changes more often', 'They find subtractive changes less often', 'No measurable difference'], 'Plain, parallel options.')
edit('biz11', 'options', ['The estimate moves toward the number', 'The estimate is unaffected', 'The estimate moves away from the number'], 'Parallel options.')
edit('social20', 'question', 'Two teams give the same average answer on what conduct is acceptable. How do you see whether their norms differ?', 'Concrete managerial framing.')
edit('social20', 'options', ['Keep the full distribution of each person’s view', 'Compare the two team averages', 'Ask each manager to describe the norm', 'Count past policy violations'], 'Serious distractors.')
edit('social20', 'answerTitle', 'Keep the whole distribution', 'Shorter.')
edit('ai10', 'options', ['They weighted human advice more', 'They weighted algorithmic advice more', 'They ignored both sources equally'], 'Parallel options.')
for cid in ('social13',):
    edit(cid, 'options', ['Women became more likely to advance and be hired', 'No difference in any estimate', 'Women became less likely to advance'], 'Parallel options.')

# Merge drafts
for name in ('clusterA', 'clusterB', 'clusterC', 'clusterD'):
    d = json.loads((D / f'{name}.json').read_text())
    for sid, s in d['sources'].items():
        if sid in bank['sources']:
            if sid == 'dell26' and s.get('verification', {}).get('status') == 'verified_full_text':
                bank['sources'][sid]['verification'].update({'status': 'verified_full_text', 'text_read': s['verification'].get('text_read', ''), 'text_url': s['verification'].get('text_url', '')}); log.append(('upgrade', sid, 'full text read in cluster A'))
            continue
        s = dict(s); s.setdefault('kind', 'peer-reviewed'); s.setdefault('url', 'https://doi.org/' + s['doi'])
        bank['sources'][sid] = s; log.append(('source', sid, name))
    for c in d['challenges']:
        c = dict(c); ev = c.pop('evidence', None)
        if ev: evidence[c['id']] = ev
        assert c['id'] not in C, c['id']
        C[c['id']] = c; log.append(('add', c['id'], name))

# Post-merge editorial fixes (gate hits and house style)
C['misperceived-norms-action']['implication'] = C['misperceived-norms-action']['implication'].replace('to unlock stalled behavior', 'to move stalled behavior')
# Wording consistency: forecasts ask the same plain question
for c in C.values():
    if c['format'] == 'forecast' and re.match(r'How likely is (this|it)', c['question']):
        c['question'] = 'Is this what the study found?'
# Costello et al. is under an Expression of Concern: not used.
bank['sources'].pop('costello24', None)

THEME_OF_SOURCE = {
 'ai-work': ['noy23', 'bry25', 'dell26', 'bastani25', 'vaccaro24', 'doshi24'],
 'ai-trust': ['diet15', 'dietvorst18', 'logg19', 'cast19', 'long19', 'yeomans19', 'grove00', 'bucinca21', 'kleinberg18', 'hoffman18'],
 'fairness': ['obermeyer19', 'lambrecht19', 'resume04', 'blind00', 'bohnet16', 'contact05'],
 'persuasion': ['salvi25', 'altay24', 'jakesch23', 'vosoughi18', 'pennycook21', 'beyond23', 'bail18', 'allcott20'],
 'choice': ['defaults01', 'johnson04', 'thaler04', 'benartzi01', 'hotel08', 'energy07', 'frame81', 'anchor74', 'subtract21', 'scheibehenne10', 'iyengar00', 'hallsworth17', 'loss79'],
 'incentives': ['gneezy00', 'card12', 'breza18', 'bloom15', 'bloom24', 'kahneman90', 'bertrand10'],
 'evidence': ['gordon19', 'lewis15', 'kristal20', 'shu12', 'masks22', 'requiem20'],
 'honesty': ['cohn19', 'abeler19', 'gachter16', 'fischbacher13', 'prox22', 'notalie23', 'deviant21', 'enforcers23', 'observ21', 'opioid26'],
 'norms': ['norms24', 'plural24', 'measure23', 'hate23', 'contagion19', 'plural93', 'bursztyn20', 'lees20', 'motivated24'],
 'forecasting': ['mellers14', 'moore08', 'buehler94', 'cent10', 'team10'],
}
src_theme = {s: t for t, ss in THEME_OF_SOURCE.items() for s in ss}
missing = set()
for c in C.values():
    t = None
    for s in c['sources']:
        if s in src_theme: t = src_theme[s]; break
    if t is None: missing.add((c['id'], tuple(c['sources'])))
    c['theme'] = t or 'choice'
bank['themes'] = [
 {'id': 'ai-work', 'title': 'AI at work', 'principle': 'Generative AI raises average output on tasks inside its frontier and lifts weaker performers most. Outside the frontier it makes confident people wrong, and unrestricted use can erode the skill it replaces.'},
 {'id': 'ai-trust', 'title': 'Trusting algorithms', 'principle': 'People punish an algorithm’s visible errors more than a human’s, yet often weight algorithmic advice heavily when they cannot see it fail. Control, task type and expertise move the balance.'},
 {'id': 'fairness', 'title': 'Fairness and bias', 'principle': 'Bias enters through the target a model predicts, the market that delivers it and the signals evaluators see. Measured outcomes, not intentions, show whether a process is fair.'},
 {'id': 'persuasion', 'title': 'Persuasion and misinformation', 'principle': 'Falsehood travels on human attention. AI can personalize arguments at scale, labels change trust in ways designers do not intend, and small prompts to think about accuracy help a little.'},
 {'id': 'choice', 'title': 'Choice architecture', 'principle': 'Defaults, menus, frames and anchors decide many choices before preferences do. The design of the decision is a management decision.'},
 {'id': 'incentives', 'title': 'Pay, incentives and work design', 'principle': 'Money changes the meaning of behavior as well as its price. Pay comparisons, fines and flexibility have effects that the incentive alone does not predict.'},
 {'id': 'evidence', 'title': 'Measuring what works', 'principle': 'Observational lift, expert forecasts and famous single studies often overstate effects. Randomized tests, replications and honest uncertainty protect budgets.'},
 {'id': 'honesty', 'title': 'Honesty and compliance', 'principle': 'Most people lie less than they could, many lie a little, and what they believe peers do shapes both. Enforcement works through norms as much as through penalties.'},
 {'id': 'norms', 'title': 'Norms and polarization', 'principle': 'The average opinion hides the distribution behind it. Misread norms, polarized expectations and visible bad examples drive behavior in teams and societies, and correcting beliefs can move it.'},
 {'id': 'forecasting', 'title': 'Forecasting and teams', 'principle': 'Forecasts improve with training, teaming and scoring, and fail through overconfidence and planning optimism. How a group talks and connects matters as much as who is in it.'},
]
bank['paths'] = [
 {'id': 'leading-ai', 'title': 'Leading with AI', 'case': True, 'blurb': 'Roll out an assistant, decide who gets it first, route tasks across the frontier, and protect the skills your people still need.', 'ids': ['rollout1', 'rollout2', 'rollout3', 'rollout4', 'axb14', 'axb01', 'ai07', 'axb13']},
 {'id': 'trust-algo', 'title': 'When to trust the algorithm', 'blurb': 'Formulas beat experts more often than experts expect. People still abandon models after one error. What changes their minds?', 'ids': ['axb04', 'ai09', 'axb02', 'axb03', 'axb06', 'ai10', 'axb11', 'axb10']},
 {'id': 'measure', 'title': 'Measure before you scale', 'blurb': 'Matched ad lift, famous nudges and expert forecasts. Find out which ones survived a randomized test.', 'ids': ['bz01', 'bz02', 'bz11', 'bz10', 'dimant-masks-forecast', 'dimant-requiem-forecast', 'civic-wallet-experts']},
 {'id': 'dimant-lab', 'title': 'Norms, honesty, polarization', 'blurb': 'Eugen Dimant’s research on how the shape of a norm, the visibility of peers and political identity change what people do.', 'ids': ['dimant-polarizednorms-choice', 'social01', 'dimant-hate-choice', 'dimant-contagion-multi', 'dimant-proximity-estimate', 'dimant-enforcers-rank', 'dimant-notalie-causal', 'dimant-masks-forecast']},
 {'id': 'design', 'title': 'Design the decision', 'blurb': 'Defaults, menus, frames and anchors. Small design choices that move retirement savings, consent and estimates.', 'ids': ['biz01', 'bz15', 'bz03', 'bz16', 'biz03', 'biz05', 'biz11', 'judg05']},
 {'id': 'people', 'title': 'Pay, flexibility and fairness', 'blurb': 'Remote work, pay transparency, fines and biased algorithms. What field experiments say about running people well.', 'ids': ['bz05', 'bz07', 'bz12', 'bz13', 'bz08', 'axb05', 'axb12', 'social12']},
 {'id': 'truth', 'title': 'Truth, persuasion and AI', 'blurb': 'AI debaters, AI labels, detection and the spread of falsehood. How beliefs move when machines join the conversation.', 'ids': ['axb08', 'axb07', 'axb09', 'false-news-spread', 'accuracy-prompt', 'opposing-views-bot', 'dimant-conspiracy-choice']},
]
bank['challenges'] = list(C.values())
ids = {c['id'] for c in bank['challenges']}
for p in bank['paths']: assert set(p['ids']) <= ids, (p['id'], set(p['ids']) - ids)
# Drop sources nothing uses any more, but record them.
used = {s for c in bank['challenges'] for s in c['sources']}
for sid in list(bank['sources']):
    if sid not in used:
        bank.setdefault('unused_sources', {})[sid] = bank['sources'].pop(sid); log.append(('unused-source', sid))
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'docs/audit/merge_log_2026-10-31.json').write_text(json.dumps(log, ensure_ascii=False, indent=1))
for name in ('clusterA', 'clusterB', 'clusterC', 'clusterD'): (ROOT / f'docs/audit/draft_{name}.json').write_text((D / f'{name}.json').read_text())
print(len(bank['challenges']), 'challenges;', len(bank['sources']), 'sources; missing theme:', missing)
