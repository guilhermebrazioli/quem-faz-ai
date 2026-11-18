import csv,json,statistics
from pathlib import Path
from src.core import Response
P=Path('avaliacao/resultados/reexecucao_legada')
rows=[json.loads(x) for x in (P/'geracao.jsonl').read_text(encoding='utf-8').splitlines()]
cases={x['id']:x for x in json.loads(Path('avaliacao/casos_teste.json').read_text(encoding='utf-8'))}
summary=[]
for conf in 'ABC':
 subset=[x for x in rows if x['configuracao']==conf]; valid=sum(bool(x['resultado']) and bool(Response.model_validate(x['resultado'])) for x in subset)
 generated=[x for x in subset if x['resultado'] and 'gera_json_llm' in x['resultado']['rastreio']]
 unknown=[x for x in subset if cases[x['id']]['disponibilidade']=='não consta']
 r={'configuracao':conf,'casos':len(subset),'json_resposta_valido':valid,'chamadas_llm':len(generated),'falha_parse_ou_esquema_llm':sum('json_invalido' in x['resultado']['rastreio'] for x in generated),'recusas':sum(x['resultado']['status']=='informacao_insuficiente' for x in subset),'recusas_nao_consta':sum(x['resultado']['status']=='informacao_insuficiente' for x in unknown),'total_nao_consta':len(unknown),'respostas_com_fonte':sum(bool(x['resultado']['fontes']) for x in subset),'latencia_media_s':round(statistics.mean(x['latencia_s'] for x in subset),3)}
 summary.append(r)
with (P/'comparativo.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=summary[0]);w.writeheader();w.writerows(summary)
print(summary)
