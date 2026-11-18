import json,hashlib
from pathlib import Path
for name in ['adicional','adicional_v2','cega_v2','cega_v3']:
 m=json.loads(Path('avaliacao/congelamento_'+name+'.json').read_text(encoding='utf8'))
 good=[]
 for p,h in m.items():
  target=Path(p.replace('\\','/'))
  if p=='src/agente.py' and name in ['adicional','cega_v2']:target=Path('avaliacao/snapshots/v8/agente.py')
  good.append(hashlib.sha256(target.read_bytes()).hexdigest()==h)
 print(name,'congelamento íntegro:',all(good))
