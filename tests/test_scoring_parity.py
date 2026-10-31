"""JS scorer (shipped to browsers) and Python scorer (server aggregates) must agree on every case."""
import json, random, shutil, subprocess
import pytest
from conftest import BANK, ROOT
from server import scoring

def cases():
    rnd = random.Random(7); out = []
    for c in BANK['challenges']:
        f = c['format']
        for _ in range(6):
            if f in ('choice', 'causal'): r = rnd.randrange(len(c['options']))
            elif f == 'multi': r = rnd.sample(range(len(c['options'])), 2)
            elif f == 'estimate': r = rnd.randint(c['estimate']['min'], c['estimate']['max'])
            elif f == 'forecast': r = rnd.randrange(0, 101, 5)
            elif f == 'rank': r = rnd.sample(range(len(c['options'])), len(c['options']))
            elif f == 'allocate':
                k = len(c['options']); t = c['allocate']['total']; st = c['allocate'].get('step', 10)
                cuts = sorted(rnd.randrange(0, t // st + 1) for _ in range(k - 1)); parts = [b - a for a, b in zip([0] + cuts, cuts + [t // st])]; r = [p * st for p in parts]
            elif f == 'delegate': r = [rnd.randrange(len(c['delegate']['choices'])) for _ in c['delegate']['tasks']]
            out.append((c, r))
    return out

@pytest.mark.skipif(not shutil.which('node'), reason='node not installed')
def test_parity():
    cs = cases()
    js = "const S=require(process.argv[1]);const d=JSON.parse(require('fs').readFileSync(0,'utf8'));console.log(JSON.stringify(d.map(([c,r])=>{const x=S.score(c,r);return [Math.round(x.score*1e6)/1e6,x.correct]})))"
    out = subprocess.run(['node', '-e', js, str(ROOT / 'src' / 'scoring.js')], input=json.dumps(cs), capture_output=True, text=True, check=True).stdout
    got = json.loads(out)
    for (c, r), (s, ok) in zip(cs, got):
        p = scoring.score(c, r)
        assert abs(p['score'] - s) < 1e-6 and p['correct'] == ok, (c['id'], r, p, s, ok)
    assert len(got) == len(cs) > 300

def test_answers_score_full():
    for c in BANK['challenges']:
        f = c['format']
        r = {'choice': c.get('answer'), 'causal': c.get('answer'), 'multi': c.get('multiAnswers'), 'estimate': c.get('estimate', {}).get('target'),
             'forecast': 100 if c.get('forecast', {}).get('truth') else 0, 'rank': c.get('rankAnswer')}.get(f)
        if f == 'allocate': v = c['allocate']['values']; r = [c['allocate']['total'] if i == v.index(max(v)) else 0 for i in range(len(v))]
        if f == 'delegate': r = [t['answer'] for t in c['delegate']['tasks']]
        res = scoring.score(c, r); assert res['score'] == 1 and res['correct'], c['id']
        assert scoring.valid(c, r), c['id']
