"""Write the live content counts into README.md and docs/HANDOVER_FOR_CLAUDE.md, and check them in tests.

Counts live between markers such as <!--n:decisions-->112<!--/n-->. Run after any content change."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DOCS = [ROOT / 'README.md', ROOT / 'docs/HANDOVER_FOR_CLAUDE.md']

def counts():
    b = json.loads((ROOT / 'src/bank.json').read_text()); S = b['sources']
    live = [c for c in b['challenges'] if all(S[s]['verification']['status'] != 'quarantined' for s in c['sources'])]
    used = {s for c in live for s in c['sources']}
    dim = [c for c in live if any('Dimant' in S[s].get('authors', '') for s in c['sources'])]
    dim_src = {s for c in dim for s in c['sources'] if 'Dimant' in S[s].get('authors', '')}
    full = sum(1 for s in used if S[s]['verification']['status'] == 'verified_full_text')
    return {'decisions': len(live), 'sources': len(used), 'fulltext': full, 'dimant_decisions': len(dim), 'dimant_papers': len(dim_src),
            'paths': len(b.get('paths', [])), 'principles': len(b.get('themes', [])), 'retired': len(b.get('retired', []))}

PAT = re.compile(r'<!--n:(\w+)-->(.*?)<!--/n-->')
def apply(check=False):
    n = counts(); stale = []
    for p in DOCS:
        t = p.read_text(); new = PAT.sub(lambda m: f'<!--n:{m.group(1)}-->{n[m.group(1)]}<!--/n-->', t)
        if new != t:
            stale.append(p.name)
            if not check: p.write_text(new)
    return stale

if __name__ == '__main__':
    s = apply(check='--check' in sys.argv)
    if '--check' in sys.argv and s: sys.exit('STALE counts in: ' + ', '.join(s))
    print('counts', counts(), 'updated' if s else 'current')
