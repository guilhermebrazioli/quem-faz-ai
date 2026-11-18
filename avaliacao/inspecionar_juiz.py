import json
from pathlib import Path
responses={(x['id'],x['configuracao']):x for x in (json.loads(t) for t in Path('avaliacao/resultados/cega_v2/geracao.jsonl').read_text(encoding='utf8').splitlines())}
judge=[json.loads(t) for t in Path('avaliacao/resultados/cega_v2/pre_revisao_modelo.jsonl').read_text(encoding='utf8').splitlines()]
for conf in 'ABC':
 s=[x for x in judge if x['configuracao']==conf and x['julgamento'] and responses[(x['id'],conf)]['resultado']['status']=='informacao_insuficiente']
 print(conf,'recusas com juiz válido',len(s),'juiz diz nao_aplicavel',sum(x['julgamento']['adequacao_recusa']=='nao_aplicavel' for x in s))
