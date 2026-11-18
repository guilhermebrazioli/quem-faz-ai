import csv
from pathlib import Path
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--entrada',default='avaliacao/resultados/v6/recuperacao_metodos.csv');parser.add_argument('--saida',default='avaliacao/resultados/recalculo_busca/calibracao.csv');args=parser.parse_args()
destination=Path(args.saida);destination.parent.mkdir(parents=True,exist_ok=True)
if destination.exists():raise SystemExit('Resultado existente; escolha outra saída.')
rows=list(csv.DictReader(Path(args.entrada).open(encoding='utf8'))); records=[]
for method,ts in [('tfidf_original',[.01,.05,.1,.12,.15,.2]),('tfidf_stem',[.01,.03,.05,.08,.1,.15,.2]),('bm25_stem',[.05,.1,.2,.3,.5,1,2])]:
 for split in ['calibracao','final']:
  subset=[x for x in rows if x['metodo']==method and x['particao']==split]; rel=[x for x in subset if x['relevantes']]
  for t in ts:
   records.append({'metodo':method,'particao':split,'limiar':t,'total':len(subset),'corretos_binarios':sum((float(x['score'])>=t)==bool(x['relevantes']) for x in subset),'cobertura':sum(float(x['score'])>=t for x in subset),'recall1_macro':sum(float(x['recall1']) for x in rel)/len(rel),'recall3_macro':sum(float(x['recall3']) for x in rel)/len(rel),'hit1':sum(int(x['hit1']) for x in rel)/len(rel),'hit3':sum(int(x['hit3']) for x in rel)/len(rel)})
with destination.open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=records[0]);w.writeheader();w.writerows(records)
print([x for x in records if x['metodo']=='tfidf_stem' and x['limiar']==.15])
