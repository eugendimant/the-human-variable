"""Apply the replication check (docs/audit/replications_2026-10-31.json): contested classics become items about the evidence record."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']
def src(sid, authors, year, title, venue, vol, pages, doi, takeaway, text='abstract (Crossref or publisher)'):
    S.setdefault(sid, {'id': sid, 'authors': authors, 'year': year, 'title': title, 'venue': venue, 'volume': vol, 'pages': pages, 'doi': doi,
        'url': 'https://doi.org/' + doi, 'kind': 'peer-reviewed', 'takeaway': takeaway,
        'verification': {'status': 'verified_abstract', 'checked': '2026-10-31', 'metadata': 'matched Crossref record', 'text_read': text}})
src('bohner14', 'Bohner & Schlüter', 2014, 'A room with a viewpoint revisited: Descriptive norms and hotel guests’ towel reuse behavior', 'PLoS ONE', '9(8)', 'e104086', '10.1371/journal.pone.0104086',
    'In two German hotels, both a descriptive-norm sign and a standard environmental sign raised towel reuse compared with no sign, and the norm sign did no better than the standard one.')
src('bates17', 'Bates & Gupta', 2017, 'Smart groups of smart people: Evidence for IQ as the origin of collective intelligence in the performance of human groups', 'Intelligence', '60', '46-56', '10.1016/j.intell.2016.11.004',
    'In independent replications, members’ individual IQ accounted for about 80% of differences in group IQ; effects of turn-taking and the share of women were not supported.')
src('plott05', 'Plott & Zeiler', 2005, 'The willingness to pay-willingness to accept gap, the "endowment effect," subject misconceptions, and experimental procedures for eliciting valuations', 'American Economic Review', '95(3)', '530-545', '10.1257/0002828054201387',
    'With procedures designed to remove misconceptions, the gap between willingness to accept and willingness to pay for mugs disappeared; later studies found it returns under other procedures.')
# Hotel towels: the original finding stays, with its replication record visible; the same-room claim becomes an item about the replication.
C['biz03']['boundary'] = 'Field studies in one US hotel. Later replications found modest effects, and some found the norm sign no better than a plain environmental sign.'
b4 = C['biz04']
for k in ('options', 'answer'): b4.pop(k, None)
b4.update({'format': 'forecast', 'title': 'Does the towel sign travel?', 'concept': 'Replication',
  'scene': 'A famous US study found hotel guests reused more towels when a sign said most guests do, especially guests of the same room. Researchers repeated the test in two German hotels.',
  'question': 'Is this what the replication found?',
  'forecast': {'claim': 'In the German hotels, the “most guests reuse” sign raised reuse more than a standard environmental sign.', 'truth': False},
  'answerTitle': 'Both signs helped; the norm sign did no better',
  'explain': 'Both message types raised towel reuse compared with no message, but the descriptive-norm message was not more effective than the standard environmental message, and same-room effects were inconsistent.',
  'implication': 'Before rolling out a famous nudge, test it against the plain message you would otherwise use, not just against doing nothing.',
  'boundary': 'Two hotels in Germany; later meta-analyses report modest, consistent effects of norm messages across studies.',
  'sources': ['bohner14', 'hotel08'], 'theme': 'evidence', 'study': {'design': 'Field replication', 'n': 'Guests of two German hotels'},
  'follow': [{'q': 'What did the original study find?', 'a': 'Goldstein, Cialdini and Griskevicius (2008) found that a sign saying most guests reuse towels beat a standard environmental appeal, and that a same-room norm worked best.'},
             {'q': 'So do norm messages work at all?', 'a': 'Modestly. A 2017 meta-analysis of hotel studies described the social-norms effect as weaker than earlier estimates but consistent.'},
             {'q': 'What should a manager compare against?', 'a': 'The message you would send anyway. Here, any sign beat no sign, which a test against silence would have mistaken for a norm effect.'}]})
# Collective intelligence: an item about the contest.
s10 = C['social10']
for k in ('options', 'answer'): s10.pop(k, None)
s10.update({'format': 'forecast', 'title': 'Does turn-taking make groups smart?', 'concept': 'Replication', 'theme': 'evidence',
  'scene': 'A 2010 Science paper reported a general “collective intelligence” factor in groups, linked to members’ social sensitivity and to equal turn-taking in conversation. Independent researchers ran their own groups.',
  'question': 'Is this what the independent replication found?',
  'forecast': {'claim': 'Groups with more equal conversational turn-taking scored higher on collective intelligence.', 'truth': False},
  'answerTitle': 'Turn-taking did not predict it; members’ IQ did',
  'explain': 'In the replication, members’ individual IQ accounted for about 80% of differences in group performance, and the turn-taking and share-of-women effects were not supported.',
  'implication': 'Treat team-composition recipes from single studies as hypotheses. Track your own teams’ results before redesigning how meetings run.',
  'boundary': 'Lab groups on standardized tasks. The original team’s later meta-analysis of 22 studies supports a collective intelligence factor, so the debate continues.',
  'sources': ['bates17', 'team10'], 'study': {'design': 'Independent lab replications', 'n': 'Groups of students'},
  'follow': [{'q': 'What did the original paper claim?', 'a': 'Woolley et al. (2010) reported a general factor across group tasks, correlated with average social sensitivity, equal turn-taking and the share of women.'},
             {'q': 'Is the whole idea dead?', 'a': 'No. The original team’s 2021 meta-analysis of 22 studies supports the factor and points to social perceptiveness, while independent analyses find it weaker or explained by members’ IQ.'},
             {'q': 'Why does replication matter here?', 'a': 'Team-design advice spread widely from the original paper. When an independent test fails on the key predictors, the advice should wait for more evidence.'}]})
# Blind auditions: keep the item, state the precision plainly.
C['social13']['boundary'] = 'Orchestra audition records; the authors report large standard errors for several estimates, and one effect ran in the opposite direction.'
C['social13']['follow'][0] = {'q': 'How precise were the estimates?', 'a': 'Not very. The authors note large standard errors for several estimates, so the direction favors women while many individual effects fall short of statistical significance.'}
# Endowment effect: the gap is robust, its cause is debated.
C['bz06']['sources'] = ['kahneman90', 'plott05'] if 'kahneman90' in S else C['bz06']['sources'] + ['plott05']
C['bz06']['follow'][2] = {'q': 'Is the gap just a quirk of the procedure?', 'a': 'Debated. Plott and Zeiler (2005) removed it with extra training on the procedure; a later replication found it returned under their own method. The gap itself shows up widely.'}
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok', C['bz06']['sources'])
# Second pass: cite the meta-analyses the item text refers to.
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']
src('nisa17', 'Nisa, Varum & Botelho', 2017, 'Promoting sustainable hotel guest behavior: A systematic review and meta-analysis', 'Cornell Hospitality Quarterly', '58(4)', '354-363', '10.1177/1938965517704371',
    'Across hotel studies, the social-norms effect on towel reuse was weaker than earlier estimates but consistent, producing modest increases in reuse.')
src('riedl21', 'Riedl et al.', 2021, 'Quantifying collective intelligence in human groups', 'Proceedings of the National Academy of Sciences', '118(21)', 'e2005737118', '10.1073/pnas.2005737118',
    'A meta-analysis of 22 studies found strong support for a general collective intelligence factor, with the share of women predicting performance through social perceptiveness.')
for cid, extra in (('biz04', 'nisa17'), ('social10', 'riedl21')):
    if extra not in C[cid]['sources']: C[cid]['sources'].append(extra)
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('meta-analyses cited')
