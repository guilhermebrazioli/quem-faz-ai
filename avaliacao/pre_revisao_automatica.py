"""Pré-revisão mecânica; não equivale a avaliação semântica nem humana."""
import argparse,csv,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--saida',default='avaliacao/resultados/cega_v2/pre_revisao_automatica.jsonl');args=p.parse_args()
out=Path(args.saida)
if out.exists():raise SystemExit('Saída já existe; use outro caminho.')
cases={x['id']:x for x in json.loads(Path('avaliacao/casos_cegos_v1.json').read_text(encoding='utf8'))}
base={x['id']:x for x in json.loads(Path('base/trechos.json').read_text(encoding='utf8'))}
rows=[json.loads(line) for line in Path('avaliacao/resultados/cega_v2/geracao.jsonl').read_text(encoding='utf8').splitlines()]
with out.open('x',encoding='utf8') as f:
 for x in rows:
  case=cases[x['id']];result=x['resultado'];ids=case['chunks_relevantes']; retrieved=x['evidencias_recuperadas'];
  record={'id':x['id'],'configuracao':x['configuracao'],'pergunta':case['pergunta'],'gabarito':case['esperado'],'ids_gabarito':ids,'fontes_gabarito':[{'id':i,'texto':base[i]['texto'],'url':base[i]['url']} for i in ids], 'top3':retrieved,'resposta':result,'erro':x['erro'],'metodo':'regras sobre status, IDs, correspondência literal com a base e rótulo do gabarito; não verifica relevância nem a verdade dos fatos','avaliacao_semantica':'não avaliada','alucinacao':'não avaliada'}
  if not result:
   record.update(recusa='não observável',adequacao_recusa_heuristica='não avaliada',citacoes='não avaliadas',justificativa='Não houve resposta para avaliar.')
  else:
   refusal=result.get('status')=='informacao_insuficiente';claims=result.get('orientacoes',[])+result.get('perguntas_sugeridas',[])
   if refusal:
    adequacy='consistente com rótulo não consta' if not ids else 'possível recusa indevida segundo gabarito'
    record.update(recusa='sim',adequacao_recusa_heuristica=adequacy,citacoes='não aplicável à recusa',justificativa='Comparação automática com rótulo; exige revisão do contexto e da suficiência.')
   else:
    valid=bool(claims) and all(c.get('fontes') and all(i in base for i in c['fontes']) for c in claims)
    exact=valid and all(any(c.get('texto')==base[i]['texto'] for i in c['fontes']) for c in claims)
    record.update(recusa='não',adequacao_recusa_heuristica='não aplicável',citacoes='IDs válidos e texto literal' if exact else ('IDs válidos; texto não literal' if valid else 'sem citação completa verificável'),justificativa='Checagem estrutural não demonstra suporte semântico nem correção da resposta.')
  f.write(json.dumps(record,ensure_ascii=False)+'\n')
print('Pré-revisão automática:',len(rows),'respostas; nenhum julgamento humano atribuído.')
