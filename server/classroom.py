"""Live classroom sessions: instructor-controlled rounds, anonymous participants, aggregate reveals.

Storage is SQLite in WAL mode (one file, safe for one server process with many threads).
State that every participant polls is cached in memory and versioned, so 50 phones polling
every two seconds cost a dictionary lookup, not a database query.
"""
from __future__ import annotations
import csv, hashlib, hmac, io, json, os, re, secrets, sqlite3, statistics, threading, time
from pathlib import Path
from . import scoring

ROOT = Path(__file__).resolve().parents[1]
BANK = json.loads((ROOT / 'src' / 'bank.json').read_text(encoding='utf-8'))
LIVE_SOURCES = {k for k, s in BANK['sources'].items() if s.get('verification', {}).get('status') != 'quarantined'}
CHALLENGES = {c['id']: c for c in BANK['challenges'] if all(s in LIVE_SOURCES for s in c['sources'])}

RETENTION_HOURS = float(os.environ.get('THV_RETENTION_HOURS', '48'))
MAX_PARTICIPANTS = int(os.environ.get('THV_MAX_PARTICIPANTS', '120'))
CLASS_LOCK_HOURS = float(os.environ.get('THV_CLASS_LOCK_HOURS', '3'))
# A class holds the lock only while its instructor is active: the open console refreshes it, students joining do not.
CLASS_LOCK_IDLE_MIN = float(os.environ.get('THV_CLASS_LOCK_IDLE_MIN', '20'))  # measured from instructor activity only
CODE_ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'  # no 0/O/1/I

class ClassroomError(Exception):
    status = 400
class NotFound(ClassroomError):
    status = 404
class Forbidden(ClassroomError):
    status = 403
class Conflict(ClassroomError):
    status = 409

def _h(token: str) -> str: return hashlib.sha256(token.encode()).hexdigest()

def answer_text(c, a):
    """Readable answer for the CSV export."""
    f, o = c.get('format'), c.get('options') or []
    try:
        if f in ('choice', 'causal'): return o[a]
        if f == 'multi': return ' + '.join(o[i] for i in a)
        if f == 'rank': return ' > '.join(o[i] for i in a)
        if f == 'allocate': return '; '.join(f'{o[i]}: {v}' for i, v in enumerate(a))
        if f == 'delegate':
            ch = c['delegate']['choices']; return '; '.join(f"{t['text']}: {ch[v]}" for t, v in zip(c['delegate']['tasks'], a))
        if f == 'forecast': return f'{a}% true'
        if f == 'estimate': return f"{a}{c['estimate'].get('unit', '%')}"
    except (IndexError, KeyError, TypeError): pass
    return ''

