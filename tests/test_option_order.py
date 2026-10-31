"""Phones, projector console and the Streamlit pages must show options in the same order."""
import json, re, shutil, subprocess
import pytest
from conftest import ROOT
from thv_streamlit.common import option_order

@pytest.mark.skipif(not shutil.which('node'), reason='node not installed')
def test_python_order_matches_console_js():
    src = (ROOT / 'src/classroom.js').read_text()
    fns = '\n'.join(re.search(rf'^function {n}\(.*$', src, re.M).group(0) for n in ('hash', 'rng', 'shuffle'))
    cases = [(cid, n, code) for cid in ('ai09', 'bz15', 'axb11', 'dimant-contagion-multi') for n in (3, 4, 5) for code in ('K7QPM', 'ABCDE', 'ZZ9Q2')]
    js = fns + f"""
const S = {{}}; const out = [];
for (const [id, n, code] of {json.dumps(cases)}) {{ const c = {{ id, options: Array.from({{length: n}}, (_, i) => i) }};
  out.push(shuffle(c.options.map((t, i) => ({{ t, i }})), rng(hash(c.id + '-' + (hash(code) >>> 0)))).map(x => x.i)); }}
console.log(JSON.stringify(out));"""
    got = json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout)
    assert got == [option_order(cid, n, code) for cid, n, code in cases]
