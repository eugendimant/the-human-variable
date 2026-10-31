"""Standard-library classroom server. Run: python -m server.app"""
import json, sqlite3, secrets, threading, os, time, urllib.parse, urllib.request
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DB=Path(os.environ.get('THV_DB',str(ROOT/'server'/'classroom.sqlite3')))
LOCK=threading.RLock()
BANK=json.loads((ROOT/'src'/'bank.json').read_text())
CHALLENGES={c['id']:c for c in BANK['challenges']}
SOURCES=BANK['sources']

def connect():
 c=sqlite3.connect(DB,timeout=10)
 c.execute('PRAGMA busy_timeout=10000')
 c.execute('CREATE TABLE IF NOT EXISTS sessions(code TEXT PRIMARY KEY,secret TEXT NOT NULL,challenge TEXT,revealed INTEGER DEFAULT 0,created INTEGER NOT NULL)')
 c.execute('CREATE TABLE IF NOT EXISTS responses(code TEXT,participant TEXT,challenge TEXT,answer TEXT,created INTEGER,PRIMARY KEY(code,participant,challenge))')
 c.commit();return c

def create_session(challenge):
 if challenge not in CHALLENGES:raise ValueError('Unknown challenge')
 with LOCK:
  with connect() as db:
   for _ in range(10):
    code=secrets.token_hex(3).upper();secret=secrets.token_urlsafe(24)
    try:db.execute('INSERT INTO sessions(code,secret,challenge,created) VALUES(?,?,?,?)',(code,secret,challenge,int(time.time())));return {'code':code,'secret':secret,'challenge':challenge}
    except sqlite3.IntegrityError:pass
 raise RuntimeError('Unable to allocate session')

def session(code,secret=None):
 with connect() as db:
  s=db.execute('SELECT code,secret,challenge,revealed FROM sessions WHERE code=?',(code,)).fetchone()
  if not s:raise LookupError('Session not found')
  admin=secrets.compare_digest(str(secret or ''),s[1])
  return {'code':s[0],'challenge':s[2],'revealed':bool(s[3]),'admin':admin}

def submit(code,participant,answer):
 if not isinstance(participant,str) or not 3<=len(participant)<=80:raise ValueError('Invalid participant ID')
 if not isinstance(answer,(str,int,float,list)) or len(json.dumps(answer))>1000:raise ValueError('Invalid answer')
 with LOCK:
  with connect() as db:
   s=db.execute('SELECT challenge,revealed FROM sessions WHERE code=?',(code,)).fetchone()
   if not s:raise LookupError('Session not found')
   if s[1]:raise ValueError('Reveal already completed')
   challenge=CHALLENGES[s[0]]
   fmt=challenge.get('format','choice')
   if fmt=='choice' and (type(answer) is not int or not 0<=answer<len(challenge['options'])):raise ValueError('Invalid choice')
   if fmt=='multi' and (not isinstance(answer,list) or len(answer)!=2 or any(type(a) is not int or not 0<=a<len(challenge['options']) for a in answer) or len(set(answer))!=2):raise ValueError('Invalid multiple answer')
   if fmt=='estimate' and (type(answer) not in (int,float) or not -1e9<=answer<=1e9):raise ValueError('Invalid estimate')
   cur=db.execute('INSERT OR IGNORE INTO responses VALUES(?,?,?,?,?)',(code,participant,s[0],json.dumps(answer),int(time.time())))
  accepted=cur.rowcount==1
 return {'accepted':accepted}

def change(code,secret,challenge=None,reveal=None):
 s=session(code,secret)
 if not s['admin']:raise PermissionError('Instructor credential required')
 if challenge is not None and challenge not in CHALLENGES:raise ValueError('Unknown challenge')
 with LOCK:
  with connect() as db:
   if challenge is not None:db.execute('UPDATE sessions SET challenge=?,revealed=0 WHERE code=?',(challenge,code))
   if reveal is not None:db.execute('UPDATE sessions SET revealed=? WHERE code=?',(int(bool(reveal)),code))
 return session(code,secret)

