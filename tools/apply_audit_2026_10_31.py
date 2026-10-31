"""Apply the 2026-10-31 source audit to src/bank.json. Idempotent. Logs every change to docs/audit/corrections.json."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT/'src/bank.json').read_text())
A = Path(sys.argv[1])
res = {}
for k in range(1, 5):
    r = json.loads((A/f'result{k}.json').read_text())
    res.update(r['sources']); res.setdefault('_ch', {}).update(r['challenges'])
log = []
C = {c['id']: c for c in bank['challenges']}
def setf(cid, field, val, why):
    c = C[cid]
    if field.startswith('follow['):
        i = int(field[7]); old = c['follow'][i]['a']; c['follow'][i]['a'] = val
    elif field.startswith('options['):
        i = int(field[8]); old = c['options'][i]; c['options'][i] = val
    else:
        old = c.get(field); c[field] = val
    if old != val: log.append({'challenge': cid, 'field': field, 'old': old, 'new': val, 'reason': why})

ch = res.pop('_ch')
for cid, v in ch.items():
    for f, val in (v.get('corrections') or {}).items():
        if cid == 'judg02': continue  # handled by quarantine below
        if cid in ('biz05', 'biz06') and f == 'scene':
            continue  # rewritten below without design details that rest on a secondary source
        if cid == 'biz11' and f == 'follow[1].a': f = 'follow[1]'
        if f.endswith('.a'): f = f[:-2]
        setf(cid, f, val, '; '.join(v.get('issues', []))[:400])
# energy study: neutral wording that the abstract supports
setf('biz05', 'scene', 'A household already uses less electricity than its neighbors. It receives feedback showing the higher neighborhood average.', 'Delivery details (door hangers) rest on a secondary source; neutral wording keeps only what the abstract states.')
setf('biz06', 'scene', 'Researchers add an approval cue (a smiley face for households using less than average) to neighborhood comparison feedback.', 'Approval cue described as in the published abstract; not a utility bill.')
# biz11 follow answers referencing incentives
for i, f in enumerate(C['biz11']['follow']):
    if 'incentive' in f['a'] or 'expertise' in f['a']:
        setf('biz11', f'follow[{i}]', 'Anchor effects vary with context, and a relevant anchor can carry real information. In the original study, paying for accuracy did not remove the effect.', 'Tversky & Kahneman (1974): "Payoffs for accuracy did not reduce the anchoring effect."')
# Every field anywhere that repeats a corrected source summary
fix93 = "Students thought peers were more comfortable with campus drinking than they themselves were. Men's attitudes later shifted toward that mistaken norm, and feeling out of step was linked to alienation from campus."
for cid in ('social04', 'social05'):
    for i, f in enumerate(C[cid]['follow']):
        if 'individual behavior' in f['a'] or 'mistaken norm' in f['a']: setf(cid, f'follow[{i}]', fix93, 'Abstract reports attitude change and alienation, not drinking behavior.')
# Source metadata
S = bank['sources']
def sset(sid, k, v, why):
    if S[sid].get(k) != v: log.append({'source': sid, 'field': k, 'old': S[sid].get(k), 'new': v, 'reason': why}); S[sid][k] = v
sset('hate23', 'year', 2024, 'Version of record: Management Science 70(1), 1-31, January 2024 (online 2023).')
sset('norms24', 'year', 2025, 'Version of record: Management Science 71(3), 2245-2263, March 2025 (online 2024).')
sset('cast19', 'title', 'Task-Dependent Algorithm Aversion', 'Crossref title case.')
sset('blind00', 'title', 'Orchestrating Impartiality: The Impact of "Blind" Auditions on Female Musicians', 'Crossref title has quotation marks.')
sset('plural93', 'takeaway', fix93, 'Abstract reports attitudes and alienation, not behavior.')
VOL = {'noy23': ('381(6654)', '187-192'), 'bry25': ('140(2)', '889-942'), 'dell26': ('37(2)', '403-423'), 'doshi24': ('10(28)', 'eadn5290'),
 'diet15': ('144(1)', '114-126'), 'logg19': ('151', '90-103'), 'cast19': ('56(5)', '809-825'), 'long19': ('46(4)', '629-650'), 'frame81': ('211(4481)', '453-458'),
 'anchor74': ('185(4157)', '1124-1131'), 'defaults01': ('116(4)', '1149-1187'), 'hotel08': ('35(3)', '472-482'), 'energy07': ('18(5)', '429-434'), 'norms24': ('71(3)', '2245-2263'),
 'plural24': ('3(10)', 'pgae413'), 'resume04': ('94(4)', '991-1013'), 'blind00': ('90(4)', '715-741'), 'cent10': ('329(5996)', '1194-1197'), 'team10': ('330(6004)', '686-688'),
 'subtract21': ('592(7853)', '258-261'), 'plural93': ('64(2)', '243-256'), 'loss79': ('47(2)', '263-292'), 'loss15': ('144(1)', '7-11'), 'avoid03': ('129(1)', '139-167'),
 'contact05': ('88(1)', '91-107'), 'hate23': ('70(1)', '1-31'), 'contagion19': ('73', '66-88'), 'measure23': ('233', '111417')}
for sid, s in S.items():
    r = res[sid]; tr = r.get('text_read', '').lower()
    status = 'verified_full_text' if tr.startswith('full text') or 'verified full text' in tr else 'verified_abstract'
    s['volume'], s['pages'] = VOL[sid]
    s['verification'] = {'status': status, 'checked': '2026-10-31', 'metadata': 'matched Crossref record', 'text_read': r.get('text_read', ''), 'text_url': r.get('text_url', '')}
    for k in ('verified', 'verification_status', 'verification_note', 'doi_url'): s.pop(k, None)
# The loss-aversion reversal is contested (André & de Langhe 2021): withheld from scored play.
S['loss15']['verification'] = {'status': 'quarantined', 'checked': '2026-10-31', 'metadata': 'matched Crossref record',
  'note': 'Reversal finding contested by a reanalysis (Andre & de Langhe, 2021, JEP: General 150(12), 2659-2665). Withheld from scored play.', 'text_read': 'abstract only'}
log.append({'source': 'loss15', 'field': 'verification.status', 'old': None, 'new': 'quarantined', 'reason': 'Contested reversal; challenge judg02 removed from scored play.'})
(ROOT/'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
out = ROOT/'docs/audit'; out.mkdir(parents=True, exist_ok=True)
(out/'corrections_2026-10-31.json').write_text(json.dumps(log, ensure_ascii=False, indent=1))
for k in range(1, 5): (out/f'agent_result_batch{k}.json').write_text((A/f'result{k}.json').read_text())
print(len(log), 'changes')
