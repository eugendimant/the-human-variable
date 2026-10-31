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
        r = {'choice': c.get('answer'), 'causal': c.get('answer'), 'multi': c.get('multiAnswers'), 'estimate': (lambda e: e and e['min'] + round((e['target'] - e['min']) / e.get('step', 1)) * e.get('step', 1))(c.get('estimate')),   # nearest slider position to the target
             'forecast': 100 if c.get('forecast', {}).get('truth') else 0, 'rank': c.get('rankAnswer')}.get(f)
        if f == 'allocate':
            v = c['allocate']['values']; best = c['allocate'].get('best') or [v.index(max(v))]; t = c['allocate']['total']
            if len(best) > 1 and t % len(best): continue
            r = [t // len(best) if i in best else 0 for i in range(len(v))]
            res = scoring.score(c, r); assert abs(res['score'] - 1) < 1e-9, c['id']; continue
        if f == 'delegate': r = [t['answer'] for t in c['delegate']['tasks']]
        res = scoring.score(c, r); assert res['score'] == 1 and res['correct'], c['id']
        assert scoring.valid(c, r), c['id']

def test_forecast_calibration_is_folded():
    """Review 8, M1: a confident correct 'no' is calibrated, not overconfident."""
    js = "const S=require('./src/scoring.js');const r=[{format:'forecast',response:10,outcome:0},{format:'forecast',response:90,outcome:1}].map(x=>S.toCalibrationRecord(null,x));console.log(JSON.stringify([r,S.calibration(r).overconfidence]))"
    out = json.loads(subprocess.run(['node', '-e', js], cwd=ROOT, capture_output=True, text=True, check=True).stdout)
    assert out[0] == [{'p': 90, 'outcome': 1}, {'p': 90, 'outcome': 1}] and out[1] <= 0

def test_no_information_strategies_have_no_skill():
    """Review 9, M2: hedging, random order and even splits earn zero skill in every format."""
    js = """const S=require('./src/scoring.js');const B=require('./src/bank.json');const out=[];
for(const c of B.challenges){let r=null;
 if(c.format==='forecast')r=50; else if(c.format==='allocate'){const n=c.options.length,t=c.allocate.total;r=Array.from({length:n},(_, i)=>i<n-1?Math.floor(t/n):t-Math.floor(t/n)*(n-1))}
 if(r!==null)out.push([c.id,S.skill(c,S.score(c,r).score)])}
console.log(JSON.stringify(out))"""
    out = json.loads(subprocess.run(['node', '-e', js], cwd=ROOT, capture_output=True, text=True, check=True).stdout)
    assert out and all(abs(v) < 0.05 for _, v in out), [x for x in out if abs(x[1]) >= 0.05]
