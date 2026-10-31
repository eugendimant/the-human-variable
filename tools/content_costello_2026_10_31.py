"""Add Costello, Pennycook & Rand (2024) at Eugen Dimant's instruction."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text())
bank['sources']['costello24'] = {
 'id': 'costello24', 'authors': 'Costello, Pennycook & Rand', 'authors_full': 'Thomas H. Costello, Gordon Pennycook, David G. Rand',
 'year': 2024, 'title': 'Durably reducing conspiracy beliefs through dialogues with AI', 'venue': 'Science', 'volume': '385(6714)', 'pages': 'eadq1814',
 'doi': '10.1126/science.adq1814', 'url': 'https://doi.org/10.1126/science.adq1814', 'kind': 'peer-reviewed',
 'takeaway': 'Personalized, evidence-based dialogues with GPT-4 Turbo reduced conspiracy belief by about 20%, and the effect lasted two months.',
 'verification': {'status': 'verified_abstract', 'checked': '2026-10-31', 'metadata': 'matched Crossref record', 'text_read': 'abstract (Crossref)'},
}
item = {'id': 'axb15', 'track': 'AI × Business', 'concept': 'AI and belief change', 'theme': 'persuasion', 'format': 'estimate',
 'title': 'Can a chatbot talk people out of it?',
 'scene': '2,044 people who believed a conspiracy theory described it in their own words. GPT-4 Turbo then answered their specific claims with evidence over three rounds of conversation.',
 'question': 'By how much did belief in their own conspiracy theory fall?',
 'answerTitle': 'About 20%, and it held for two months',
 'explain': 'Belief in the chosen conspiracy fell by about 20% after three rounds of tailored, evidence-based dialogue, and the drop persisted two months later.',
 'implication': 'To correct persistent false beliefs among customers or staff, answer each person’s specific claim with evidence. A tailored AI dialogue can do this at scale.',
 'boundary': 'Online experiments with 2,044 conspiracy believers in three-round conversations with GPT-4 Turbo.',
 'sources': ['costello24'],
 'estimate': {'target': 20, 'min': 0, 'max': 60, 'tolerance': 6, 'label': 'Drop in belief in their own conspiracy theory', 'unit': '%'},
 'study': {'design': 'Online experiments', 'n': '2,044 conspiracy believers'},
 'follow': [{'q': 'Did the effect fade?', 'a': 'No. The reduction in belief persisted at the two-month follow-up.'},
            {'q': 'Did it change other beliefs too?', 'a': 'Yes. The dialogues also reduced belief in conspiracy theories the participants had not discussed with the AI.'},
            {'q': 'Why tailor the conversation?', 'a': 'Each participant described their own theory and evidence, and the model responded to those specific claims rather than giving a generic debunking.'}]}
ids = {c['id'] for c in bank['challenges']}
if 'axb15' not in ids: bank['challenges'].append(item)
for p in bank['paths']:
    if p['id'] == 'truth' and 'axb15' not in p['ids']: p['ids'].insert(1, 'axb15')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('added')
