import argparse,csv,hashlib,json,time
from pathlib import Path
from src.core import BASE,Input,MODEL,Response,generate
from src.retrieval import rank
parser=argparse.ArgumentParser();parser.add_argument('--destino',default='avaliacao/resultados/cega_v1');parser.add_argument('--manifesto',default='avaliacao/congelamento_cega_v3.json');args=parser.parse_args();out=Path(args.destino)
manifest=json.loads(Path(args.manifesto).read_text(encoding='utf8'))
for path,digest in manifest.items():
 if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=digest:raise SystemExit('Código, base ou casos diferem do congelamento: '+path)
out.mkdir(parents=True,exist_ok=True)
if (out/'geracao.jsonl').exists():raise SystemExit('Arquivo existente; informe outro destino.')
cases=json.loads(Path('avaliacao/casos_cegos_v1.json').read_text(encoding='utf8')); retrieved=[]
with (out/'geracao.jsonl').open('w',encoding='utf8') as f:
 for c in cases:
  candidates=rank(c['pergunta'],BASE);ids=[x['id'] for x in candidates]; rel=set(c['chunks_relevantes'])
  retrieved.append({'id':c['id'],'relevantes':','.join(sorted(rel)),'top1':ids[0],'top3':','.join(ids),'score':candidates[0]['score'],'recall1':len(rel.intersection(ids[:1]))/len(rel) if rel else '', 'recall3':len(rel.intersection(ids))/len(rel) if rel else '', 'hit1':int(bool(rel.intersection(ids[:1]))) if rel else '', 'hit3':int(bool(rel.intersection(ids))) if rel else ''})
  for config in 'ABC':
   start=time.perf_counter()
   try:result=generate(Input(descricao=c['pergunta'],configuracao=config)).model_dump();error=None
   except Exception as e:result=None;error=f'{type(e).__name__}: {e}'
   row={'id':c['id'],'configuracao':config,'modelo':MODEL,'latencia_s':round(time.perf_counter()-start,3),'resultado':result,'erro':error,'evidencias_recuperadas':[{'id':x['id'],'texto':x['texto'],'score':x['score']} for x in candidates]}
   f.write(json.dumps(row,ensure_ascii=False)+'\n');f.flush();print(c['id'],config,row['latencia_s'],error,flush=True)
with (out/'recuperacao.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=retrieved[0]);w.writeheader();w.writerows(retrieved)
