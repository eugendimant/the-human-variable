"""Content gates: schema per format, source integrity, verification status, writing rules."""
import json, re, subprocess, sys
import pytest
from conftest import BANK, ROOT

C = BANK['challenges']; S = BANK['sources']
LIVE = [c for c in C if all(S[s]['verification']['status'] != 'quarantined' for s in c['sources'])]
FORMATS = {'choice', 'causal', 'multi', 'estimate', 'forecast', 'rank', 'allocate', 'delegate'}
TRACKS = {'AI × Business', 'Business', 'Culture & Society', 'Judgment'}
# Phrases that read as generated filler. Extend when a new one is found (gate, not a style note).
BANNED = re.compile(r"\b(delve|crucial|landscape|game[- ]changer|in today's|it is important to note|it's important to note|unlock|leverage|harness|navigate the|tapestry|revolutioni[sz]e|seamless(ly)?|cutting[- ]edge|robust insights?)\b|—", re.I)

def test_counts_and_ids():
    assert len(LIVE) >= 60
    ids = [c['id'] for c in C]; assert len(ids) == len(set(ids))
    assert TRACKS <= {c['track'] for c in LIVE}

def test_every_format_present():
    assert FORMATS <= {c['format'] for c in LIVE}, FORMATS - {c['format'] for c in LIVE}

@pytest.mark.parametrize('c', C, ids=lambda c: c['id'])
def test_schema(c):
    for k in ('id', 'track', 'concept', 'title', 'scene', 'question', 'answerTitle', 'explain', 'implication', 'boundary', 'sources', 'follow', 'format'):
        assert c.get(k), f'missing {k}'
    assert c['track'] in TRACKS and c['format'] in FORMATS
    assert len(c['follow']) >= 3 and all(f['q'].strip() and f['a'].strip() for f in c['follow'])
    f = c['format']
    if f in ('choice', 'causal', 'multi', 'rank', 'allocate'): assert len(c['options']) >= 2
    if f in ('choice', 'causal'): assert isinstance(c['answer'], int) and 0 <= c['answer'] < len(c['options'])
    if f == 'causal' and 'dag' in c:
        ids = {n['id'] for n in c['dag']['nodes']}; assert all(a in ids and b in ids for a, b, *_ in c['dag']['edges'])
    if f == 'multi':
        a = c['multiAnswers']; assert len(set(a)) == len(a) == 2 and all(0 <= i < len(c['options']) for i in a)
    if f == 'estimate':
        e = c['estimate']; assert e['min'] <= e['target'] <= e['max'] and e['tolerance'] > 0 and e['label']
    if f == 'forecast': assert isinstance(c['forecast']['truth'], bool) and len(c['forecast']['claim']) > 10
    if f == 'rank': assert sorted(c['rankAnswer']) == list(range(len(c['options']))) and c['rankLabel']
    if f == 'allocate':
        a = c['allocate']; assert len(a['values']) == len(c['options']) and a['total'] % a.get('step', 10) == 0
    if f == 'delegate':
        d = c['delegate']; assert len(d['tasks']) >= 2 and all(0 <= t['answer'] < len(d['choices']) and t['why'] for t in d['tasks'])
    if 'chart' in c: assert len(c['chart']['labels']) == len(c['chart']['values']) and c['chart'].get('note')
    if 'case' in c: assert 1 <= c['case']['step'] <= c['case']['of']

def test_cases_complete():
    cases = {}
    for c in C:
        if 'case' in c: cases.setdefault(c['case']['id'], []).append(c['case'])
    for cid, steps in cases.items():
        assert sorted(s['step'] for s in steps) == list(range(1, steps[0]['of'] + 1)), cid

def test_sources_verified_and_referenced():
    used = {s for c in C for s in c['sources']}
    assert used <= set(S)
    for sid, s in S.items():
        assert s['kind'] in ('peer-reviewed', 'scholarly-book'), sid
        assert re.match(r'^10\.\d{4,9}/\S+$', s['doi']) or s['kind'] == 'scholarly-book', sid
        assert s['url'].startswith('https://'), sid
        v = s['verification']; assert v['status'] in ('verified_full_text', 'verified_abstract', 'quarantined') and v['checked'], sid
        assert s.get('year') and s.get('venue') and s.get('takeaway'), sid
    assert not (set(S) - used), f'unused sources: {set(S) - used}'

def test_no_generated_filler():
    hits = []
    for c in C:
        for k in ('title', 'scene', 'question', 'answerTitle', 'explain', 'implication', 'boundary'):
            if BANNED.search(c[k]): hits.append((c['id'], k, BANNED.search(c[k]).group(0)))
        for f in c['follow']:
            if BANNED.search(f['q'] + ' ' + f['a']): hits.append((c['id'], 'follow', BANNED.search(f['q'] + f['a']).group(0)))
    assert not hits, hits

def test_banned_gate_fires():
    assert BANNED.search('We delve into the landscape') and BANNED.search('a — b') and not BANNED.search('A plain sentence.')

def test_short_copy():
    long = [(c['id'], k, len(c[k].split())) for c in LIVE for k, n in (('question', 22), ('scene', 55), ('answerTitle', 12)) if len(c[k].split()) > n]
    assert not long, long

def test_no_script_markup():
    blob = json.dumps(BANK)
    assert not re.search(r'<script|javascript:|onerror=', blob, re.I)

def test_built_page_current():
    r = subprocess.run([sys.executable, str(ROOT / 'src' / 'build.py'), '--check'], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout

def test_followups_add_information():
    """A follow-up must not repeat text already on the reveal screen (implication, boundary, explain)."""
    dup = [(c['id'], f['q']) for c in LIVE for f in c['follow'] if f['a'].strip() in (c['implication'].strip(), c['boundary'].strip(), c['explain'].strip())]
    assert not dup, dup

def test_followup_questions_unique_per_item():
    for c in LIVE:
        qs = [f['q'].lower() for f in c['follow']]; assert len(set(qs)) == len(qs), c['id']
