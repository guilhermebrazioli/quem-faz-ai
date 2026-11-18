import hashlib,json
from pathlib import Path
files=['src/core.py','src/agente.py','src/retrieval.py','base/trechos.json']
for kind,dataset in [('adicional_v2','avaliacao/casos_internos_adicionais.json'),('cega_v3','avaliacao/casos_cegos_v1.json')]:
 out=Path('avaliacao/congelamento_'+kind+'.json')
 if out.exists():raise SystemExit('Manifesto existente')
 out.write_text(json.dumps({p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in files+[dataset]},indent=2),encoding='utf8')
