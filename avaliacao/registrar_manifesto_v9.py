import json,hashlib
from pathlib import Path
old=json.loads(Path('docs/manifesto_experimentos.json').read_text(encoding='utf8'))
old['versao_atual']='v9 - filtro preventivo de padrões suspeitos em B e C; não é um release Git'
old['manifesto_atual']='avaliacao/congelamento_adicional_v2.json'
old['snapshot_anterior']='avaliacao/snapshots/v8/agente.py'
old['experimentos_adicionais']={}
for label,name in [('antes','adicional_v1'),('depois_exploratorio','adicional_v2')]:
 path=Path('avaliacao/resultados')/name/'geracao.jsonl'
 old['experimentos_adicionais'][label]={'arquivo':path.as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
Path('docs/manifesto_atual_v9.json').write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf8')
