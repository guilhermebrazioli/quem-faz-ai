import json
from collections import Counter
from pathlib import Path
p=Path('avaliacao/resultados/cega_v2/pre_revisao_modelo.jsonl');rows=[json.loads(x) for x in p.read_text(encoding='utf8').splitlines()]
summary={}
for config in 'ABC':
 sub=[x for x in rows if x['configuracao']==config];valid=[x['julgamento'] for x in sub if x['julgamento']];entry={'total':len(sub),'validos':len(valid),'falhas':len(sub)-len(valid)}
 for field in ['correcao','sustentacao','alucinacao','adequacao_recusa']:entry[field]=dict(Counter(x[field] for x in valid))
 summary[config]=entry
out=Path('avaliacao/resultados/cega_v2/resumo_pre_revisao_modelo.json')
if out.exists():raise SystemExit('Arquivo existente')
out.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False,indent=2))
