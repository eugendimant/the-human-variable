"""Review 47 (m-1): tutor questions that the stored text answers but no route caught. Adds alternatives to five existing routes in
src/bank.json tutorRoutes (both the page tutor and server/tutor.py read this table). Idempotent. Run tools/tutor_golden.py after."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text())
R = B['tutorRoutes']['routes']
ADD = {
    'who': r'\bwho (took part|participated|were the subjects|were they|were involved)\b|\bsubjects\b',
    'design': r'\b(was|is) (it|this|that) an? (field|lab|laboratory|online|survey|natural|randomi[sz]ed|real) (experiment|study|trial)\b|\bwhat (kind|type) of (study|experiment|trial)\b',
    'authors': r'\bwhere (can|do|could) (i|we) (read|find|get) (the|this|it|that) (paper|study|article|full text)\b',
    'summary': r'\bone[- ]line\b|\btakeaway\b',
    'catch': r'\bhow (reliable|sure|certain|robust|solid) (is|are|can)\b|\bhow sure can (i|we) be\b',
}
for name, add in ADD.items():
    i = next(k for k, (n, _) in enumerate(R) if n == name); rx = R[i][1]
    if add in rx: continue
    R[i][1] = rx + '|' + add
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
