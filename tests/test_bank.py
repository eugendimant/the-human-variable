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
        v = s['verification']; assert v['status'] in ('verified_full_text', 'verified_accepted_manuscript', 'verified_published_excerpts', 'verified_abstract', 'quarantined') and v['checked'], sid
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
    items = [c for c in LIVE if c['format'] in ('choice', 'causal')]
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

NEG_SCOPE = re.compile(r"\b(were|was) not (tested|studied)\b|\bdoes not\b|\bdo not\b|, not\b|\bnot (a|an|the|every|whether|modern|random)\b|\btests no\b", re.I)
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
                e = by[ci]; text = ' '.join([e['explain'], e['implication'], e['answerTitle'], (e.get('chart') or {}).get('note', '')] + [f['a'] for f in e['follow']] + [t.get('why', '') for t in (e.get('delegate') or {}).get('tasks', [])])
                hit = {k for k in key if re.search(r'(?<![\d.])' + re.escape(k) + r'(?![\d])', text)}
                if hit: bad.append((p['id'], ci, '->', cj, sorted(hit)))
    assert not bad, bad

def test_evidence_comes_from_versions_of_record():
    ev = json.loads((ROOT / 'src/evidence.json').read_text())
    bad = [(k, q['location'][:40]) for k, qs in ev.items() for q in qs if re.search(r'\b(NBER|working paper|SSRN|arXiv)\b', q.get('location', ''), re.I) and 'design details only' not in q.get('location', '')]
    assert not bad, bad[:5]

# Explanations without a number: full text not readable, so the abstract-level statement stands (docs/audit/explain_rewrites_2026_10_31.json).
NO_NUMBER = {'social10', 'ai12', 'biz02', 'biz08', 'social04', 'social14', 'social20', 'axb11', 'axb12', 'bz14', 'bz16', 'axe08', 'axe09', 'axf04'}
GENERIC = re.compile(r"\b(research (highlights|documents|shows)|experiments link|the study found|studies show)\b", re.I)
def test_explanations_carry_the_key_number():
    """Review 4, M7: the main teaching sentence states the result with its number, in plain words."""
    assert not [c['id'] for c in LIVE if not re.search(r'\d', c['explain']) and c['id'] not in NO_NUMBER]
    assert not [c['id'] for c in LIVE if GENERIC.search(c['explain'])]
    assert GENERIC.search('Medical-AI resistance research highlights concerns')

QUALIFIERS = re.compile(r"\b(simply|clearly|closely|reliably|substantially|dramatically|strongly|vastly|about equally)\b", re.I)
def test_forecast_claims_are_neutral():
    """Review 5, M6: strong qualifiers must not mark false claims."""
    assert not [c['id'] for c in LIVE if c['format'] == 'forecast' and QUALIFIERS.search(c['forecast']['claim'])]

def test_pick_two_has_four_options():
    """Review 5, minor 1: with three options one correct pick forces the other."""
    assert not [c['id'] for c in LIVE if c['format'] == 'multi' and len(c['options']) < 4]

def test_no_constant_guess_pays_across_estimates():
    """Review 6, M3: one 'typical effect' guess on every estimate must not earn a good average."""
    from server import scoring
    E = [c for c in LIVE if c['format'] == 'estimate']
    best = max(sum(scoring.score(c, min(max(x, c['estimate']['min']), c['estimate']['max']))['score'] for c in E) / len(E) for x in range(-50, 501))
    assert best <= 0.35, best

def _reveal_text(e):
    return ' '.join([e['explain'], e['implication'], e['answerTitle'], (e.get('chart') or {}).get('note', '')] + [f['a'] for f in e['follow']] + [t.get('why', '') for t in (e.get('delegate') or {}).get('tasks', [])])

def test_siblings_do_not_leak_each_other():
    """Review 7, minor 3: decisions built on the same paper can meet in any round, so neither reveal may carry the other's key number."""
    bad = []
    for c in LIVE:
        key = _nums(c['answerTitle']) | ({f"{c['estimate']['target']:g}"} if c['format'] == 'estimate' else set())
        for e in LIVE:
            if e['id'] == c['id'] or not set(e['sources']) & set(c['sources']) or (c.get('case') and e.get('case')): continue
            hit = {k for k in key if re.search(r'(?<![\d.])' + re.escape(k) + r'(?![\d])', _reveal_text(e))}
            if hit: bad.append((e['id'], '->', c['id'], sorted(hit)))
    assert not bad, bad

