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

def _correct(c):
    return set(c['multiAnswers']) if c['format'] == 'multi' else {c['answer']}

def test_correct_option_is_not_usually_the_longest():
    """Review 2, M9: the longest option should not be a reliable cue (chance is about 1 in 3)."""
    items = [c for c in LIVE if c['format'] == 'choice']
    hits = [c['id'] for c in items if max(range(len(c['options'])), key=lambda i: len(c['options'][i])) in _correct(c)]
    assert len(hits) <= 0.35 * len(items), hits
    multi = [c for c in LIVE if c['format'] == 'multi']
    top2 = [c['id'] for c in multi if set(sorted(range(len(c['options'])), key=lambda i: -len(c['options'][i]))[:2]) == _correct(c)]
    assert not top2, top2

ABSOLUTE = re.compile(r"\b(always|never|only|completely|entirely|nothing)\b", re.I)
def test_distractors_avoid_absolute_words():
    """Review 2, M9: absolute words mark a distractor as wrong without thought."""
    bad = [(c['id'], o) for c in LIVE if c['format'] in ('choice', 'multi', 'causal')
           for i, o in enumerate(c['options']) if i not in _correct(c) and ABSOLUTE.search(o)]
    assert not bad, bad

def test_gates_fire():
    assert ABSOLUTE.search('The algorithm only beat strangers')

def test_titles_do_not_state_the_finding():
    """Review 2, M8: titles show before play, so they must not contain the answer's key words."""
    bad = []
    for c in LIVE:
        t = set(re.findall(r"[a-z]{5,}", c['title'].lower()))
        a = set(re.findall(r"[a-z]{5,}", c['answerTitle'].lower()))
        if t & a & {'backfired', 'surprise', 'wasn', 'worth', 'spared', 'unequal', 'fails', 'failed', 'failure', 'beats', 'doubled', 'halved'}: bad.append(c['id'])
        if re.search(r"backfire|wasn.t there|not spared|beats|fails", c['title'], re.I): bad.append(c['id'])
    assert not bad, bad

def test_doc_counts_current():
    sys.path.insert(0, str(ROOT / 'tools')); import sync_doc_counts
    assert not sync_doc_counts.apply(check=True), 'run python tools/sync_doc_counts.py'

def _js_score(c, r):
    out = subprocess.run(['node', '-e', f"const S=require('./src/scoring.js');console.log(JSON.stringify(S.score({json.dumps(c)},{json.dumps(r)})))"], cwd=ROOT, capture_output=True, text=True)
    return json.loads(out.stdout)['score']

def test_midpoint_guess_scores_at_most_half():
    """Review 3, M5: the untouched middle of an estimate axis must not be a winning strategy."""
    from server import scoring
    bad = [(c['id'], round(scoring.score(c, (c['estimate']['min'] + c['estimate']['max']) / 2)['score'], 2)) for c in LIVE if c['format'] == 'estimate'
           if scoring.score(c, (c['estimate']['min'] + c['estimate']['max']) / 2)['score'] > 0.5]
    assert not bad, bad

def test_bank_order_does_not_carry_the_answer():
    """Review 3, M2: answer indices spread across positions; no rank item is stored in answer order."""
    from collections import Counter
    ch = [c['answer'] for c in LIVE if c['format'] in ('choice', 'causal')]
    top = Counter(ch).most_common(1)[0][1]; assert top <= 0.45 * len(ch), Counter(ch)
    assert not [c['id'] for c in LIVE if c['format'] == 'rank' and c['rankAnswer'] == list(range(len(c['options'])))]
    assert sum(1 for c in LIVE if c['format'] == 'multi' and c['multiAnswers'] == [0, 1]) <= 0.4 * sum(1 for c in LIVE if c['format'] == 'multi')

NEG_SCOPE = re.compile(r"\b(were|was) not (tested|studied)\b", re.I)
def test_boundaries_state_scope_positively():
    """Review 3, minor 4 and CONTENT_GUIDE: a boundary says what the study covers."""
    assert not [c['id'] for c in LIVE if NEG_SCOPE.search(c['boundary'])]
    assert NEG_SCOPE.search('long-run use was not studied')

def test_no_working_paper_material_in_decisions():
    """Review 4, M2: decisions draw on versions of record only."""
    bad = [c['id'] for c in LIVE if re.search(r'\b(working[- ]paper|preprint|SSRN|NBER)\b', json.dumps(c, ensure_ascii=False), re.I)]
    assert not bad, bad

def _nums(t):
    return set(re.findall(r'\d+(?:\.\d+)?%|\d+\.\d+|\d{2,}(?:,\d{3})*', t))

def test_paths_do_not_leak_later_answers():
    """Review 4, M1: an item's key numbers must not appear in the reveal of an earlier item on the same path."""
    by = {c['id']: c for c in LIVE}; bad = []
    for p in BANK['paths']:
        ids = [i for i in p['ids'] if i in by]
        for j, cj in enumerate(ids):
            c = by[cj]; key = _nums(c['answerTitle'])
            if c['format'] == 'estimate': key |= {f"{c['estimate']['target']:g}"}
            for ci in ids[:j]:
                e = by[ci]; text = ' '.join([e['explain'], e['implication']] + [f['a'] for f in e['follow']])
                hit = {k for k in key if re.search(r'(?<![\d.])' + re.escape(k) + r'(?![\d])', text)}
                if hit: bad.append((p['id'], ci, '->', cj, sorted(hit)))
    assert not bad, bad

def test_evidence_comes_from_versions_of_record():
    ev = json.loads((ROOT / 'src/evidence.json').read_text())
    bad = [(k, q['location'][:40]) for k, qs in ev.items() for q in qs if re.search(r'\b(NBER|working paper|SSRN|arXiv)\b', q.get('location', ''), re.I) and 'design details only' not in q.get('location', '')]
    assert not bad, bad[:5]
