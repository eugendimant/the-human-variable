import json,unittest,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
B=json.loads((R/'src/bank.json').read_text())
class QualityTests(unittest.TestCase):
 def test_formats_have_valid_answers(self):
  for c in B['challenges']:
   with self.subTest(id=c['id']):
    fmt=c['format']; self.assertIn(fmt,('choice','multi','estimate'))
    if fmt=='choice':self.assertIsInstance(c['answer'],int);self.assertLess(c['answer'],len(c['options']));self.assertGreaterEqual(c['answer'],0)
    elif fmt=='multi':
     a=c['multiAnswers'];self.assertEqual(len(a),2);self.assertEqual(len(set(a)),2);self.assertTrue(all(0<=i<len(c['options']) for i in a))
    else:
     e=c['estimate'];self.assertLess(e['min'],e['max']);self.assertLessEqual(e['min'],e['target']);self.assertLessEqual(e['target'],e['max']);self.assertGreater(e['tolerance'],0)
 def test_followups(self):
  for c in B['challenges']:
   with self.subTest(id=c['id']):
    self.assertGreaterEqual(len(c['follow']),3)
    for f in c['follow']:self.assertGreater(len(f['q']),8);self.assertGreater(len(f['a']),15)
 def test_all_tracks_and_sources(self):
  self.assertGreaterEqual(len(set(c['track'] for c in B['challenges'])),3)
  for c in B['challenges']:
   for s in c['sources']:self.assertIn(s,B['sources'])
 def test_source_dois_not_empty(self):
  for s in B['sources'].values():
   self.assertRegex(s['doi'],r'^10\.\d{4,9}/\S+$')
 def test_safe_content_no_script_markup(self):
  for c in B['challenges']:
   for field in ('title','question','explain','boundary','implication'):
    self.assertNotRegex(c[field],r'<script|javascript:',f'{c["id"]} {field}')
 def test_local_file_completeness(self):
  self.assertTrue((R/'streamlit_app.py').exists());self.assertTrue((R/'src/build.py').exists());self.assertTrue((R/'index.html').exists())
if __name__=='__main__':unittest.main()
