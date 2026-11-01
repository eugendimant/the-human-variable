"""Review 25 content fixes. Idempotent; edits by text (I11); every new sentence checked against the item's evidence (I15)."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
bp, ep = R / 'src/bank.json', R / 'src/evidence.json'
b = json.loads(bp.read_text()); ev = json.loads(ep.read_text()); C = {c['id']: c for c in b['challenges']}
def fa(cid, q, new):
    for f in C[cid]['follow']:
        if f['q'] == q: f['a'] = new
# minor 1: a follow-up never states another live item's answer, or names that item's authors
fa('ai09', 'Why do other studies find people prefer algorithms?', 'Designs differ. Here people watched the model make errors before choosing. Studies in which advice is only labeled as coming from an algorithm, and never seen to fail, test a different situation; one of them is a decision of its own in the lab.')
fa('dimant-contagion-multi', 'Does the 2022 proximity study say the same?', 'Both studies give closeness a central role. Here closeness meant answering personal questions more like the observed peer, and close peers’ bad choices spread most. The 2022 study varied a minimal shared-identity cue; its result is a decision of its own in the lab.')
fa('genai3', 'What about colleagues who use AI?', 'How colleagues judge people who use AI is a separate decision in the lab.')
# minor 2: the axb01 task-type entry was a paraphrase stored as a quote; the published sentence replaces it
ev['axb01'] = [e for e in ev['axb01'] if not e.get('quote', '').startswith('Decision tasks: significantly negative')]
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
print('ok')
ev = json.loads(ep.read_text())
Q = [('Among decision tasks—those in which participants decided between a finite set of options—the pooled effect size for human–AI synergy was significantly negative (g = −0.27; t104 = −3.20; two-tailed P = 0.002; 95% CI, −0.44 to −0.10), which indicates performance losses from combining humans and AI.', 'Results, task type'),
     ('In contrast, among creation tasks—those in which participants created some sort of open-response content—the pooled effect size for human–AI synergy was positive (g = 0.19; t104 = 1.35; two-tailed P = 0.180; 95% CI, −0.09 to 0.48), pointing to synergy between humans and AI.', 'Results, task type')]
for q, loc in Q:
    if not any(e.get('quote') == q for e in ev['axb01']):
        ev['axb01'].append({'source': 'vaccaro24', 'quote': q, 'location': loc + '; Nature Human Behaviour, published article (Europe PMC full text, PMC11659167)'})
ep.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
# minor 3: the "hate in behavior" comparator. The published-version quote stops at the in-group figure; the full sentence, with the
# painting out-group (11.99%, net giving), is read in the author's public working-paper version (owner's rule: preprints may verify
# numbers behind a paywall, labelled as such).
b = json.loads(bp.read_text()); ev = json.loads(ep.read_text()); C = {c['id']: c for c in b['challenges']}
s = C['social15']
s['explain'] = ('In Dimant’s experiments, Trump supporters and opponents felt far closer to their own side (78.1%) than to a group-mate who shared only a painting preference (about 39%), '
                'yet gave allies no more money (14.97% versus 13.54%). A painting out-group still received 11.99%; from political opponents, people took 22.9%.')
s['chart'] = {'labels': ['Gave to allies', 'Gave to a painting group-mate', 'Gave to a painting out-group', 'Took from political opponents'], 'values': [14.97, 13.54, 11.99, 22.9], 'unit': '%', 'highlight': 3,
              'note': 'Share of the endowment given or taken.'}
q = {'source': 'hate23', 'quote': 'regardless of whether their partners held the same (13.54%, green bar bottom-right panel, p=0.78) or different (11.99%, red bar bottom-right panel, p=0.56) painting preferences.',
     'location': 'Section on prosocial and antisocial behavior; author’s public working-paper version (Jan 2021, CESS Nuffield), used to complete the sentence that the published-version quote truncates'}
if not any(e.get('quote') == q['quote'] for e in ev['social15']): ev['social15'].append(q)
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
# lint R27 (new): a chart's title states its measure; the citation lives in the source line under the figure
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
NOTES = {'ai10': 'Weight on the advice, by its label (Experiment 1A).',
         'biz01': 'Share enrolled in the savings plan at 3 to 15 months of tenure.',
         'biz11': 'Median estimate of the share of African countries in the UN, by the number the wheel showed.',
         'judg05': 'Share choosing the sure option, by frame.',
         'bz07': 'Fall in quit rates under hybrid work, by group.',
         'facebook-deactivation': 'Effect of deactivating Facebook, in standard deviations (treatment minus control).',
         'misperceived-norms-action': 'Share of wives who applied for and interviewed for jobs outside the home, follow-up survey.',
         'judg09': 'Share choosing the gamble, gains against losses.'}
for k, v in NOTES.items(): C[k]['chart']['note'] = v
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
# audit 30, minor 5: the chart says where its third value was read
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
C['social15']['chart']['note'] = 'Share of the endowment given or taken; the painting out-group value is read in the author\u2019s public working-paper version.'
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
b = json.loads(bp.read_text()); C = {c['id']: c for c in b['challenges']}
C['social15']['chart']['note'] = 'Share of the endowment given or taken.'   # provenance of the 11.99% stays in the evidence record (owner rule: preprints verify, players see the version of record)
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n')
