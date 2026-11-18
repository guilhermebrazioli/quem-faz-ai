import csv,json,statistics
from pathlib import Path
from src.core import BASE,Response
p=Path('avaliacao/resultados/v3'); cases={x['id']:x for x in json.loads(Path('avaliacao/casos_teste.json').read_text(encoding='utf-8'))}; rows=[json.loads(x) for x in (p/'geracao.jsonl').read_text(encoding='utf-8').splitlines()]; base={x['id']:x for x in BASE}; summary=[]; reviews=[]
for config in 'ABC':
 rs=[x for x in rows if x['configuracao']==config]; valid=0; refusal=0; correct_ref=0; wrong_ref=0; sourced=0; supported=0; fail=0
 for x in rs:
  result=x['resultado']; case=cases[x['id']]
  if result:
   try:Response.model_validate(result);valid+=1
   except Exception:pass
   isref=result['status']=='informacao_insuficiente';refusal+=isref
   correct_ref+=isref and case['disponibilidade']=='não consta';wrong_ref+=isref and case['disponibilidade']=='consta'
   if not isref and config!='A':
    claims=result['orientacoes']+result['perguntas_sugeridas']; cited=bool(claims) and all(c['fontes'] and all(i in base for i in c['fontes']) for c in claims)
    exact=cited and all(any(c['texto']==base[i]['texto'] for i in c['fontes']) for c in claims)
    sourced+=cited;supported+=exact
  else:fail+=1
  reviews.append({'id':x['id'],'configuracao':config,'pergunta':case['pergunta'],'gabarito':case['esperado'],'disponibilidade':case['disponibilidade'],'ids_relevantes':','.join(case['chunks_relevantes']),'resposta':json.dumps(result,ensure_ascii=False),'evidencias_recuperadas':json.dumps(x['evidencias_recuperadas'],ensure_ascii=False),'criterio':'Correta se satisfaz o gabarito sem informação não sustentada; alucinação se afirma fato não sustentado ou contraditório; recusa indevida se há resposta disponível. Avaliar relevância e suporte por afirmação.', 'correcao_humana':'','fundamentacao_humana':'','alucinacao_humana':'','observacoes_revisor':''})
 summary.append({'configuracao':config,'total':len(rs),'corretas_humano':'pendente','incorretas_humano':'pendente','recusas':refusal,'recusas_rotulo_nao_consta':correct_ref,'recusas_rotulo_consta':wrong_ref,'json_valido':valid,'respostas_fontes_ids_validos':sourced if config!='A' else 'na','afirmacoes_texto_exato':supported if config!='A' else 'na','fundamentacao_semantica_humano':'pendente','alucinacoes_humano':'pendente','falhas':fail,'latencia_media_s':round(statistics.mean(x['latencia_s'] for x in rs),3)})
for name,table in [('placar.csv',summary),('revisao_humana.csv',reviews)]:
 with (p/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=table[0]);w.writeheader();w.writerows(table)
print(summary)