class Store:
    def __init__(self, path: str | Path):
        self.path = str(path); self._local = threading.local(); self.lock = threading.Lock()
        self.cache: dict[str, dict] = {}; self._beats: dict[str, float] = {}
        db = self.db()
        db.executescript('''
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS sessions(code TEXT PRIMARY KEY, secret_hash TEXT NOT NULL, title TEXT, challenge TEXT, phase TEXT NOT NULL DEFAULT 'lobby', version INTEGER NOT NULL DEFAULT 1, created REAL NOT NULL, touched REAL NOT NULL, played TEXT NOT NULL DEFAULT '[]');
        CREATE TABLE IF NOT EXISTS participants(code TEXT, token_hash TEXT, num INTEGER, joined REAL, PRIMARY KEY(code, token_hash));
        CREATE TABLE IF NOT EXISTS responses(code TEXT, num INTEGER, challenge TEXT, answer TEXT, confidence INTEGER, score REAL, correct INTEGER, created REAL, PRIMARY KEY(code, num, challenge));
        CREATE INDEX IF NOT EXISTS r_cc ON responses(code, challenge);
        ''')
        cols = {r[1] for r in db.execute('PRAGMA table_info(sessions)')}
        if 'revealed' not in cols: db.execute("ALTER TABLE sessions ADD COLUMN revealed TEXT NOT NULL DEFAULT '[]'")
        if 'joining' not in cols: db.execute("ALTER TABLE sessions ADD COLUMN joining INTEGER NOT NULL DEFAULT 1")
        if 'beat' not in cols: db.execute("ALTER TABLE sessions ADD COLUMN beat REAL NOT NULL DEFAULT 0")  # last instructor activity
        db.commit()

    def db(self) -> sqlite3.Connection:
        c = getattr(self._local, 'c', None)
        if c is None:
            c = sqlite3.connect(self.path, timeout=15, check_same_thread=False)
            c.execute('PRAGMA busy_timeout=15000'); c.execute('PRAGMA synchronous=NORMAL')
            self._local.c = c
        return c

    # ---- instructor ----
    def create(self, title: str = '') -> dict:
        self.purge()
        title = str(title or '')[:80]
        secret = secrets.token_urlsafe(24); now = time.time()
        with self.lock:
            db = self.db()
            for _ in range(20):
                code = ''.join(secrets.choice(CODE_ALPHABET) for _ in range(5))
                try:
                    db.execute('INSERT INTO sessions(code, secret_hash, title, created, touched, beat) VALUES(?,?,?,?,?,?)', (code, _h(secret), title, now, now, now)); db.commit()
                    self.cache.pop(code, None)
                    return {'code': code, 'secret': secret, 'title': title}
                except sqlite3.IntegrityError:
                    continue
        raise ClassroomError('Could not allocate a session code')

    def _row(self, code: str):
        r = self.db().execute('SELECT code, secret_hash, title, challenge, phase, version, created, played FROM sessions WHERE code=?', (code,)).fetchone()
        if not r: raise NotFound('No session with that code. Check the code on the instructor screen.')
        return r

    def is_admin(self, code: str, secret: str) -> bool:
        r = self._row(code); return bool(secret) and hmac.compare_digest(r[1], _h(secret))

    def require_admin(self, code: str, secret: str):
        if not self.is_admin(code, secret): raise Forbidden('Instructor key required')

    def control(self, code: str, secret: str, action: str, challenge: str | None = None) -> dict:
        self.require_admin(code, secret)
        r = self._row(code); phase = r[4]; played = json.loads(r[7])
        if action == 'open':
            if challenge not in CHALLENGES: raise ClassroomError('Unknown decision')
            if challenge not in played: played.append(challenge)
            rev = [x for x in json.loads(self.db().execute('SELECT revealed FROM sessions WHERE code=?', (code,)).fetchone()[0]) if x != challenge]
            sql, args = 'UPDATE sessions SET challenge=?, phase=?, played=?, revealed=?', [challenge, 'open', json.dumps(played), json.dumps(rev)]
        elif action == 'close':
            if phase != 'open': raise Conflict('Nothing is open')
            sql, args = 'UPDATE sessions SET phase=?', ['closed']
        elif action == 'reveal':
            if phase not in ('open', 'closed'): raise Conflict('Open a decision first')
            rev = json.loads(self.db().execute('SELECT revealed FROM sessions WHERE code=?', (code,)).fetchone()[0])
            if r[3] not in rev: rev.append(r[3])
            sql, args = 'UPDATE sessions SET phase=?, revealed=?', ['revealed', json.dumps(rev)]
        elif action in ('lockjoin', 'unlockjoin'):
            sql, args = 'UPDATE sessions SET joining=?', [0 if action == 'lockjoin' else 1]
        elif action == 'lobby':
            sql, args = 'UPDATE sessions SET phase=?', ['lobby']
        elif action == 'end':
            self.delete(code, secret); return {'ended': True}
        else:
            raise ClassroomError('Unknown action')
        with self.lock:
            db = self.db(); db.execute(sql + ', version=version+1, touched=?, beat=? WHERE code=?', (*args, time.time(), time.time(), code)); db.commit()
            self.cache.pop(code, None); self._open = None; self._lock = None
        return self.state(code, admin=True)

    def delete(self, code: str, secret: str):
        self.require_admin(code, secret)
        with self.lock:
            db = self.db()
            for t in ('responses', 'participants', 'sessions'): db.execute(f'DELETE FROM {t} WHERE code=?', (code,))
            db.commit(); self.cache.pop(code, None)

    # ---- participants ----
    def join(self, code: str) -> dict:
        code = str(code or '').strip().upper()[:8]
        self._row(code)
        with self.lock:
            db = self.db()
            n = db.execute('SELECT COUNT(*) FROM participants WHERE code=?', (code,)).fetchone()[0]
            if n >= MAX_PARTICIPANTS: raise Conflict('This session is full')
            if not db.execute('SELECT joining FROM sessions WHERE code=?', (code,)).fetchone()[0]: raise Conflict('The instructor has closed joining for this session.')
            token = secrets.token_urlsafe(18)
            db.execute('INSERT INTO participants VALUES(?,?,?,?)', (code, _h(token), n + 1, time.time()))
            db.execute('UPDATE sessions SET touched=? WHERE code=?', (time.time(), code)); db.commit()
            self.cache.pop(code, None)
        return {'code': code, 'token': token, 'number': n + 1}

    def _participant(self, code: str, token: str) -> int:
        r = self.db().execute('SELECT num FROM participants WHERE code=? AND token_hash=?', (code, _h(str(token or '')))).fetchone()
        if not r: raise Forbidden('Join the session first')
        return r[0]

    def submit(self, code: str, token: str, answer, confidence=None, challenge=None) -> dict:
        r = self._row(code); num = self._participant(code, token)
        if r[4] != 'open': raise Conflict('Responses are closed for this decision')
        if challenge is not None and challenge != r[3]: raise Conflict('The class has moved on; that answer was for an earlier decision')   # never filed under another decision (audit 49, M1)
        c = CHALLENGES[r[3]]
        if not scoring.valid(c, answer): raise ClassroomError('That answer does not fit this decision')
        if c['format'] not in ('forecast', 'allocate'):  # both are probability statements already
            if type(confidence) not in (int, float) or not 0 <= confidence <= 100: raise ClassroomError('Confidence must be 0 to 100')
            confidence = int(round(confidence))
        else:
            confidence = None
        s = scoring.score(c, answer)
        with self.lock:
            db = self.db()
            cur = db.execute('INSERT OR IGNORE INTO responses VALUES(?,?,?,?,?,?,?,?)', (code, num, c['id'], json.dumps(answer), confidence, s['score'], int(s['correct']), time.time()))
            db.execute('UPDATE sessions SET touched=? WHERE code=?', (time.time(), code))
            db.commit(); accepted = cur.rowcount == 1
            if accepted: self.cache.pop(code, None)
        return {'accepted': accepted, 'message': 'Recorded' if accepted else 'You already answered this decision'}

    # ---- reads ----
    def heartbeat(self, code: str):
        """The instructor console is open: keep the class alive (at most one write a minute)."""
        now = time.time(); last = self._beats.get(code, 0)
        if now - last < 60: return
        self._beats[code] = now
        with self.lock:
            db = self.db(); db.execute('UPDATE sessions SET touched=?, beat=? WHERE code=?', (now, now, code)); db.commit()

    def state(self, code: str, admin: bool = False) -> dict:
        code = str(code or '').upper()
        if admin: self.heartbeat(code)
        hit = self.cache.get(code)
        if hit is None or time.time() - hit['_t'] > 30:
            r = self._row(code); db = self.db()
            n_part = db.execute('SELECT COUNT(*) FROM participants WHERE code=?', (code,)).fetchone()[0]
            n_resp = db.execute('SELECT COUNT(*) FROM responses WHERE code=? AND challenge=?', (code, r[3])).fetchone()[0] if r[3] else 0
            joining = db.execute('SELECT joining FROM sessions WHERE code=?', (code,)).fetchone()[0]
            hit = {'_t': time.time(), 'code': r[0], 'title': r[2], 'challenge': r[3], 'phase': r[4], 'version': r[5], 'participants': n_part, 'responses': n_resp, 'joining': bool(joining)}
            if r[4] == 'revealed' and r[3]: hit['aggregate'] = self.aggregate(code, r[3])
            self.cache[code] = hit
        out = {k: v for k, v in hit.items() if not k.startswith('_')}
        if not admin and out['phase'] != 'revealed': out.pop('aggregate', None)
        return out

    def aggregate(self, code: str, cid: str) -> dict:
        c = CHALLENGES[cid]; f = c['format']
        rows = self.db().execute('SELECT answer, confidence, score, correct FROM responses WHERE code=? AND challenge=?', (code, cid)).fetchall()
        ans = [json.loads(a) for a, *_ in rows]; n = len(rows)
        out = {'n': n, 'format': f, 'meanScore': round(100 * sum(r[2] for r in rows) / n) if n else None,
               'shareCorrect': round(100 * sum(r[3] for r in rows) / n) if n else None,
               'meanConfidence': round(statistics.mean([r[1] for r in rows if r[1] is not None])) if any(r[1] is not None for r in rows) else None}
        if f in ('choice', 'causal', 'multi'):
            counts = [0] * len(c['options'])
            for a in ans:
                for i in (a if isinstance(a, list) else [a]): counts[i] += 1
            out['counts'] = counts
        elif f in ('estimate', 'forecast'):
            lo, hi = (c['estimate']['min'], c['estimate']['max']) if f == 'estimate' else (0, 100)
            bins = 10; w = (hi - lo) / bins; hist = [0] * bins
            for a in ans: hist[min(bins - 1, int((a - lo) / w))] += 1
            pts = {}
            for a in ans: pts[a] = pts.get(a, 0) + 1
            out.update({'points': sorted([v, k] for v, k in pts.items()), 'hist': hist, 'lo': lo, 'hi': hi, 'median': statistics.median(ans) if ans else None, 'mean': round(statistics.mean(ans), 1) if ans else None})
        elif f == 'rank':
            k = len(c['options']); pos = [0.0] * k
            for a in ans:
                for p, item in enumerate(a): pos[item] += p + 1
            out['meanPosition'] = [round(p / n, 2) if n else None for p in pos]
        elif f == 'allocate':
            k = len(c['options']); out['meanShare'] = [round(sum(a[i] for a in ans) / n, 1) if n else None for i in range(k)]
        elif f == 'delegate':
            out['taskCounts'] = [[sum(1 for a in ans if a[t] == m) for m in range(len(c['delegate']['choices']))] for t in range(len(c['delegate']['tasks']))]
        return out

    def class_lock(self) -> tuple[bool, set]:
        """While any class with participants has been active in the last CLASS_LOCK_HOURS, evidence is released
        only for decisions that class has already revealed. Returns (locked, allowed ids). Cached for 2 s."""
        now = time.time(); hit = getattr(self, '_lock', None)
        if hit and now - hit[0] < 2: return hit[1]
        since = now - min(CLASS_LOCK_HOURS * 3600, CLASS_LOCK_IDLE_MIN * 60)
        rows = self.db().execute("SELECT s.revealed FROM sessions s WHERE s.beat > ? AND s.phase != 'ended' AND (s.phase IN ('open', 'closed') OR EXISTS (SELECT 1 FROM participants p WHERE p.code = s.code))", (since,)).fetchall()
        # With several classes, a decision is released only once every running class has revealed it.
        sets = [set(json.loads(rv)) for (rv,) in rows]
        allowed = set.intersection(*sets) if sets else set()
        val = (bool(rows), allowed); self._lock = (now, val); return val

    def open_challenges(self) -> set:
        """Decisions currently open or closed-but-unrevealed in a session active in the last six hours (cached for 2 s).
        Settled (tests/test_http.py): an open question stays held while the console is quiet, since an instructor may talk for longer than the lock's idle window."""
        now = time.time(); hit = getattr(self, '_open', None)
        if hit and now - hit[0] < 2: return hit[1]
        rows = self.db().execute("SELECT challenge FROM sessions WHERE phase IN ('open','closed') AND beat > ?", (now - 6 * 3600,)).fetchall()   # instructor activity only, as for the lock
        val = {r[0] for r in rows if r[0]}; self._open = (now, val); return val

    # score: 0 to 100 for most formats; forecasts and point splits run from -100 (confident miss, or all points on a wrong option) to 100.
    def export_csv(self, code: str, secret: str) -> str:
        self.require_admin(code, secret)
        rows = self.db().execute('SELECT num, challenge, answer, confidence, score, correct, created FROM responses WHERE code=? ORDER BY challenge, num', (code,)).fetchall()
        buf = io.StringIO(); w = csv.writer(buf)
        w.writerow(['participant', 'decision_id', 'decision_title', 'format', 'answer', 'answer_text', 'confidence', 'score', 'correct', 'utc_time'])
        safe = lambda x: x if re.fullmatch(r'-?\d+(\.\d+)?\s?%?[A-Za-z$]*', x) else "'" + x if x[:1] in '=+-@\t\r' else x   # a plain negative number is not a formula
        for num, cid, a, conf, sc, ok, t in rows:
            c = CHALLENGES.get(cid, {})
            w.writerow([f'P{num:03d}', cid, safe(str(c.get('title', ''))), c.get('format', ''), a, safe(answer_text(c, json.loads(a))), '' if conf is None else conf, round(100 * sc), ok, time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t))])
        return buf.getvalue()

    def purge(self):
        cutoff = time.time() - RETENTION_HOURS * 3600
        with self.lock:
            db = self.db(); old = [r[0] for r in db.execute('SELECT code FROM sessions WHERE touched < ?', (cutoff,))]
            for code in old:
                for t in ('responses', 'participants', 'sessions'): db.execute(f'DELETE FROM {t} WHERE code=?', (code,))
                self.cache.pop(code, None)
            db.commit()
        return len(old)

