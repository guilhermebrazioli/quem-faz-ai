import json
from pathlib import Path
cases=json.loads(Path('avaliacao/casos_teste.json').read_text(encoding='utf8'))
old=[json.loads(x) for x in Path('avaliacao/resultados/geracao.jsonl').read_text(encoding='utf8').splitlines()]
v6=[json.loads(x) for x in Path('avaliacao/resultados/v6/execucao_final/geracao.jsonl').read_text(encoding='utf8').splitlines()]
v7=[json.loads(x) for x in Path('avaliacao/resultados/v8_dev/geracao.jsonl').read_text(encoding='utf8').splitlines()]
notes={('T16','A'):'A referência sem contexto continua incompleta. Não se repetiu exatamente a afirmação de 30 dias.',('T17','C'):'Agora seleciona e exibe IPS-01; informação apoiada na base, mas revisão humana da resposta segue pendente.',('T18','C'):'CDC-01 segue selecionado com fonte válida.',('T28','A'):'A referência sem contexto repete a alegação falsa; essa configuração não recebeu filtro de domínio.',('T29','B'):'A resposta sem citação foi substituída por recusa por ausência de evidência acima do limiar.'}
out=['# Evolução dos cinco erros reais','','A comparação é sobre os mesmos casos já usados para desenvolver o sistema. Não é teste independente.','']
for (id,cfg),note in notes.items():
 c=next(x for x in cases if x['id']==id);out += [f'## {id} — {cfg}',f"Pergunta: {c['pergunta']}",f"Gabarito: {c['esperado']}",f'Análise: {note}']
 for label,rows in [('Original',old),('v6',v6),('v8',v7)]:
  x=next(x for x in rows if x['id']==id and x['configuracao']==cfg)
  out += [f'### {label}','```json',json.dumps(x['resultado'],ensure_ascii=False,indent=2),'```']
 out.append('')
Path('avaliacao/comparacao_erros_v8.md').write_text('\n'.join(out),encoding='utf8')
