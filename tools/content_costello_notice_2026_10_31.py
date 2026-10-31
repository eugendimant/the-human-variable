"""Eugen Dimant, 2026-10-31: the expression of concern on Costello et al. (2024) has been officially removed. Remove every mention."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
bank['sources']['costello24']['verification'].pop('note', None)
bank['sources']['costello24'].pop('flags', None)
C['axb15']['boundary'] = 'Online experiments with 2,044 conspiracy believers, in conversations with GPT-4 Turbo.'
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
