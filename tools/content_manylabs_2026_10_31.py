"""Review 23, minor 11: a contest item where the famous finding held up (Many Labs 1, anchoring). Idempotent.
Text read: the published article (Social Psychology 45(3):142-152, Hogrefe), institutional repository copy."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]
bp, ep = R / 'src/bank.json', R / 'src/evidence.json'
b = json.loads(bp.read_text()); ev = json.loads(ep.read_text())
URL = 'https://research.unipd.it/bitstream/11577/2688304/1/ManyLabs.2014.SP.fulltext.pdf'
b['sources']['manylabs14'] = {
    'id': 'manylabs14', 'authors': 'Klein et al.', 'year': 2014,
    'title': 'Investigating variation in replicability: A “Many Labs” replication project', 'venue': 'Social Psychology',
    'volume': '45(3)', 'pages': '142-152', 'doi': '10.1027/1864-9335/a000178', 'url': 'https://doi.org/10.1027/1864-9335/a000178', 'kind': 'peer-reviewed',
    'takeaway': 'Across 36 samples, 10 of 13 classic effects replicated consistently; anchoring came out larger than originally reported.',
    'verification': {'status': 'verified_full_text', 'checked': '2026-10-31', 'metadata': 'journal, volume and pages printed on the article',
                     'text_read': 'published article PDF (Hogrefe layout), University of Padova repository copy', 'text_url': URL}}
item = {
    'id': 'manylabs-anchoring', 'track': 'Business', 'format': 'forecast', 'concept': 'Replication check', 'title': 'A number shown first',
    'scene': 'A classic study found that a high or low number shown before a question, such as how many babies are born per day in the US or how tall Mount Everest is, pulled people’s estimates toward it. A large replication project reran it across many labs.',
    'question': 'How likely is it that the study found this?',
    'forecast': {'claim': 'Across the replication samples, the anchoring effect held up and came out at least as large as in the original study.', 'truth': True},
    'answerTitle': 'Anchoring replicated, and larger than first reported',
    'explain': 'Across 36 samples with 6,344 participants, Klein and colleagues found anchoring effects of d = 1.27 to 2.60 on four estimation questions, against an overall 0.93 in the original study. Ten effects in the project replicated consistently; two priming effects did not.',
    'implication': 'Treat anchors as reliable: decide which number a customer or negotiating partner sees first, and test the choice before you scale it.',
    'boundary': 'General-knowledge estimation questions answered by participants in 36 samples.',
    'sources': ['manylabs14'],
    'study': {'design': 'Multi-site replication', 'n': '36 samples, 6,344 participants'},
    'theme': 'evidence',
    'chart': {'labels': ['Original study, overall', 'Distance to New York', 'Population of Chicago', 'Height of Mount Everest', 'Babies born per day'],
              'values': [0.93, 1.27, 2.05, 2.45, 2.60], 'unit': '', 'highlight': 4, 'decimals': 2,
              'note': 'Anchoring effect size, Cohen’s d (unweighted replication estimate per question).'},
    'follow': [
        {'q': 'Which effects did not replicate?', 'a': 'Flag priming on conservatism and currency priming on system justification did not replicate; imagined contact reducing prejudice showed weak support.'},
        {'q': 'How large was each replication effect?', 'a': 'From d = 1.27 for distance to New York to d = 2.60 for babies born, against an overall 0.93 in the original study.'},
        {'q': 'How large was the project?', 'a': '36 independent samples totaling 6,344 participants.'}],
}
b['challenges'] = [c for c in b['challenges'] if c['id'] != item['id']] + [item]
P = {p['id']: p for p in b['paths']}
if item['id'] not in P['measure']['ids']: P['measure']['ids'].append(item['id'])
ev[item['id']] = [
    {'source': 'manylabs14', 'quote': 'In the aggregate, 10 effects replicated consistently.', 'location': 'Abstract, Social Psychology 45(3), p. 142'},
    {'source': 'manylabs14', 'quote': 'across 36 independent samples totaling 6,344 participants.', 'location': 'Abstract, p. 142'},
    {'source': 'manylabs14', 'quote': 'And two effects – flag priming influencing conservatism and currency priming influencing system justification – did not replicate.', 'location': 'Abstract, p. 142'},
    {'source': 'manylabs14', 'quote': 'One effect – imagined contact reducing prejudice – showed weak support for replicability.', 'location': 'Abstract, p. 142'},
    {'source': 'manylabs14', 'printed': 'Original study ES 0.93 for each anchoring item; replication ES (unweighted): babies born 2.60, Mt. Everest 2.45, Chicago 2.05, distance to NYC 1.27', 'location': 'Table 2, p. 147'},
]
bp.write_text(json.dumps(b, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
print('ok')
