import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
BANK = json.loads((ROOT / 'src' / 'bank.json').read_text(encoding='utf-8'))
