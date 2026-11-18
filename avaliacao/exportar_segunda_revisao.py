"""Exportação local para segundo avaliador. Não atribui julgamentos humanos."""
import argparse,csv,json,secrets
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('entrada');p.add_argument('--saida',required=True);p.add_argument('--mapa',required=True);args=p.parse_args()
out=Path(args.saida);mapping_path=Path(args.mapa)
if out.exists() or mapping_path.exists():raise SystemExit('Saída ou mapa já existem; escolha outros nomes.')
with Path(args.entrada).open(encoding='utf-8-sig',newline='') as f:
 reader=csv.DictReader(f);rows=list(reader);fields=reader.fieldnames
if not rows:raise SystemExit('Sem respostas para revisão.')
fields=list(fields)
if 'adequacao_recusa' not in fields:fields.append('adequacao_recusa')
mapping={}
for row in rows:
 anon=secrets.token_hex(8)
 mapping[anon]={'id_original':row['id'],'configuracao':row['configuracao']}
 row['id']=anon;row['configuracao']='oculta'
 try:
  answer=json.loads(row['resposta'])
  if isinstance(answer,dict):
   answer.pop('rastreio',None)
   if answer.get('status') in ('sem_contexto','fundamentado'):answer['status']='resposta'
  row['resposta']=json.dumps(answer,ensure_ascii=False)
 except (ValueError,TypeError):pass
 for name in ['correcao_humana','fundamentacao_humana','alucinacao_humana','adequacao_recusa','observacoes_revisor']:
  row[name]=''
secrets.SystemRandom().shuffle(rows)
out.parent.mkdir(parents=True,exist_ok=True);mapping_path.parent.mkdir(parents=True,exist_ok=True)
with out.open('x',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
with mapping_path.open('x',encoding='utf8') as f:json.dump(mapping,f,ensure_ascii=False,indent=2)
print(f'{len(rows)} registros exportados. Guarde o mapa separado da cópia de revisão.')
