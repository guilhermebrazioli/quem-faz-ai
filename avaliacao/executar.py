import json, csv, time, argparse
from pathlib import Path
from src.core import search, generate_legacy as generate, Input, MODEL
P=Path('avaliacao/resultados/reexecucao_legada'); P.mkdir(parents=True, exist_ok=True)
cases=json.loads(Path('avaliacao/casos_teste.json').read_text(encoding='utf-8'))
def retrieval():
 rows=[]
 for case in cases:
  result=search(case['pergunta']); relevant=set(case['chunks_relevantes']); ids=[x['id'] for x in result]
  rows.append({'id':case['id'],'particao':case['particao'],'relevantes':','.join(sorted(relevant)),'top1':ids[0],'top3':','.join(ids),'score':round(result[0]['score'],4),'recall1':len(relevant.intersection(ids[:1]))/len(relevant) if relevant else '', 'recall3':len(relevant.intersection(ids))/len(relevant) if relevant else ''})
 with (P/'recuperacao.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 for split in ['calibracao','final']:
  relevant=[x for x in rows if x['particao']==split and x['relevantes']]
  print(split,'n=',len(relevant),'recall@1=',sum(x['recall1'] for x in relevant)/len(relevant),'recall@3=',sum(x['recall3'] for x in relevant)/len(relevant))
  subset=[x for x in rows if x['particao']==split]
  for t in [0.05,0.1,0.12,0.15,0.2,0.3]:
   tp=sum(bool(x['relevantes']) and x['score']>=t for x in subset); tn=sum(not x['relevantes'] and x['score']<t for x in subset)
   print('limiar',t,'aceitos',sum(x['score']>=t for x in subset),'acertos_binarios',tp+tn,'/',len(subset))
def generation():
 out=P/'geracao.jsonl'
 with out.open('w',encoding='utf-8') as f:
  for case in [x for x in cases if x['particao']=='final']:
   for config in 'ABC':
    start=time.perf_counter()
    try: result=generate(Input(descricao=case['pergunta'],configuracao=config)).model_dump(); error=None
    except Exception as e: result=None; error=f'{type(e).__name__}: {e}'
    row={'id':case['id'],'configuracao':config,'modelo':MODEL,'latencia_s':round(time.perf_counter()-start,3),'resultado':result,'erro':error,'correcao_humana':None,'fundamentacao_humana':None}
    f.write(json.dumps(row,ensure_ascii=False)+'\n'); f.flush(); print(case['id'],config,row['latencia_s'],error,flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--geracao',action='store_true');args=parser.parse_args();retrieval()
 if args.geracao:generation()
