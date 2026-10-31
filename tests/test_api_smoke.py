import unittest
from server import app
class APISmoke(unittest.TestCase):
 def test_challenge_index_has_all_formats(self):
  challenges=[{'id':c['id'],'format':c.get('format','choice')} for c in app.BANK['challenges']]
  self.assertEqual(len(challenges),60)
  self.assertEqual(set(x['format'] for x in challenges),{'choice','multi','estimate'})
 def test_public_challenges_exclude_answers(self):
  public=[{'id':c['id'],'title':c['title'],'question':c['question'],'options':c.get('options',[]),'format':c.get('format','choice'),'estimate':c.get('estimate')} for c in app.BANK['challenges']]
  self.assertTrue(all('answer' not in x for x in public))
