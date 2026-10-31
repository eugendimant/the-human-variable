"""Generate docs/SCIENTIFIC_AUDIT.md and docs/SOURCE_INDEX.md from src/bank.json and the audit logs. Run after any content change."""
import json
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
B = json.loads((ROOT / 'src/bank.json').read_text())
S, C = B['sources'], B['challenges']
live = lambda c: all(S[s]['verification']['status'] != 'quarantined' for s in c['sources'])
corr = json.loads((ROOT / 'docs/audit/corrections_2026-10-31.json').read_text())
st = Counter(s['verification']['status'] for s in S.values())
L = ['# Scientific audit', '', f"Generated from `src/bank.json` by `tools/make_audit_doc.py`. Audit date: 2026-10-31.", '',
     '## Standard', '',
     '- Scored answers rest only on peer-reviewed journal articles (no working papers or preprints).',
     '- Every source: metadata matched against its Crossref record (authors, year of the version of record, title, journal, volume, pages).',
     '- Every number used in a decision appears in text the auditor read. The record states what was read: the full text or the published abstract. Where a number came from an earlier version of the same paper, that is stated.',
     '- Contested findings appear only as items about the contest (for example, choice overload and the sign-first replication). A source whose central claim is disputed and has no such item is quarantined from scored play.',
     '- Scenes are teaching adaptations; they describe the real design (population, task, setting).', '',
     '## Summary', '',
     f"- Decisions in scored play: {sum(map(live, C))} (formats: {', '.join(f'{k} {v}' for k, v in Counter(c['format'] for c in C if live(c)).most_common())}).",
     f"- Sources: {len(S)} ({st.get('verified_full_text', 0)} checked against full text, {st.get('verified_abstract', 0)} against the published abstract, {st.get('quarantined', 0)} quarantined).",
     f"- Corrections applied to the 28 carried-forward sources and their 60 decisions: {len(corr)} logged changes (`docs/audit/corrections_2026-10-31.json`).",
     f"- Decisions retired with reasons: {len(B.get('retired', []))} (listed below).",
     f"- Track balance: {', '.join(f'{k} {v}' for k, v in Counter(c['track'] for c in C if live(c)).most_common())}.", '',
     '## Sources', '', '| Source | Venue | Check | Decisions | Note |', '|---|---|---|---|---|']
for sid, s in sorted(S.items(), key=lambda kv: (kv[1]['authors'], kv[1]['year'])):
    used = [c['id'] for c in C if sid in c['sources']]
    v = s['verification']; check = {'verified_full_text': 'Full text', 'verified_abstract': 'Abstract', 'quarantined': 'Quarantined'}[v['status']]
    note = (v.get('note') or s.get('flags') or '')
    if isinstance(note, (list, dict)): note = json.dumps(note, ensure_ascii=False)
    L.append(f"| {s['authors']} ({s['year']}). *{s['title']}*. [doi:{s['doi']}]({s['url']}) | {s['venue']} {s.get('volume', '')} {s.get('pages', '')} | {check} | {', '.join(used)} | {str(note).replace('|', '/')[:300]} |")
L += ['', '## Corrections to carried-forward content', '']
for x in corr:
    who = x.get('challenge') or x.get('source'); L.append(f"- **{who}**, {x['field']}: {str(x['reason'])[:240]}")
L += ['', '## Retired decisions', '']
for r in B.get('retired', []): L.append(f"- {r['id']} ({r['title']}): {r['reason']}")
L += ['', '## Not verified', '', '- No independent human expert has reviewed this audit. Checks were run by AI agents that read the published texts listed above; each quote and location is stored in `src/evidence.json` and `docs/audit/`.',
      '- Abstract-level checks confirm the numbers and directions that appear in abstracts; design details beyond the abstract were taken only from full texts where marked.']
(ROOT / 'docs/SCIENTIFIC_AUDIT.md').write_text('\n'.join(L) + '\n')
idx = ['# Source index', ''] + [f"- {s['authors']} ({s['year']}). {s['title']}. *{s['venue']}* {s.get('volume', '')}, {s.get('pages', '')}. {s['url']}" for s in sorted(S.values(), key=lambda s: (s['authors'], s['year']))]
(ROOT / 'docs/SOURCE_INDEX.md').write_text('\n'.join(idx) + '\n')
print('wrote audit for', len(S), 'sources')
