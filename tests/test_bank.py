import json,unittest,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
B=json.loads((ROOT/'src/bank.json').read_text())
class BankTests(unittest.TestCase):
 def test_count(self): self.assertGreaterEqual(len(B['challenges']),60)
 def test_unique(self): self.assertEqual(len({x['id'] for x in B['challenges']}),len(B['challenges']))
 def test_source_integrity(self):
  for c in B['challenges']:
   self.assertTrue(c['sources'],c['id'])
   for ref in c['sources']: self.assertIn(ref,B['sources'])
  for s in B['sources'].values():
   self.assertEqual(s['kind'],'peer-reviewed')
   self.assertTrue(s['url'].startswith('https://doi.org/'))
 def test_content(self):
  for c in B['challenges']:
   for key in ('title','question','explain','boundary','implication','format'):
    self.assertTrue(c.get(key),f'{c["id"]}: {key}')
 def test_html_embedded_bank_matches(self):
  h=(ROOT/'index.html').read_text()
  m=re.search(r'<script>const BANK = (\{.*?\});\s*</script>',h,re.S)
  self.assertIsNotNone(m)
  self.assertEqual(json.loads(m.group(1)),B)
if __name__=='__main__':unittest.main()