def public_challenge(c: dict) -> dict:
    """Everything a participant needs to answer, nothing that reveals the answer."""
    keep = ('id', 'track', 'title', 'scene', 'question', 'options', 'format', 'rankLabel', 'dag', 'case', 'study')  # concept can name the result
    out = {k: c[k] for k in keep if k in c}
    if c['format'] == 'estimate':
        out['estimate'] = {k: c['estimate'][k] for k in ('min', 'max', 'label', 'unit', 'step', 'tolerance') if k in c['estimate']}
        n = str((c.get('study') or {}).get('n', ''))
        if any(abs(float(m) - c['estimate']['target']) <= c['estimate']['tolerance'] for m in re.findall(r'-?\d+(?:\.\d+)?', n.replace(',', ''))):
            out['study'] = {k: v for k, v in c['study'].items() if k != 'n'}   # a sample whose numbers sit in the scoring band stays off the wire, as off the screen (review 30)
    if c['format'] == 'forecast': out['forecast'] = {'claim': c['forecast']['claim']}
    if c['format'] == 'allocate': out['allocate'] = {k: c['allocate'][k] for k in ('total', 'step', 'label', 'prefix', 'suffix') if k in c['allocate']}  # allow-list: nothing that names the best arm
    if c['format'] == 'delegate': out['delegate'] = {'choices': c['delegate']['choices'], 'tasks': [{'text': t['text']} for t in c['delegate']['tasks']]}
    if 'dag' in c:  # the written explanation and the masked label state the answer; edge styles mark the questioned link
        d = c['dag']; out['dag'] = {k: v for k, v in d.items() if k not in ('alt', 'nodes', 'edges')}
        ren = {n['id']: f'n{i}' for i, n in enumerate(d['nodes'])}   # neutral ids: a masked node's id must not name it
        out['dag']['nodes'] = [{k: v for k, v in n.items() if k not in ('label', 'id')} | {'id': ren[n['id']], 'label': '?' if n.get('mask') else n['label']} for n in d['nodes']]
        out['dag']['edges'] = []   # links narrow the options; they arrive with the evidence
    if c['format'] == 'multi': out['pick'] = len(c['multiAnswers'])
    if c['format'] == 'rank': out['nRank'] = len(c['rankAnswer'])
    return out
