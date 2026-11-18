import argparse, csv, json, time
from pathlib import Path
from src.core import generate, Input, MODEL, BASE
from src.retrieval import rank
parser=argparse.ArgumentParser(); parser.add_argument('--destino', default='avaliacao/resultados/reexecucao_v5'); args=parser.parse_args()
P=Path(args.destino); P.mkdir(parents=True, exist_ok=True)
if (P/'geracao.jsonl').exists(): raise SystemExit('Destino j? cont?m geracao.jsonl; escolha outro --destino para preservar resultados.')
cases=json.loads(Path('avaliacao/casos_teste.json').read_text(encoding='utf-8'))
with (P/'geracao.jsonl').open('w',encoding='utf-8') as f:
 for case in [x for x in cases if x['particao']=='final']:
  for config in 'ABC':
   start=time.perf_counter()
   try: result=generate(Input(descricao=case['pergunta'],configuracao=config)).model_dump(); error=None
   except Exception as exc: result=None; error=f'{type(exc).__name__}: {exc}'
   row={'id':case['id'],'pergunta':case['pergunta'],'configuracao':config,'modelo':MODEL,'latencia_s':round(time.perf_counter()-start,3),'resultado':result,'erro':error,'evidencias_recuperadas':[{'id':x['id'],'score':x['score'],'texto':x['texto']} for x in rank(case['pergunta'],BASE)],'correcao_humana':None,'fundamentacao_humana':None,'alucinacao_humana':None}
   f.write(json.dumps(row,ensure_ascii=False)+'\n');f.flush();print(case['id'],config,row['latencia_s'], error,flush=True)
