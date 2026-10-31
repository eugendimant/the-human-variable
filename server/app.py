"""HTTP server for the game, the live classroom and the tutor. Standard library only.

Run locally:   python start_classroom.py            (binds 127.0.0.1:8502)
In a container: HOST=0.0.0.0 PORT=8080 python -m server.app
Environment: see docs/DEPLOYMENT.md.
"""
from __future__ import annotations
import json, os, re, threading, time, urllib.parse
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from .classroom import CHALLENGES, ClassroomError, Store, public_challenge, ROOT
from .tutor import Tutor

DATA = Path(os.environ.get('THV_DATA_DIR', str(ROOT / 'server' / 'data')))
DATA.mkdir(parents=True, exist_ok=True)
STORE = Store(os.environ.get('THV_DB', str(DATA / 'classroom.sqlite3')))
TUTOR = Tutor(str(DATA / 'tutor_cache.sqlite3'))
PASSCODE = os.environ.get('THV_INSTRUCTOR_PASSCODE', '')
TRUST_PROXY = os.environ.get('THV_TRUST_PROXY', '') == '1'
FRAME_ANCESTORS = os.environ.get('THV_FRAME_ANCESTORS', "'self'")
STATIC = {'/': 'index.html', '/index.html': 'index.html', '/classroom': 'classroom.html', '/classroom.html': 'classroom.html'}
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
       f"font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors {FRAME_ANCESTORS}")

class Limiter:
    """Token bucket per (client ip, bucket name)."""
    # Per-client buckets (X-Client-Id, a random id each browser keeps) plus a generous per-IP ceiling,
    # because a whole class often shares one campus NAT address.
    RULES = {'read': (4.0, 20), 'write': (2.0, 12), 'create': (10 / 3600, 10), 'tutor': (0.5, 6),
             'ip_read': (150.0, 400), 'ip_write': (60.0, 200)}
    def __init__(self): self.b = defaultdict(lambda: [0.0, 0.0]); self.lock = threading.Lock()
    def allow(self, ip: str, name: str) -> bool:
        rate, burst = self.RULES[name]; now = time.time()
        with self.lock:
            tokens, last = self.b[(ip, name)]
            tokens = burst if last == 0 else min(burst, tokens + (now - last) * rate)
            if tokens < 1: self.b[(ip, name)] = [tokens, now]; return False
            self.b[(ip, name)] = [tokens - 1, now]; return True
LIMIT = Limiter()
CODE_RE = re.compile(r'^/api/rooms/([A-Z2-9]{4,8})(/[a-z.]+)?$')

