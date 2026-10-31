"""Fixes from independent review 6 (2026-10-31): provenance made consistent, wrong Dimant number, leaky scenes. Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']
ev = json.loads((ROOT / 'src/evidence.json').read_text())

# --- M1: the 30% in the paper is misreporting above chance, not the winning-report rate
C['dimant-requiem-forecast']['explain'] = 'Among 1,200 MTurk participants, misreporting (winning reports above the 16.67% that honest reporting would produce) hovered around 30 percentage points under every message, with null effects and tight confidence intervals.'

# --- M2: verification records match what was read
PUBLISHED = {  # read in the published article (author-hosted journal PDF, open-access journal page, PMC or the journal PDF)
  'requiem20': 'JEBO article, published version (author-hosted PDF)', 'notalie23': 'GEB article, published version (author-hosted PDF)',
  'contagion19': 'Journal of Economic Psychology article, published version (author-hosted PDF); numbers identical to the accepted manuscript',
  'deviant21': 'JEBO article, published version (author-hosted PDF)', 'observ21': 'JEBO article, published version (author-hosted PDF)',
  'beyond23': 'JESP article, published version (author-hosted PDF)', 'opioid26': 'Health Economics article, open-access published PDF',
  'hate23': 'Management Science article (Articles in Advance), published version (author-hosted PDF)', 'card12': 'AER article, published version (author-hosted PDF)',
  'doshi24': 'Science Advances article, open access (PMC)', 'hotel08': 'Journal of Consumer Research article, published version (author-hosted PDF)',
  'bohner14': 'PLoS ONE article, open access', 'energy07': 'Psychological Science article, published version (author-hosted PDF)',
  'blind00': 'AER article, published version (journal PDF)', 'jabbour23': 'JAMA article, publisher full text (excerpts)'}
for sid, how in PUBLISHED.items():
    if sid in S:
        v = S[sid]['verification']; v['status'] = 'verified_full_text'; v['text_read'] = how
ACCEPTED = {'allcott20': "authors' final accepted manuscript of the AER article", 'gachter16': 'Europe PMC author manuscript of the Nature article',
            'lees20': 'Harvard DASH accepted manuscript of the Nature Human Behaviour article', 'dietvorst18': 'accepted manuscript of the Management Science article (UPenn deposit)'}
for sid, how in ACCEPTED.items():
    if sid in S: S[sid]['verification'].update({'status': 'verified_accepted_manuscript', 'text_read': how})
C['facebook-deactivation']['chart']['note'] = "Values reported in Allcott et al. (2020, AER), read in the authors' accepted manuscript; effects in standard deviations, treatment minus control."
DROP = re.compile(r'povertyactionlab|Working-paper version|fetch-tool paraphrase|press release|news release|news item|annotated copy|Pezzo & Beckstead', re.I)
for k in list(ev): ev[k] = [q for q in ev[k] if not DROP.search(q.get('location', ''))]
ev['ai01'] = [q for q in ev.get('ai01', []) if 'Science abstract' not in q.get('location', '')] + [
  {'source': 'noy23', 'quote': 'The average time taken decreased by 40% and output quality rose by 18%.', 'location': 'Science abstract (version of record)'}]
# text that rested on the dropped quotes
f = C['civic-wallet-rank']['follow']
for i, x in enumerate(f):
    if x['q'] == 'Did the key in the wallet matter?': f[i] = {'q': 'Did the key in the wallet matter?', 'a': 'Yes. Wallets with a key, useful only to the owner, were more likely to be reported, which the authors read as concern for the owner.'}
m = C['misperceived-norms-support']
m['explain'] = '87% of participants agreed that women should be able to work outside the home, yet on average they guessed that only 63% of the other men in their session agreed.'
m['follow'] = [x for x in m['follow'] if not x['q'].startswith('Were men just telling') and x['q'] != 'What does this mean for a manager?'] + [{'q': 'What does this mean for a manager?', 'a': 'Private support can be far higher than people assume; sharing the measured share can free people to make choices they thought their peers opposed.'}]
a = C['misperceived-norms-action']
a['study']['n'] = 'Married Saudi men from the original sessions'
for i, x in enumerate(a['follow']):
    if x['q'] == 'How wrong were the original beliefs?': a['follow'][i] = {'q': 'How wrong were the original beliefs?', 'a': 'On average men guessed that 63% of their peers supported women working outside the home, when 87% did.'}
for i, x in enumerate(C['biz07']['follow']):
    if x['q'] == 'How many people took part?': C['biz07']['follow'][i] = {'q': 'How many people took part?', 'a': 'Hundreds of participants across eight experiments, each solving a different improvement problem.'}
for i, x in enumerate(C['biz08']['follow']):
    if x['q'] == 'Was this a single study?': C['biz08']['follow'][i] = {'q': 'Was this a single study?', 'a': 'No. It was one of eight experiments that all pointed to a default toward adding.'}
C['biz07']['study']['n'] = 'Eight experiments'
s10 = C['social10']
s10['explain'] = 'In the independent replication, members’ individual IQ largely accounted for differences in group performance, and the turn-taking and share-of-women effects were not supported.'
for i, x in enumerate(s10['follow']):
    if x['q'] == 'Is the whole idea dead?': s10['follow'][i] = {'q': 'Is the whole idea dead?', 'a': 'No. The original team’s 2021 meta-analysis supports the factor and points to social perceptiveness, while independent analyses find it weaker or explained by members’ IQ.'}

# --- M4: scenes and options that give the answer away
C['dimant-conspiracy-choice']['scene'] = re.sub(r'\s*they knew were false', '', C['dimant-conspiracy-choice']['scene'])
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
def swap(cid, old, new):
    C[cid]['options'] = [new if o == old else o for o in C[cid]['options']]
C['social04']['scene'] = 'Students rated their own comfort with campus drinking and the comfort of the average student at their university.'
C['dimant-conspiracy-choice']['scene'] = 'In a multi-round sharing task, participants chose whether to share factual news or conspiracy theories, including ones they did not believe. The social feedback each kind of post earned varied.'
swap('dimant-conspiracy-choice', 'Inattention: they missed that the content was false', 'Habit: they shared whatever appeared first')
swap('dimant-conspiracy-choice', 'Belief: people shared what they thought was true', 'Novelty: conspiracy posts felt more original')
swap('dimant-notalie-causal', 'Honest employees hold this belief most strongly', 'Seeing others lie taught both the belief and the habit')
swap('dimant-notalie-causal', 'The belief and lying are unrelated', 'The belief reflects general cynicism, not the task')
C['ai12']['options'] = ['It costs more than a human doctor', 'Its handling of health data feels unsafe', 'It cannot account for each patient’s uniqueness']
C['axb10']['scene'] = 'People make decisions with help from an AI that is usually right but sometimes wrong. Designers test different ways of presenting its advice.'
C['axb10']['options'] = ['No design changed agreement with wrong advice', 'Plain explanations with each suggestion', 'Making users answer before seeing the AI']
C['social07']['scene'] = 'Members of a political party agree on its headline position. Researchers asked members to draw how views are spread within their party.'
swap('biz02', 'They had each worked out that it was the best plan', 'The employer match required the default rate')
swap('ai07', 'The AI-assisted set was more varied overall', 'AI help made stories less enjoyable to read')
swap('dimant-contagion-multi', 'Pro-social behavior was the more contagious', 'Distant peers’ bad behavior spread most')
C['dimant-contagion-multi']['options'] = [o for o in C['dimant-contagion-multi']['options'] if o != 'Closeness spread good behavior more than bad']
C['dimant-contagion-multi']['multiAnswers'] = sorted(C['dimant-contagion-multi']['options'].index(o) for o in ['Anti-social behavior was more contagious than pro-social', "Closeness amplified bad behavior's spread more than good"])
# M5: an untested gap is a tie
a4 = C['axe04']['allocate']; o = C['axe04']['options']
a4['best'] = [o.index('Original propaganda article'), o.index('GPT-3 article, no human editing')]
a4['valueName'] = "share agreeing with the claim; the paper reports no test of the 3.9-point gap between the original and GPT-3, so both count as best"
# minors
C['ai04']['explain'] = 'Across 5,172 customer-support agents, access to a generative AI assistant raised issues resolved per hour by 15% on average.'
C['bz10']['scene'] = C['bz10']['scene'].replace('about 30% of shoppers bought jam', 'about 30% of shoppers who stopped at the display bought jam')
C['dimant-masks-forecast']['forecast']['claim'] = 'At least one of the seven messages increased mask-wearing among Democrats or Republicans.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('scenes ok')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
C['axe11'].pop('rankTies', None)
C['axe11']['answerTitle'] = 'GPT-3 helped true claims and slightly shielded false ones'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('axe11')
