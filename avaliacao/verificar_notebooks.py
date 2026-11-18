import json,re
from pathlib import Path
for p in Path('notebooks').glob('*.ipynb'):
 nb=json.loads(p.read_text(encoding='utf8'));hits=[]
 for c in nb.get('cells',[]):
  source=''.join(c.get('source',[]))
  if re.search(r'[A-Za-z]:\\\\|/Users/|/home/',source):hits.append('código')
  for o in c.get('outputs',[]):
   text=''.join(o.get('text',[])) if isinstance(o.get('text',[]),list) else o.get('text','')
   if re.search(r'[A-Za-z]:\\\\|/Users/|/home/',text):hits.append('saída')
 print(p.name, 'caminhos absolutos encontrados:',hits)
