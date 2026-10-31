"""Fixes from independent review 2 and the blind fact-check of 32 items (2026-10-31)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}; S = bank['sources']
# --- fact-check fixes
C['rollout1']['follow'][2] = {'q': 'Which problems gained most?', 'a': 'Gains were largest for moderately rare problems, where agents had less experience but the system still had enough training data.'}
C['rollout1']['explain'] = 'In a staggered rollout to customer-support agents, issues resolved per hour rose 15% on average, and less experienced and lower-skilled agents improved both speed and quality.'
C['genai1']['follow'][0]['a'] = 'Peak content novelty rose slightly (marginally significant), and AI-assisted artists who explored more novel ideas earned better peer evaluations, regardless of prior originality.'
C['genai1']['follow'][2]['a'] = 'Output rose substantially after adoption. The paper’s own figures differ (25% in the abstract, 50% at adoption in the results), so treat the size as uncertain.'
C['axe05']['follow'][1]['a'] = 'Yes. Physician answers averaged 52 words and chatbot answers 211, and the authors note length may have inflated empathy ratings.'
S['ayers23']['pages'] = '589-596'
S['dell26']['authors_full'] = "Fabrizio Dell'Acqua, Edward McFowland III, Ethan Mollick, Hila Lifshitz, Katherine C. Kellogg, Saran Rajendran, Lisa Krayer, François Candelon, Karim R. Lakhani"
S['bry25']['authors_full'] = 'Erik Brynjolfsson, Danielle Li, Lindsey Raymond'
S['norms24']['authors_full'] = 'Eugen Dimant, Michele Gelfand, Anna Hochleitner, Silvia Sonderegger'
S['plott05']['authors_full'] = 'Charles R. Plott, Kathryn Zeiler'
S['contagion19']['authors_full'] = 'Eugen Dimant'
C['dimant-enforcers-rank']['explain'] = 'Norm information raised reporting from 73.3% to 82.8% when the bribe created inequity (P < 0.005), and from 57.9% to 67.2% when it restored equity (marginal, P = 0.074). Inequity-creating bribes drew more reporting overall (77.8% vs 62.3%, P < 0.001).'
C['dimant-enforcers-rank']['boundary'] = 'Bribery vignette with 225 US adults, alongside a main behavioral study with 1,240 punishers from a representative US sample.'
C['bz06']['follow'][2]['a'] = 'Debated. Plott and Zeiler (2005) made the mug gap disappear with procedures that remove misunderstandings; Isoni, Loomes and Sugden (2011) confirmed that for mugs but found a persistent gap for lotteries under the same procedures.'
C['bz06']['rankTies'] = [[0, 2]]
# --- M10: one consistent description of Dimant et al. (2025)
d24 = {'design': 'Online experiment, two-player contribution game (6 treatments)', 'n': '1,203 US adults (representative sample)'}
for cid in ('social01', 'social03', 'dimant-polarizednorms-choice'): C[cid]['study'] = dict(d24)
C['dimant-polarizednorms-choice']['scene'] = 'A representative US sample played a two-player contribution game after seeing how others behaved: tightly clustered, widely spread, or split into two extreme camps.'
C['dimant-polarizednorms-choice']['boundary'] = 'Two-player contribution game with 1,203 US adults, with the distribution of others’ behavior set by design.'
C['social01']['boundary'] = 'Two-player contribution game with 1,203 US adults, varying the shape of the norm while holding its average fixed.'
C['social03']['boundary'] = 'Two-player contribution game in which the spread of the norm was set by design; whether variety helps depends on the task.'
C['dimant-motivated-estimate']['boundary'] = 'US participants choosing information sources before an undetectable lying game, with and without partisan identity cues.'
# --- M4: no scoring of differences the study did not separate
b7 = C['bz07']
for k in ('options', 'rankAnswer', 'rankValues', 'rankLabel', 'rankTies'): b7.pop(k, None)
b7.update({'format': 'estimate', 'question': 'By how much did hybrid work cut the quit rate overall?',
  'estimate': {'target': 33, 'min': 0, 'max': 100, 'tolerance': 7, 'label': 'Reduction in quit rate with two home days a week', 'unit': '%'},
  'answerTitle': 'Quits fell by a third, with no loss in performance',
  'explain': 'Hybrid work cut quit rates by one-third (7.20% to 4.80%), with larger drops for women and non-managers. Performance reviews showed no difference over two years.',
  'chart': {'labels': ['All employees', 'Women', 'Non-managers'], 'values': [33, 54, 40], 'unit': '%', 'highlight': 0, 'note': 'Bloom, Han & Liang (2024), Nature: reductions in quit rates overall 7.20% to 4.80% (P = 0.043); women 9.2% to 4.2%; non-managers 8.59% to 5.33%.'}})
# --- M5: only routes the study compared; no hints in task text
r3 = C['rollout3']['delegate']; r3['choices'] = ['Use GPT-4', 'Work without AI']
for t in r3['tasks']: t['answer'] = 0 if t['answer'] == 0 else 1
r3['tasks'][2]['why'] = 'On this outside-frontier task, correctness fell from 84.5% without AI to 70.6% with GPT-4 and 60.0% with GPT-4 plus a prompt overview.'
C['rollout3']['explain'] = 'Inside the frontier, consultants with GPT-4 completed 12.2% more tasks and worked 25.1% faster. On the outside-frontier case, correctness fell from 84.5% without AI to 70.6% with GPT-4 and 60.0% with GPT-4 plus a prompt overview.'
C['axb01']['delegate']['choices'][0] = 'Human and AI together'
C['axe01']['delegate']['tasks'][2]['text'] = 'Pick a vacation spot chosen for sensory pleasure'
# --- M6: the record on Costello et al. is visible to players
C['axb15']['boundary'] = 'Online experiments with 2,190 conspiracy believers. Science issued an expression of concern in June 2026; the authors’ corrected reanalysis reports the same result.'
# --- M8: neutral titles (titles show before play in the Library and on the projector)
T = {'ai01': 'Writing with ChatGPT', 'ai07': 'Stories written with AI', 'ai09': 'The model that erred', 'ai12': 'Medical advice from AI', 'biz05': 'Feedback for thrifty homes',
     'biz07': 'Fixing a slow process', 'social03': 'When peers vary', 'social04': 'Comfort with campus drinking', 'social07': 'Drawing a party’s norm', 'social13': 'Screens at auditions',
     'social16': 'Nudges across the divide', 'social20': 'Same average, two teams', 'axb05': 'Who gets extra care?', 'axb10': 'Designing AI advice', 'axb12': 'Who saw the STEM ad?',
     'bz01': 'Measuring ad lift', 'bz06': 'The mug market', 'bz08': 'Fines for late pickup', 'bz09': 'Photo or price?', 'bz13': 'Pay by rank', 'bz14': 'Two ways to compare candidates',
     'bz15': 'Organ donor forms', 'bz16': 'Two fund menus', 'misperceived-norms-support': 'Private views in Riyadh', 'dimant-observability-choice': 'Giving while watched',
     'genai1': 'Artists adopt AI images', 'axe14': 'The sales bot', 'axb11': 'Jokes, friends and algorithms', 'axb02': 'Control over the model'}
for k, v in T.items(): C[k]['title'] = v
C['axb05']['study'] = {'design': 'Audit of a widely used health-care risk algorithm', 'n': 'Patients at one large academic hospital'}
# --- M9: competitive options instead of absolute-word strawmen
C['social01']['options'][2] = 'The average alone predicted choices well'
C['social16']['options'][2] = 'The nudges closed the partisan gap'
C['axb05']['options'][2] = 'The model used zip code as a proxy for race'
C['biz05']['options'][2] = 'Below-average households cut use further'
# --- Forecast balance: state four claims in their true form
def flip(cid, claim):
    C[cid]['forecast'] = {'claim': claim, 'truth': True}
flip('axb07', 'People could not tell AI-written from human-written self-descriptions better than chance.')
flip('bz11', 'A preregistered direct replication with 1,235 people found no effect of signing first.')
flip('axe08', 'Freelancers with strong past performance also lost jobs and earnings after ChatGPT arrived.')
flip('dimant-requiem-forecast', 'None of the four honesty messages reduced cheating compared with no message.')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
