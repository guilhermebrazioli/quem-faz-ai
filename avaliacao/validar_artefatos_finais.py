import json,nbformat
from pathlib import Path
from src.core import Response
files=list(Path('notebooks').glob('*.ipynb'))
for p in files:
 nb=nbformat.read(p,as_version=4);nbformat.validate(nb);print(p.name,'válido',sum(c.cell_type=='code' and c.execution_count is not None for c in nb.cells),'células executadas')
paths=[Path('base/trechos.json'),Path('avaliacao/casos_teste.json'),Path('avaliacao/casos_cegos_v1.json'),Path('avaliacao/casos_internos_adicionais.json'),Path('docs/manifesto_experimentos.json')]
for p in paths:json.loads(p.read_text(encoding='utf-8-sig'))
for p in [Path('avaliacao/resultados/cega_v2/geracao.jsonl'),Path('avaliacao/resultados/adicional_v1/geracao.jsonl'),Path('avaliacao/resultados/adicional_v2/geracao.jsonl'),Path('avaliacao/resultados/cega_v2/pre_revisao_automatica.jsonl')]:
 lines=[json.loads(x) for x in p.read_text(encoding='utf8').splitlines()];print(p,len(lines),'JSONL válido')
 if p.name=='geracao.jsonl':
  for row in lines:
   if row.get('erro') or not row.get('resultado'):raise ValueError(f'Erro na execução {p} {row.get("id")}')
   Response.model_validate(row['resultado'])
