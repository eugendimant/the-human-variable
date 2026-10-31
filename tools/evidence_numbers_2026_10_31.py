"""Review 9, M1: every number in an explanation or answer title appears in a quote for that decision.
Numbers that were recorded in location notes (read from tables or figure labels) become their own entries,
marked as values as printed. Two decisions get their missing quotes. Retired ids leave the file. Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); ev = json.loads((ROOT / 'src/evidence.json').read_text())
C = {c['id']: c for c in bank['challenges']}
for k in list(ev):
    if k not in C: del ev[k]
for k, qs in ev.items():
    seen = set(); out = []
    for q in qs:
        if (q['quote'], q.get('location')) in seen: continue
        seen.add((q['quote'], q.get('location'))); out.append(q)
        m = re.search(r'\(([^()]*\d[^()]*)\)\s*$', q.get('location', ''))
        if m and not re.search(r'p\.\s*\d|pp\.|Section|Table \d+$|Fig\. \d+$|^\d{4}$', m.group(1)):
            vq = {'source': q.get('source'), 'quote': m.group(1), 'location': q['location'][:m.start()].strip() + ' (values as printed)'}
            if (vq['quote'], vq['location']) not in seen: seen.add((vq['quote'], vq['location'])); out.append(vq)
    ev[k] = out
ADD = {
 'judg09': [{'source': 'loss79', 'quote': 'PROBLEM 3: Choose between A: (4,000, .80), or B: (3,000). N = 95 [20] [80]*', 'location': 'Econometrica 47(2), p. 266, Table I (values as printed)'},
            {'source': 'loss79', 'quote': "PROBLEM 3': Choose between A: (-4,000, .80), or B: (-3,000). N = 95 [92]* [8]", 'location': 'Econometrica 47(2), p. 268, Table I (values as printed)'}],
 'axb15': [{'source': 'costello24', 'quote': 'engaged 2044 conspiracy believers in personalized evidence-based dialogues with GPT-4 Turbo', 'location': 'Abstract (Crossref record of the Science article)'},
           {'source': 'costello24', 'quote': 'The intervention reduced conspiracy belief by ~20%.', 'location': 'Abstract (Crossref record of the Science article)'},
           {'source': 'costello24', 'quote': 'The effect remained 2 months later', 'location': 'Abstract (Crossref record of the Science article)'}],
 'ai01': [{'source': 'noy23', 'quote': 'we assigned occupation-specific, incentivized writing tasks to 453 college-educated professionals', 'location': 'Science abstract (version of record)'}],
 'dimant-enforcers-rank': [{'source': C['dimant-enforcers-rank']['sources'][0], 'quote': '77.8% vs 62.3%, P < 0.001', 'location': 'PNAS Nexus, Results, inequity-creating vs equity-restoring bribes (Europe PMC full text; values as printed)'}],
 'dimant-polarizednorms-choice': [{'source': 'norms24', 'quote': '1,203 participants', 'location': 'Management Science 71(3), Section 4 (published version; values as printed)'}],
}
for k, qs in ADD.items():
    have = {q['quote'] for q in ev.get(k, [])}
    ev.setdefault(k, []).extend(q for q in qs if q['quote'] not in have)
ev['axb15'] = [q for q in ev['axb15'] if '2190 Americans' not in q['quote'] and 'durably reduced participants' not in q['quote'] and 'undiminished' not in q['quote']]
a = C['axb15']   # the abstract of the version of record reports 2,044 believers in the dialogues
a['scene'] = a['scene'].replace('2,190 people', '2,044 people'); a['boundary'] = a['boundary'].replace('2,190 US adults who endorsed at least one conspiracy theory', '2,044 conspiracy believers'); a['study']['n'] = '2,044 conspiracy believers'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n'); print('ok')
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
C['social15']['explain'] = 'In Dimant’s experiments, Trump supporters and opponents felt far closer to their own side (78.1%) than to a group-mate who shared only a painting preference (about 39%), yet gave allies no more money (14.97% versus 13.54%). From opponents, they took 22.9%.'
C['axb14']['explain'] = 'Consultants with GPT-4 completed 12.2% more tasks and worked 25.1% faster, and graded quality rose 33.9% with GPT-4 alone.'
C['bz04']['explain'] = 'Only 29.7% finished by their best-guess date, against an average prediction of 33.9 days, and fewer than half (48.7%) finished by their worst-case date.'
C['dimant-motivated-estimate']['explain'] = 'Without identity cues, people chose lenient (above-median) peers’ information 54.61% of the time, a self-serving tilt in which sources they consulted.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('explains')
# ai10's source was read in the published PDF (evidence: p. 93)
bank = json.loads((ROOT / 'src/bank.json').read_text())
sid = next(c for c in bank['challenges'] if c['id'] == 'ai10')['sources'][0]
bank['sources'][sid]['verification'].update({'status': 'verified_full_text', 'text_read': 'OBHDP article, published version (PDF), Experiment 1A results p. 93'})
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