class Handler(BaseHTTPRequestHandler):
    server_version = 'THV'; sys_version = ''
    def log_message(self, fmt, *args):
        if os.environ.get('THV_ACCESS_LOG') == '1': super().log_message(fmt, *args)

    def ip(self) -> str:
        if TRUST_PROXY and self.headers.get('X-Forwarded-For'): return self.headers['X-Forwarded-For'].split(',')[0].strip()
        return self.client_address[0]

    def headers_common(self):
        self.send_header('X-Content-Type-Options', 'nosniff'); self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Security-Policy', CSP); self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')

    def json(self, status: int, data, extra: dict | None = None):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status); self.send_header('Content-Type', 'application/json; charset=utf-8'); self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store'); self.headers_common()
        for k, v in (extra or {}).items(): self.send_header(k, v)
        self.end_headers(); self.wfile.write(body)

    def body(self) -> dict:
        n = int(self.headers.get('Content-Length') or 0)
        if n < 0 or n > 8192: raise ClassroomError('Request too large')
        if n and 'application/json' not in (self.headers.get('Content-Type') or ''): raise ClassroomError('Send JSON')
        d = json.loads(self.rfile.read(n) or b'{}')
        if not isinstance(d, dict): raise ClassroomError('Send a JSON object')
        return d

    def key(self) -> str: return self.headers.get('X-Instructor-Key', '')

    def client(self) -> str: return re.sub(r'[^A-Za-z0-9_-]', '', self.headers.get('X-Client-Id', ''))[:40]

    def allowed(self, kind: str) -> bool:
        ip = self.ip()
        if not LIMIT.allow(ip, 'ip_' + kind): return False
        return LIMIT.allow(ip + '|' + self.client(), kind)

    def do_GET(self):
        u = urllib.parse.urlsplit(self.path); p = u.path; qs = urllib.parse.parse_qs(u.query)
        try:
            if p in STATIC:
                f = ROOT / STATIC[p]; data = f.read_bytes()
                self.send_response(200); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(data)))
                self.send_header('Cache-Control', 'no-cache'); self.headers_common(); self.end_headers(); self.wfile.write(data); return
            if not self.allowed('read'): return self.json(429, {'error': 'Too many requests. Wait a moment.'}, {'Retry-After': '2'})
            if p == '/api/health': return self.json(200, {'ok': True, 'decisions': len(CHALLENGES), 'tutor': TUTOR.enabled})
            if p == '/api/tutor/status': return self.json(200, TUTOR.status((qs.get('client') or [''])[0][:40]))
            if p == '/api/challenges': return self.json(200, {'challenges': [public_challenge(c) for c in CHALLENGES.values()]})
            m = CODE_RE.match(p)
            if m:
                code, sub = m.group(1), m.group(2)
                if sub is None:
                    admin = bool(self.key()) and STORE.is_admin(code, self.key())
                    s = STORE.state(code, admin=admin)
                    if (qs.get('v') or [''])[0] == str(s['version']) + ':' + str(s['responses']) + ':' + str(s['participants']):
                        return self.json(200, {'same': True})
                    s['etag'] = f"{s['version']}:{s['responses']}:{s['participants']}"
                    if s.get('challenge'): s['decision'] = public_challenge(CHALLENGES[s['challenge']])
                    s['admin'] = admin
                    return self.json(200, s)
                if sub == '/export.csv':
                    data = STORE.export_csv(code, self.key()).encode('utf-8-sig')
                    self.send_response(200); self.send_header('Content-Type', 'text/csv; charset=utf-8'); self.send_header('Content-Disposition', f'attachment; filename="human-variable-{code}.csv"')
                    self.send_header('Content-Length', str(len(data))); self.send_header('Cache-Control', 'no-store'); self.headers_common(); self.end_headers(); self.wfile.write(data); return
            self.json(404, {'error': 'Not found'})
        except ClassroomError as e: self.json(e.status, {'error': str(e)})
        except Exception: self.json(500, {'error': 'Server error'})

    def do_POST(self):
        p = urllib.parse.urlsplit(self.path).path
        try:
            d = self.body()
            if p == '/api/tutor':
                if not LIMIT.allow(self.ip() + '|' + self.client(), 'tutor'): return self.json(429, {'error': 'Ask again in a few seconds.'}, {'Retry-After': '3'})
                return self.json(200, TUTOR.ask(d.get('question', ''), d.get('challenge'), str(d.get('client', ''))[:40] or self.ip()))
            if p == '/api/rooms':
                if not LIMIT.allow(self.ip(), 'create'): return self.json(429, {'error': 'Too many sessions created from this network. Try again later.'})
                if PASSCODE and str(d.get('passcode', '')) != PASSCODE: return self.json(403, {'error': 'Instructor passcode required'})
                return self.json(201, STORE.create(d.get('title', '')))
            if not self.allowed('write'): return self.json(429, {'error': 'Too many requests. Wait a moment.'}, {'Retry-After': '2'})
            m = CODE_RE.match(p)
            if m:
                code, sub = m.group(1), m.group(2)
                if sub == '/join': return self.json(200, STORE.join(code))
                if sub == '/responses': return self.json(200, STORE.submit(code, d.get('token', ''), d.get('answer'), d.get('confidence')))
                if sub == '/control': return self.json(200, STORE.control(code, self.key(), str(d.get('action', '')), d.get('challenge')))
            self.json(404, {'error': 'Not found'})
        except ClassroomError as e: self.json(e.status, {'error': str(e)})
        except (ValueError, json.JSONDecodeError): self.json(400, {'error': 'Malformed request'})
        except Exception: self.json(500, {'error': 'Server error'})

class Server(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 128

def serve(host: str | None = None, port: int | None = None):
    host = host or os.environ.get('HOST', '127.0.0.1'); port = port or int(os.environ.get('PORT', '8502'))
    httpd = Server((host, port), Handler)
    print(f'The Human Variable on http://{"localhost" if host in ("127.0.0.1", "0.0.0.0") else host}:{port}/   classroom: /classroom   tutor: {"Gemini" if TUTOR.enabled else "curated only"}', flush=True)
    httpd.serve_forever()

if __name__ == '__main__':
    serve()
