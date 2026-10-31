"""Drop links to third-party re-hosted copies and working-paper PDFs from source provenance (review 10). Idempotent.
The text_read line keeps saying which version was read; the DOI stays the reference link."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; p = ROOT / 'src/bank.json'; bank = json.loads(p.read_text())
REHOST = r'gwern\.net|rivista\.ai|scispace\.com|hods\.org|mattalldian\.com|econreadinggroup|cesifo1_wp|/wp\d|workingpaper'
n = 0
for s in bank['sources'].values():
    v = s.get('verification', {})
    if re.search(REHOST, v.get('text_url', ''), re.I): v.pop('text_url'); n += 1
p.write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('dropped', n)
