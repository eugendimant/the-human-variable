import os,tempfile,unittest,concurrent.futures
from pathlib import Path
from server import app
class ClassroomTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();app.DB=Path(cls.tmp.name)/'test.sqlite';app.connect().close()
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def test_session_and_permission(self):
  s=app.create_session('ai01');self.assertFalse(app.session(s['code'])['admin']);self.assertTrue(app.session(s['code'],s['secret'])['admin'])
  with self.assertRaises(PermissionError):app.change(s['code'],'bad',reveal=True)
 def test_40_concurrent_students(self):
  s=app.create_session('ai01')
  with concurrent.futures.ThreadPoolExecutor(max_workers=40) as pool:
   rows=list(pool.map(lambda i:app.submit(s['code'],f'student-{i}',2),range(40)))
  self.assertEqual(len(rows),40);self.assertEqual(app.count(s['code']),40)
  self.assertEqual(app.results(s['code'],'')['count'],40)
  self.assertNotIn('by_challenge',app.results(s['code'],''))
  app.change(s['code'],s['secret'],reveal=True)
  self.assertIn('by_challenge',app.results(s['code'],''))
  with self.assertRaises(ValueError):app.submit(s['code'],'student-41',2)
 def test_replay_blocked(self):
  s=app.create_session('ai01');app.submit(s['code'],'student-one',1);app.submit(s['code'],'student-one',2)
  self.assertEqual(app.count(s['code']),1)
 def test_tutor_fallback(self):
  r=app.tutor('Why does this happen?','noy23');self.assertEqual(r['mode'],'curated-offline');self.assertTrue(r['answer'])
  with self.assertRaises(ValueError):app.tutor('Hello','not-real')
 def test_invalid_challenge(self):
  with self.assertRaises(ValueError):app.create_session('fake')
if __name__=='__main__':unittest.main()
