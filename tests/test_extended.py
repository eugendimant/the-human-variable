import unittest, json, tempfile
from pathlib import Path
from server import app
class Extended(unittest.TestCase):
 def test_all_sources_have_identifiers(self):
  for key,s in app.SOURCES.items():
   self.assertEqual(key,s['id']);self.assertTrue(s.get('doi') or s.get('url'))
 def test_all_challenges_have_source(self):
  for c in app.CHALLENGES.values():
   self.assertTrue(c['sources']);self.assertTrue(all(s in app.SOURCES for s in c['sources']))
 def test_no_unverified_marked_as_verified(self):
  for s in app.SOURCES.values():self.assertEqual(s['verification_status'],'pending_independent_primary_source_review')
 def test_duplicate_submissions_not_counted(self):
  original=app.DB
  with tempfile.TemporaryDirectory() as d:
   app.DB=Path(d)/'test.sqlite';s=app.create_session('ai01')
   self.assertTrue(app.submit(s['code'],'person-123',0)['accepted'])
   self.assertFalse(app.submit(s['code'],'person-123',1)['accepted'])
   self.assertEqual(app.count(s['code']),1)
  app.DB=original
 def test_switch_challenge_hides_previous_answers(self):
  original=app.DB
  with tempfile.TemporaryDirectory() as d:
   app.DB=Path(d)/'test.sqlite';s=app.create_session('ai01')
   app.submit(s['code'],'person-123',0)
   app.change(s['code'],s['secret'],challenge='ai02')
   self.assertEqual(app.count(s['code']),0)
   self.assertEqual(app.results(s['code'],s['secret'])['count'],0)
  app.DB=original
 def test_instructor_secret_required(self):
  original=app.DB
  with tempfile.TemporaryDirectory() as d:
   app.DB=Path(d)/'test.sqlite';s=app.create_session('ai01')
   with self.assertRaises(PermissionError):app.change(s['code'],'wrong',reveal=True)
  app.DB=original
if __name__=='__main__':unittest.main()
