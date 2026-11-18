import json
from pathlib import Path
rows=[json.loads(x) for x in Path('avaliacao/resultados/diagnostico_v6/reexecucao.jsonl').read_text(encoding='utf8').splitlines()]
analysis={
'T16':('Contexto insuficiente; falha de recuperação para CDC-02; falha de verificação semântica para a parte recuperada.','CDC-03 apareceu acima do limiar; CDC-02 não entrou no top 3. A base cobre validade e alteração, mas o contexto fornecido cobre só alteração.'),
'T17':('Recusa indevida do modelo; verificação semântica.','IPS-01 foi recuperado e orienta procurar profissional; MME-01 não entrou no top 3. É possível responder ao menos parcialmente.'),
'T18':('Sem falha observada nesta reexecução.','CDC-01 responde à pergunta e foi citado.'),
'T19':('Verificação semântica e seleção com contexto parcialmente irrelevante.','MME-01 responde à pergunta; seleção incluiu também CDC-01, que não é necessário para o quesito.'),
'T20':('Recusa indevida do modelo; verificação semântica.','MME-02 aborda cabos e extensões e foi selecionado, mas a decisão binária negou suficiência.'),
'T21':('Falha de recuperação pelo limiar; gabarito depende de enquadramento.','PROCON-01 foi o primeiro, com score abaixo de 0,15. Um defeito de pintura pode configurar vício, mas falha não comprova automaticamente o enquadramento jurídico.'),
'T22':('Recusa indevida do modelo; verificação semântica.','CDC-03 cobre alteração por negociação; o verificador negou suficiência.'),
'T23':('Contexto insuficiente; falha de recuperação para CDC-01.','CDC-02 foi aceito; CDC-01 não entrou no top 3. A base cobre itens gerais e validade, não especificações técnicas de pintura.')}
out=['# Diagnóstico da reexecução v6','', 'A geração original não guardou resposta bruta nem contexto completo. Este diagnóstico é uma nova execução instrumentada da implementação v6 preservada, não uma reconstrução de dados que não foram gravados. Conteúdo e respostas brutas completos em `reexecucao.jsonl`. Pontuações, seleção e verificação se referem a essa reexecução.','']
for x in rows:
 kind,note=analysis[x['id']];out += [f"## {x['id']}",f"**Pergunta:** {x['pergunta']}",f"**Gabarito:** {x['gabarito']} — {', '.join(x['ids_gabarito'])}",f"**Recuperados:** "+'; '.join(f"{r['id']} ({r['score']:.4f}): {r['texto']}" for r in x['recuperacao']),f"**Limiar:** {x['limiar']}; aceitos: {', '.join(x['aceitos']) or 'nenhum'}.",f"**Classificação:** {kind}",f"**Análise:** {note}"]
 if not x['chamadas']:out+=['**Contexto e resposta da LLM:** não houve chamada após o limiar.']
 for call in x['chamadas']:out += [f"**Chamada {call['schema']}:** validação {call['validacao']}", '```text',call['contexto_exato'],'```','Resposta bruta: `'+call['resposta_bruta']+'`']
 out += [f"**Validação e motivo final:** {'; '.join(x['resultado']['rastreio'])}",'']
Path('avaliacao/resultados/diagnostico_v6/diagnostico.md').write_text('\n'.join(out),encoding='utf8')
