"""Congela código, base e casos da rodada final (hash SHA-256)."""
import hashlib, json
from pathlib import Path
files=['src/core.py','src/agente.py','src/retrieval.py','base/trechos.json','avaliacao/casos_cegos_v1.json']
out=Path('avaliacao/congelamento_final.json')
if out.exists(): raise SystemExit('Manifesto já existe: '+str(out))
out.write_text(json.dumps({p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in files},indent=2),encoding='utf8')
print('Criado',out)
