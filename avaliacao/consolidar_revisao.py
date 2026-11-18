import argparse,csv,json
from collections import Counter,defaultdict
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('arquivo');parser.add_argument('--saida',required=True);parser.add_argument('--mapa');args=parser.parse_args()
with Path(args.arquivo).open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
if args.mapa:
 mapping=json.loads(Path(args.mapa).read_text(encoding='utf8'))
 for row in rows:
  if row['id'] not in mapping: raise SystemExit('ID ausente do mapa: '+row['id'])
  row['configuracao']=mapping[row['id']]['configuracao']
res={}
for config in sorted({x['configuracao'] for x in rows}):
 subset=[x for x in rows if x['configuracao']==config];entry={'total':len(subset)}
 for field in ['correcao_humana','fundamentacao_humana','alucinacao_humana','adequacao_recusa']:
  c=Counter(x.get(field,'') for x in subset if x.get(field,''));entry[field]={'avaliados':sum(c.values()),'pendentes':len(subset)-sum(c.values()),'contagens':dict(c)}
  if not c:entry[field]['resultado']='pendente'
  else:
   entry[field]['taxas_sobre_registrados']={k:round(v/sum(c.values()),4) for k,v in c.items()}
   valid={k:v for k,v in c.items() if k not in ('nao_avaliavel','nao_aplicavel')}
   entry[field]['casos_avaliaveis']=sum(valid.values())
   entry[field]['taxas_sobre_avaliaveis']={k:round(v/sum(valid.values()),4) for k,v in valid.items()} if valid else {}
 res[config]=entry
out=Path(args.saida)
if out.exists():raise SystemExit('Saída já existe; selecione outro arquivo para preservar resultados.')
out.write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(res,ensure_ascii=False,indent=2))