def results(code,secret):
 s=session(code,secret)
 if not s['admin'] and not s['revealed']:return {'count':count(code),'revealed':False}
 with connect() as db:rows=db.execute('SELECT challenge,answer FROM responses WHERE code=? AND challenge=?',(code,s['challenge'])).fetchall()
 counts={}
 for cid,ans in rows:
  counts.setdefault(cid,{})
  counts[cid][ans]=counts[cid].get(ans,0)+1
 return {'count':len(rows),'by_challenge':counts,'revealed':s['revealed']}

def count(code):
 with connect() as db:return db.execute('SELECT count(*) FROM responses WHERE code=? AND challenge=(SELECT challenge FROM sessions WHERE code=?)',(code,code)).fetchone()[0]

def tutor(question,source_id):
 if source_id not in SOURCES:raise ValueError('Unknown source')
 if not isinstance(question,str) or not 1<=len(question)<=400:raise ValueError('Question must be 1–400 characters')
 source=SOURCES[source_id]
 matches=[c for c in BANK['challenges'] if source_id in c['sources']]
 follow=[f for c in matches for f in c.get('follow',[]) if f.get('a')]
 q=set(question.lower().split());ranked=sorted(follow,key=lambda f:len(q.intersection(f['q'].lower().split())),reverse=True)
 overlap=len(q.intersection(ranked[0]['q'].lower().split())) if ranked else 0
 answer=ranked[0]['a'] if overlap>=2 else source.get('takeaway','Refer to the published study for details.')
 return {'answer':answer,'source':source['url'],'mode':'curated-offline','note':'Curated explanation, not a live AI answer.'}

class Handler(BaseHTTPRequestHandler):
 def send(self,status,data):
  body=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body)
 def payload(self):
  n=int(self.headers.get('Content-Length','0'))
  if n<0 or n>4096:raise ValueError('Request too large')
  return json.loads(self.rfile.read(n) or b'{}')
 def do_GET(self):
  u=urllib.parse.urlsplit(self.path);p=u.path;args=urllib.parse.parse_qs(u.query)
  try:
   if p=='/':
    data=(ROOT/'index.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);return
   if p=='/classroom':
    data=(ROOT/'classroom.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);return
   if p=='/api/health':return self.send(200,{'ok':True})
   if p=='/api/challenges':return self.send(200,{'challenges':[{'id':c['id'],'title':c['title'],'question':c['question'],'options':c.get('options',[]),'format':c.get('format','choice'),'estimate':c.get('estimate')} for c in BANK['challenges']]})
   if p.startswith('/api/sessions/'):
    parts=p.split('/');code=parts[3];secret=self.headers.get('X-Instructor-Key','')
    if len(parts)==5 and parts[4]=='results':return self.send(200,results(code,secret))
    return self.send(200,session(code,secret))
   self.send(404,{'error':'Not found'})
  except Exception as e:self.send(400,{'error':str(e)})
 def do_POST(self):
  try:
   d=self.payload();p=self.path
   if p=='/api/sessions':return self.send(201,create_session(d.get('challenge','ai01')))
   if p=='/api/tutor':return self.send(200,tutor(d.get('question'),d.get('source')))
   if p.startswith('/api/sessions/'):
    parts=p.split('/');code=parts[3]
    if len(parts)==5 and parts[4]=='responses':return self.send(200,submit(code,d.get('participant'),d.get('answer')))
    if len(parts)==5 and parts[4]=='control':return self.send(200,change(code,self.headers.get('X-Instructor-Key',''),d.get('challenge'),d.get('reveal')))
   self.send(404,{'error':'Not found'})
  except PermissionError as e:self.send(403,{'error':str(e)})
  except Exception as e:self.send(400,{'error':str(e)})

if __name__=='__main__':
 DB.parent.mkdir(parents=True,exist_ok=True)
 with connect():pass
 ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','8502'))),Handler).serve_forever()
