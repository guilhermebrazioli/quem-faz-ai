import json,csv
from pathlib import Path
import argparse
from src.core import BASE, search as old
from src.retrieval import rank
cases=json.loads(Path('avaliacao/casos_teste.json').read_text(encoding='utf-8'))
parser=argparse.ArgumentParser();parser.add_argument('--destino',default='avaliacao/resultados/recalculo_busca');args=parser.parse_args()
out=Path(args.destino);out.mkdir(parents=True,exist_ok=True)
if (out/'recuperacao_metodos.csv').exists():raise SystemExit('Resultado existente; escolha outro destino.')
rows=[]
for method in ['tfidf_original','tfidf_stem','bm25_stem']:
 for c in cases:
  r=old(c['pergunta']) if method=='tfidf_original' else rank(c['pergunta'],BASE,'bm25' if method=='bm25_stem' else 'tfidf')
  rel=set(c['chunks_relevantes']); ids=[x['id'] for x in r]
  rows.append(dict(metodo=method,id=c['id'],particao=c['particao'],relevantes=','.join(sorted(rel)),top1=ids[0],top3=','.join(ids),score=r[0]['score'],recall1=len(rel.intersection(ids[:1]))/len(rel) if rel else '',recall3=len(rel.intersection(ids))/len(rel) if rel else '',hit1=int(bool(rel.intersection(ids[:1]))) if rel else '',hit3=int(bool(rel.intersection(ids))) if rel else ''))
with (out/'recuperacao_metodos.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
for method in ['tfidf_original','tfidf_stem','bm25_stem']:
 for part in ['calibracao','final']:
  sub=[x for x in rows if x['metodo']==method and x['particao']==part and x['relevantes']]
  print(method,part, 'recall1',sum(x['recall1'] for x in sub)/len(sub),'recall3',sum(x['recall3'] for x in sub)/len(sub),'hit1',sum(x['hit1'] for x in sub)/len(sub),'hit3',sum(x['hit3'] for x in sub)/len(sub))