def test_allocate_even_split_is_not_a_hit():
    """Review 7, M2: an allocation item must reward a prediction, not a hedge."""
    from server import scoring
    for c in LIVE:
        if c['format'] != 'allocate': continue
        n = len(c['options']); t = c['allocate']['total']
        assert scoring.score(c, [t // n] * (n - 1) + [t - t // n * (n - 1)])['score'] <= 0.6, c['id']

def test_evidence_entries_are_verbatim():
    """Review 7, M3: evidence entries are quotes from published texts, not paraphrases or summaries."""
    ev = json.loads((ROOT / 'src/evidence.json').read_text())
    weak = re.compile(r'paraphrase|as recorded|audit summary|fetch[- ]tool|as extracted|rendering|condensed|summari[sz]ed|transcribed|new_sources', re.I)
    live = {c['id'] for c in LIVE}
    bad = [k for k, qs in ev.items() if k in live for q in qs if weak.search(q.get('location', '') + ' ' + q.get('quote', q.get('printed', '')))]
    assert not bad, sorted(set(bad))

def test_no_fixed_slider_position_pays():
    """Review 8, M2: one position along the axis (say a quarter of the way) must not pay across estimates."""
    from server import scoring
    E = [c for c in LIVE if c['format'] == 'estimate']
    best = max(sum(scoring.score(c, c['estimate']['min'] + f / 100 * (c['estimate']['max'] - c['estimate']['min']))['score'] for c in E) / len(E) for f in range(101))
    assert best <= 0.35, best

def test_causal_labels_do_not_name_the_answer():
    """Review 8, M4: a node label visible before the reveal must not repeat the correct option's key words."""
    stop = {'which', 'their', 'there', 'other', 'about', 'people', 'model', 'beliefs', 'belief'}
    bad = []
    for c in LIVE:
        if c['format'] != 'causal' or 'dag' not in c: continue
        ans = {w for w in re.findall(r'[a-z]{5,}', c['options'][c['answer']].lower())} - stop
        vis = {w for n in c['dag']['nodes'] if not n.get('mask') for w in re.findall(r'[a-z]{5,}', n['label'].lower())}
        if ans & vis: bad.append((c['id'], sorted(ans & vis)))
    assert not bad, bad

WORDS = {'four hundred fifty-seven': 457, 'eighty-five': 85, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'half': 50, 'third': 33}
def _quote_has(n, qnums, qtext):
    v = float(n); d = len(n.split('.')[1]) if '.' in n else 0
    for q in qnums:
        q = abs(q)
        if round(q, d) == v or round(q * 100, d) == v or round(q / 100, d) == v or round(q, 0) == v: return True
    return any(w in qtext and WORDS[w] == v for w in WORDS)

def test_every_explained_number_is_quoted():
    """Review 9, M1: numbers in explanations and answer titles appear in that decision's evidence quotes
    (allowing rounding, percent versus share, and number words)."""
    ev = json.loads((ROOT / 'src/evidence.json').read_text()); bad = []
    for c in LIVE:
        qtext = ' '.join(q.get('quote', q.get('printed', '')) for q in ev.get(c['id'], [])).lower().replace(',', '')   # prose quotes and values as printed
        qnums = [float(x) for x in re.findall(r'(?<![\w.])-?\.?\d+(?:\.\d+)?', qtext) if x not in ('-', '.')]
        txt = ' '.join([c['explain'], c['answerTitle'], c.get('scene', ''), c['boundary']] + [f['a'] for f in c.get('follow', [])] + [str(v) for v in c.get('chart', {}).get('values', [])]).replace(',', '')   # follow-ups (review 11), charts, scenes and scope lines (review 17)
        txt = re.sub(r'401\(k\)|\bweeks? \d+', ' ', txt)
        txt = re.sub(r'\b(Stud(y|ies)|Experiments?|GPT|DALL-E|Midjourney v|Fortune|Firefly|Imagen)[- ]?\d+[a-z]?(\s*(to|and|-)\s*\d+[a-z]?)?', ' ', txt)  # names, not results
        for n in re.findall(r'(?<![\w.-])\d+(?:\.\d+)?', txt):
            if re.fullmatch(r'(19|20)\d\d', n): continue
            if not _quote_has(n, qnums, qtext): bad.append((c['id'], n))
    assert not [c['id'] for c in LIVE if not ev.get(c['id'])]
    assert not bad, bad


def test_no_rehosted_or_working_paper_links_in_provenance():
    """Provenance links point to publishers, authors, institutions or indexes, never to third-party re-hosts or working papers."""
    import re
    bad = [k for k, s in BANK['sources'].items() if re.search(r'gwern\.net|rivista\.ai|scispace\.com|hods\.org|mattalldian\.com|econreadinggroup|cesifo1_wp|/wp\d|workingpaper', s.get('verification', {}).get('text_url', ''), re.I)]
    assert not bad, bad


def test_quotes_do_not_stop_mid_sentence():
    """Review 11, M2: a quote cut off before the number it should support (", with GPT only producing") passes a number gate but misleads."""
    ev = json.loads((ROOT / 'src/evidence.json').read_text())
    bad = [(k, q['quote'][-40:]) for k, qs in ev.items() if isinstance(qs, list) for q in qs if 'quote' in q
           and re.search(r'\b(with|the|a|an|of|and|by|for|producing|than|was|were)$', q['quote'].strip().rstrip(',;:').lower())]
    assert not bad, bad


def test_page_code_states_no_finding():
    """Review 11, M3: page code must not hard-code a decision's result (the home card once said 'graders rated the work 18% better')."""
    js = (ROOT / 'src/app.js').read_text() + (ROOT / 'src/classroom.js').read_text(); bad = []
    for c in LIVE:
        for n in re.findall(r'(\d+(?:\.\d+)?)%', c['explain'] + ' ' + c['answerTitle']):
            if n not in ('0', '50', '100') and re.search(r'(?<![\d.])' + re.escape(n) + r'%', js): bad.append((c['id'], n))
        bad += [(c['id'], c['answerTitle']) for _ in [0] if c['answerTitle'] in js]
    assert not bad, bad


def test_absolute_words_are_not_a_free_tell():
    """Review 12: keyed options rarely use absolute or null wording, so such distractors stay few."""
    R = re.compile(r'\b(all|always|never|every|none|equally|neither|no)\b', re.I)
    bad = [(c['id'], o) for c in LIVE if c['format'] in ('choice', 'causal') for i, o in enumerate(c['options']) if i != c['answer'] and R.search(o)]
    assert len(bad) <= 3, bad

def test_evidence_entries_are_clean():
    """Review 12: every quote names one of its decision's sources, and no processing note poses as a quote."""
    ev = json.loads((ROOT / 'src/evidence.json').read_text()); C = {c['id']: c for c in LIVE}; bad = []
    for k, qs in ev.items():
        if not isinstance(qs, list) or k not in C: continue
        bad += [(k, q.get('quote', q.get('printed', ''))[:40]) for q in qs if q.get('source') not in C[k]['sources'] or ('quote' in q) == ('printed' in q)
                or ('printed' in q and not re.search(r'Table|Fig', q.get('location', '') + q['printed']))   # review 15: printed values name their table or figure
                or re.search(r'extracted text|rendered as|values below|^PMC\d+|^PubMed \d+|^DOI:|^OCR |^Studies? \d\w*$|^Experiment \d\w*$', q.get('quote', q.get('printed', '')), re.I)]   # review 14: annotations are not evidence
    assert not bad, bad


def test_random_slider_guess_earns_little():
    """Review 15, m3: an axis whose top sits just above the answer lets a random guess score well."""
    from server import scoring
    bad = []
    for c in LIVE:
        if c['format'] != 'estimate': continue
        e = c['estimate']; xs = [e['min'] + (e['max'] - e['min']) * k / 200 for k in range(201)]
        m = sum(scoring.score(c, x)['score'] for x in xs) / len(xs)
        if m > 0.3: bad.append((c['id'], round(m, 2)))
    assert not bad, bad


def test_forecast_wording_does_not_predict_truth():
    """Review 16, minor 1: a rule like 'negative wording means true' must not beat guessing."""
    N = re.compile(r'\b(no|not|none|fewer|less|lower|missed|cut|reduced|failed|without|never)\b', re.I)
    P = re.compile(r'\b(raised|raise|more|increased|improved|beat|higher|further|rose|stronger|strong)\b', re.I)   # review 18: positive verbs too
    F = [c for c in LIVE if c['format'] == 'forecast']
    cls = lambda c: 'n' if N.search(c['forecast']['claim']) else 'p' if P.search(c['forecast']['claim']) else 'o'
    best = 0
    for pn in range(0, 101, 5):
        for pp in range(0, 101, 5):
            for po in range(0, 101, 5):
                pm = {'n': pn, 'p': pp, 'o': po}
                s = sum(1 - 2 * (pm[cls(c)] / 100 - (1 if c['forecast']['truth'] else 0)) ** 2 for c in F) / len(F)
                best = max(best, s)
    assert best <= 0.55, round(best, 3)   # 0.5 is guessing


def test_paths_mix_true_and_false_forecasts():
    """Review 17, minor 5: inside a path with two or more forecasts, 'always true' must not be a strategy."""
    C = {c['id']: c for c in LIVE}; bad = []
    for p in BANK['paths']:
        t = [C[i]['forecast']['truth'] for i in p['ids'] if i in C and C[i]['format'] == 'forecast']
        if len(t) >= 2 and len(set(t)) < 2: bad.append((p['id'], t))
    assert not bad, bad


def test_estimate_guess_fraction_is_current():
    """Review 20, minor 1: the skill headline's estimate baseline is the best fixed slider position, so a no-information player shows no skill."""
    from server import scoring
    E = [c for c in LIVE if c['format'] == 'estimate']
    best = max(range(101), key=lambda f: sum(scoring.score(c, c['estimate']['min'] + f / 100 * (c['estimate']['max'] - c['estimate']['min']))['score'] for c in E))
    js = (ROOT / 'src/scoring.js').read_text(); frac = float(re.search(r'GUESS_FRAC = ([\d.]+)', js).group(1))
    at = lambda f: sum(scoring.score(c, c['estimate']['min'] + f * (c['estimate']['max'] - c['estimate']['min']))['score'] for c in E) / len(E)
    assert at(best / 100) - at(frac) <= 0.02, (best, frac)


def test_streamlit_tutor_holds_siblings():
    """Review 20, minor 6: the Streamlit tutor holds same-paper siblings of an open decision, as the server does."""
    t = (ROOT / 'thv_streamlit/tutor_page.py').read_text()
    assert re.search(r"any\(srcs\(i\) & srcs\(h\) for h in held\)", t)


def test_estimate_scene_numbers_sit_outside_the_band():
    """Review 20, minor 2 (class): no number printed in the scene, question or label lands inside the target band."""
    bad = []
    for c in LIVE:
        if c['format'] != 'estimate': continue
        e = c['estimate']; txt = ' '.join([c.get('scene', ''), c['question'], e.get('label', '')]).replace(',', '')
        bad += [(c['id'], m) for m in re.findall(r'-?\d+(?:\.\d+)?', txt) if abs(float(m) - e['target']) <= e['tolerance']]
    assert not bad, bad


def test_review21_baselines_and_calibration_events():
    """Review 21, minors 6 and 7: delegate baseline is the best constant routing; allocate calibration scores the event it states."""
    import subprocess, json as _j
    js = r"""const S=require('./src/scoring.js'); const B=require('./src/bank.json'); const out={};
      for (const c of B.challenges) if (c.format==='delegate' && !c.retired) { const T=c.delegate.tasks; let best=0; c.delegate.choices.forEach((_,j)=>{ best=Math.max(best, S.score(c, T.map(()=>j)).score) }); out[c.id]=[S.baseline(c), best] }
      const a=B.challenges.find(c=>c.format==='allocate'&&!c.retired), bi=(a.allocate.best||[a.allocate.values.indexOf(Math.max(...a.allocate.values))])[0], n=a.options.length;
      const r=a.options.map((_,i)=> i===bi ? 40 : 0); const rest=60/(n-1); a.options.forEach((_,i)=>{ if(i!==bi) r[i]=Math.floor(rest) }); r[bi]+=100-r.reduce((x,y)=>x+y,0);
      const sc=S.score(a,r); out.alloc=[S.toCalibrationRecord(a,{format:'allocate',response:r,correct:sc.correct}).outcome, sc.correct]; console.log(JSON.stringify(out))"""
    out = _j.loads(subprocess.run(['node', '-e', js], cwd=ROOT, capture_output=True, text=True, check=True).stdout)
    alloc = out.pop('alloc')
    for cid, (base, best) in out.items(): assert abs(base - best) < 1e-9, (cid, base, best)
    assert alloc[0] == 1, alloc   # top weight on the best option counts as a hit for calibration even when the verdict wants half the points


def test_estimates_never_score_a_null_contrast():
    """Review 22, M2: an estimate whose finding is a non-significant difference teaches false precision; such items are forecasts."""
    bad = [c['id'] for c in LIVE if c['format'] == 'estimate' and re.search(r'not (statistically )?significant|no (clear|significant) (gain|difference|effect)|P = \.[1-9]', c['explain'] + ' ' + c['answerTitle'])]
    assert not bad, bad


def test_claim_length_does_not_predict_truth():
    """Review 22, minor 11: claims above and below the median length are true at similar rates."""
    import statistics
    F = [c for c in LIVE if c['format'] == 'forecast']; m = statistics.median(len(c['forecast']['claim']) for c in F)
    rate = lambda xs: sum(c['forecast']['truth'] for c in xs) / len(xs)
    lo = [c for c in F if len(c['forecast']['claim']) <= m]; hi = [c for c in F if len(c['forecast']['claim']) > m]
    assert abs(rate(lo) - rate(hi)) <= 0.2, (rate(lo), rate(hi))
