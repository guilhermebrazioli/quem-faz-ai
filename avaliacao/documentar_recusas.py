import json
from pathlib import Path
cases={x['id']:x for x in json.loads(Path('avaliacao/casos_cegos_v1.json').read_text(encoding='utf8'))}
base={x['id']:x for x in json.loads(Path('base/trechos.json').read_text(encoding='utf8'))}
rows=[json.loads(x) for x in Path('avaliacao/resultados/cega_v2/geracao.jsonl').read_text(encoding='utf8').splitlines()]
notes={
'B03':'O trecho sobre mudança de orçamento está no top 3, mas abaixo do limiar; a formulação pressupõe orçamento aprovado, condição explícita no trecho.',
'B04':'CDC-04 está no top 3, mas abaixo do limiar. A fonte cobre acréscimos de terceiros não previstos, sujeitos ao contexto da relação de consumo.',
'B05':'MME-01 foi enviado e selecionado; o avaliador binário negou suficiência e a confirmação parcial não forneceu ID aceito. O trecho recomenda profissional qualificado.',
'B06':'MME-02 foi enviado e selecionado; a confirmação parcial não forneceu ID aceito. Cabo com isolamento rompido é interpretado como cabo desencapado, hipótese sujeita à revisão humana.',
'B07':'MME-03 está no top 3, mas abaixo do limiar. Apenas CDC-01 foi aceito e selecionado; não há evidência de que MME-03 tenha sido enviado ao modelo.',
'B11':'PROCON-03 foi o primeiro resultado, mas ficou abaixo do limiar. A fonte cobre cobrança informada antecipadamente; proposta é interpretada como orçamento.',
'B14':'IPS-03 foi o primeiro resultado, mas ficou abaixo do limiar. O trecho se refere a disjuntor mais forte; amperagem maior é interpretação técnica que deve ser revisada.'}
out=['# Sete recusas da avaliação reutilizada — agente C','', 'Registro observacional: top 3, scores e rastreio vêm de `cega_v2/geracao.jsonl`; o experimento não guardou respostas brutas nem prompts exatos. O conjunto foi usado em duas rodadas e não é avaliação cega independente. Não foi feita nova chamada ao modelo. As verificações de adequação do gabarito são preliminares, pendentes de avaliação humana.','']
for x in rows:
 if x['configuracao']!='C' or x['id'] not in notes:continue
 case=cases[x['id']];r=x['resultado'];top=x['evidencias_recuperadas'];accepted=[a for a in top if a['score']>=.15];tr=r['rastreio'];selected=[a for a in tr if a.startswith('valida_ids:ok:')]
 out += [f"## {x['id']}",f"**Pergunta:** {case['pergunta']}",f"**Gabarito:** {case['esperado']}", '**Fontes esperadas:** '+ '; '.join(f"{id}: {base[id]['texto']}" for id in case['chunks_relevantes']), '**Top 3:** '+ '; '.join(f"{a['id']} = {a['score']:.4f}" for a in top), '**Contexto inferível pelo código e limiar:** '+('; '.join(f"{a['id']}: {a['texto']}" for a in accepted) if accepted else 'nenhum trecho; nenhuma chamada à LLM.'), '**Seleção registrada:** '+('; '.join(selected) if selected else 'não houve seleção registrada.'), '**Bloqueio e causa provável:** '+notes[x['id']], '**Validação de citações:** '+('IDs selecionados passaram na checagem estrutural; nenhuma resposta foi liberada.' if selected else 'não foi realizada, pois não houve seleção.'), '**Resposta bloqueada:** conteúdo bruto não registrado; não é possível verificar se uma resposta completa e válida foi rejeitada.', '**Rastreio:** `'+ ' → '.join(tr)+'`','']
Path('avaliacao/investigacao_sete_recusas.md').write_text('\n'.join(out),encoding='utf8')
