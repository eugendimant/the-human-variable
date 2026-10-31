from pathlib import Path
import json,re
root=Path(__file__).resolve().parent.parent
bank=json.loads((root/'src/bank.json').read_text())
p=root/'index.html'; html=p.read_text()
pattern=r'(<script>const BANK = )\{.*?\}(;\s*</script>)'
replacement=lambda m:m.group(1)+json.dumps(bank,ensure_ascii=False,separators=(',',':'))+m.group(2)
new,n=re.subn(pattern,replacement,html,count=1,flags=re.S)
assert n==1,'Cannot find embedded bank'
p.write_text(new)
print('Rebuilt',p)
