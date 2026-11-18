import json
from pathlib import Path
old=[json.loads(x) for x in Path('avaliacao/resultados/geracao.jsonl').read_text(encoding='utf8').splitlines()]
new=[json.loads(x) for x in Path('avaliacao/resultados/v5/geracao.jsonl').read_text(encoding='utf8').splitlines()]
cases={c['id']:c for c in json.loads(Path('avaliacao/casos_teste.json').read_text(encoding='utf8'))}
notes={
('T16','A'): 'A resposta anterior deu prazo de 30 dias. Na nova execução ela não repetiu esse número, mas não respondeu prazo nem negociação. A falha exata não se reproduziu; a resposta segue incompleta. A não usa base por definição e não sofreu correção específica.',
('T17','C'): 'A recusa indevida foi reproduzida: a recuperação ainda não encontrou trechos acima do limiar. A normalização morfológica não aproximou esquentando de quente. A questão exige melhoria e nova avaliação.',
('T18','C'): 'A recusa não se reproduziu: agora CDC-01 foi selecionado, verificado e apresentado com fonte. Isso demonstra o comportamento neste caso, não uma taxa geral de correção.',
('T28','A'): 'Reproduziu a afirmação falsa de que a Arábia Saudita venceu a Copa. A permanece propositalmente uma referência sem contexto e sem filtro de domínio; o risco não foi corrigido nesta configuração.',
('T29','B'): 'A resposta sem citações não se repetiu: houve recusa por ausência de evidência acima do limiar. O sistema continua sujeito a classificações incorretas de suficiência em outros casos.'}
out=['# Reexecução dos cinco erros','', 'Os registros históricos foram preservados em `avaliacao/resultados/geracao.jsonl`; a nova execução está em `avaliacao/resultados/v5/geracao.jsonl`. A reprodução é empírica e não implica determinismo absoluto.','']
for key,note in notes.items():
 a=next(x for x in old if (x['id'],x['configuracao'])==key); b=next(x for x in new if (x['id'],x['configuracao'])==key);case=cases[key[0]]
 out += [f'## {key[0]} — configuração {key[1]}',f"**Pergunta:** {case['pergunta']}",f"**Gabarito:** {case['esperado']}",f'**Análise:** {note}','', '**Resposta anterior:**','```json',json.dumps(a['resultado'],ensure_ascii=False,indent=2),'```','', '**Resposta posterior:**','```json',json.dumps(b['resultado'],ensure_ascii=False,indent=2),'```','']
Path('avaliacao/comparacao_erros_v5.md').write_text('\n'.join(out),encoding='utf8')
