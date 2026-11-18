# Auditoria e avaliação da correção v7

Este relatório complementa os históricos [inicial](relatorio_tecnico.md) e [v6](relatorio_continuacao.md). Não altera dados anteriores. O projeto continua como prova de conceito; integrantes e RMs não foram informados.

## Correção de codificação e reexecução posterior

Após a primeira execução da amostra nova, uma auditoria detectou caracteres acentuados corrompidos no prompt de confirmação. O código exato usado na primeira execução foi preservado em `avaliacao/snapshots/v7/agente.py`, e os resultados originais permanecem em `avaliacao/resultados/cega_v1/`. A codificação foi corrigida sem alterar a estratégia, e foi congelado novo manifesto `avaliacao/congelamento_cega_v2.json`. A execução foi repetida sobre as **mesmas** 20 perguntas, após observação da primeira rodada: a repetição não é uma segunda amostra cega independente. O código atual corresponde ao segundo manifesto.

A recuperação permaneceu igual: recall macro@1 0,7857 e recall macro@3 1,0000. Na repetição corrigida obtivemos:

| Configuração | JSON final válido | Respostas com IDs verificados | Recusas nos 6 não consta | Recusas nos 14 consta | Latência média s |
|---|---:|---:|---:|---:|---:|
| A | 20/20 | 0 | 1 | 2 | 1,539 |
| B | 20/20 | 7 | 6 | 7 | 0,464 |
| C | 20/20 | 7 | 6 | 7 | 0,439 |

Na primeira execução os números correspondentes de B e C foram nove respostas com IDs verificados e cinco recusas em casos consta. A correção de codificação foi motivada por auditoria do arquivo, mas ambas as rodadas devem ser lidas com essa limitação e com revisão humana pendente. A segunda execução está em `avaliacao/resultados/cega_v2/`; sua própria planilha de revisão continua vazia. Os notebooks `05_avaliacao_cega.ipynb` e `06_reexecucao.ipynb` documentam ambas as execuções.

## Diagnóstico

Foi executada novamente a versão v6 em seus oito casos rotulados como respondíveis, com registro dos prompts, contexto real, respostas brutas, scores, limiar, IDs, rastreio e classificações em [diagnóstico](../avaliacao/resultados/diagnostico_v6/diagnostico.md) e `reexecucao.jsonl`. As respostas brutas originais não haviam sido armazenadas, de modo que esta é uma reexecução, não reconstrução do histórico.

A LLM negou suficiência em cinco situações após ter selecionado evidência relevante. T16 e T23 também recebiam contexto incompleto; T21 teve o trecho esperado no primeiro lugar, mas abaixo do limiar. T21 requer qualificação: falha na pintura não demonstra, por si só, a existência de vício juridicamente caracterizado. T23 tem informações gerais de orçamento, não especificações técnicas de pintura. T18 foi respondido com CDC-01. A análise detalha cada caso e não presume que todo texto recuperado corresponda integralmente ao gabarito.

## Correções e limites

A versão atual continua copiando somente textos exatos dos trechos curados, com IDs existentes. Quando a verificação binária retorna falso, uma nova chamada solicita os IDs que apoiem ao menos parte da pergunta; somente IDs já selecionados e confirmados são aceitos. Uma resposta contém aviso de possível cobertura parcial. Não se exige concordância com IDs inventados; C inspeciona candidatos para padrões conhecidos de instrução suspeita antes de enviá-los ao modelo. A segunda checagem é feita pelo mesmo modelo e pode ter erros correlacionados: não comprova relevância nem neutraliza todas as injeções. A observação de uma fonte válida não comprova que ela responda à pergunta ou que cada fonte externa seja suficiente. A saída não melhora automaticamente a descrição nem gera perguntas.

A busca e o limiar de 0,15 foram mantidos desde v6. Ela usa TF-IDF com radicalização e um pequeno dicionário de equivalências cuja elaboração foi influenciada pelos antigos casos finais. Não foram adicionadas equivalências com base na amostra nova. Foram preservados os dez testes existentes e adicionados seis testes de regressão; os 16 passaram. Eles incluem falhas do servidor, JSON inválido, confirmação inválida e um padrão malicioso, sem afirmar proteção geral contra ataques.

## Comparação

O JSON válido abaixo é o **JSON final** depois de eventual recusa substitutiva; não é a taxa bruta da LLM. Fontes válidas significa IDs existentes e texto idêntico ao trecho interno, não fundamentação semântica. Correção e alucinação em todos os quadros permanecem pendentes de revisão humana. As recusas por rótulo não são avaliações humanas de correção. Latências incluem recusas sem chamada da LLM.

### Mesmo conjunto de desenvolvimento reutilizado: 14 casos por configuração

| Versão | Configuração | Recall macro@1 / @3 | JSON final | Respostas com fontes verificadas | Recusas em 6 não consta | Recusas em 8 consta | Latência média s |
|---|---|---|---:|---:|---:|---:|---:|
| Inicial | A | 0,5625 / 0,5625 | 14 | 0 | 0 | 1 | 1,715 |
| Inicial | B | 0,5625 / 0,5625 | 14 | 0 | 4 | 5 | 0,988 |
| Inicial | C | 0,5625 / 0,5625 | 14 | 0 | 6 | 8 | 1,025 |
| v6 | A | 0,8125 / 0,8125 | 14 | 0 | 0 | 2 | 1,574 |
| v6 | B | 0,8125 / 0,8125 | 14 | 1 | 6 | 7 | 0,335 |
| v6 | C | 0,8125 / 0,8125 | 14 | 1 | 6 | 7 | 0,322 |
| v7 com erro de codificação | A | 0,8125 / 0,8125 | 14 | 0 | 0 | 2 | 1,535 |
| v7 com erro de codificação | B | 0,8125 / 0,8125 | 14 | 4 | 6 | 4 | 0,479 |
| v7 com erro de codificação | C | 0,8125 / 0,8125 | 14 | 4 | 6 | 4 | 0,450 |
| v8 corrigida | A | 0,8125 / 0,8125 | 14 | 0 | 0 | 1 | 1,646 |
| v8 corrigida | B | 0,8125 / 0,8125 | 14 | 3 | 6 | 5 | 0,470 |
| v8 corrigida | C | 0,8125 / 0,8125 | 14 | 2 | 6 | 6 | 0,446 |

Recall é propriedade da busca disponível para B e C; A não consulta a busca, portanto os valores na tabela são apenas referência para a versão e não uma medição de recuperação de A. A resposta T17 passou a citar IPS-01; T28 da referência A continuou alucinando. As respostas completas dos cinco erros estão em [comparação v7](../avaliacao/comparacao_erros_v7.md) e [comparação v8](../avaliacao/comparacao_erros_v8.md).

### Amostra nova, congelada antes da execução

Foram escritos 20 casos novos, dos quais 14 têm trechos de referência e seis estão rotulados não consta. O código, base e casos foram congelados com SHA-256 antes da inferência (`avaliacao/congelamento_cega_v1.json`); nenhum ajuste posterior do algoritmo foi usado no resultado. As perguntas e o gabarito foram produzidos no mesmo projeto e não por avaliador independente: trata-se de conjunto novo, não de estudo duplo-cego ou validação independente de autoria e rotulagem.

Recall macro@1 = 0,7857; recall macro@3 = 1,0000, calculados sobre os 14 casos com gabarito, sem aplicar limiar; hit@1 e hit@3 são iguais nesses casos, pois cada um tem um único ID relevante. Cobertura pelo limiar 0,15: 11/20. Os resultados de recuperação são comuns a B e C; A não pesquisa a base.

| Configuração | Casos | JSON final válido | Respostas com fonte verificada | Recusas em 6 não consta | Recusas em 14 consta | Latência média s |
|---|---:|---:|---:|---:|---:|---:|
| A | 20 | 20 | 0 | 1 | 1 | 1,521 |
| B | 20 | 20 | 9 | 6 | 5 | 0,461 |
| C | 20 | 20 | 9 | 6 | 5 | 0,441 |

`avaliacao/resultados/cega_v1/` guarda respostas, scores, placar e planilha de revisão vazia. O agente não demonstrou benefício adicional no placar frente a B, embora acrescente uma checagem de integridade. Cinco recusas nos 14 casos rotulados como respondíveis indicam limitação de utilidade. Algumas respostas com fonte podem ser apenas parciais ou irrelevantes; aguardam revisão. A inferência não foi repetida após adaptação aos resultados da amostra nova.

## Revisão humana

`avaliacao/revisao_web.py` abre por padrão a planilha v6 solicitada; mostra pergunta, gabarito, configuração, resposta e evidências e salva somente após ação explícita, exigindo justificativa. Os campos permanecem vazios até a revisão. Pode-se apontar `REVISAO_CSV` para a planilha da amostra nova. Execute apenas em localhost. O consolidador calcula contagens e taxas sobre itens efetivamente avaliados, e sinaliza pendências; não interpreta vazio como erro, acerto ou ausência de alucinação.

Correção significa atender ao gabarito sem afirmações não sustentadas; uma resposta parcial deve ser classificada como tal. Fundamentação deve ser avaliada por pertinência e suporte de cada afirmação, não somente existência de ID. Alucinação é ao menos uma afirmação factual não sustentada ou contraditória. A revisão deve registrar justificativa e, idealmente, ser feita independentemente por uma pessoa que não tenha escrito os casos.

## Rubrica e auditoria para entrega

| Critério | Pontuação máxima | Implementação e evidência | Estado | Pendência |
|---|---:|---|---|---|
| Tarefa, gabarito, não consta | 0,5 | `avaliacao/casos_teste.json`, `avaliacao/casos_cegos_v1.json` | Parcial | Revisão humana dos gabaritos e ambiguidades |
| Base segmentada com fontes | 1,0 | `base/trechos.json` | Concluído | Ampliar escopo quando necessário |
| Busca, recall e limiar | 1,0 | `avaliacao/resultados/cega_v1/recuperacao.csv`; calibração v6 | Concluído | Amostra maior e anotação independente para robustez |
| JSON, fontes, recusa e fundamentação | 2,0 | `src/agente.py`; saídas da amostra nova | Parcial | Revisão semântica, reduzir falsas recusas e medir segurança |
| Agente comparado a RAG | 2,0 | `src/agente.py`; placar da amostra nova | Parcial | Evidenciar eventual benefício do agente; não foi observado |
| Comparativo das três configurações | 2,0 | `avaliacao/resultados/cega_v1/placar.csv` | Parcial | Completar correção, alucinação e fundamentação por revisão humana |
| Cinco erros reais | 1,0 | `avaliacao/comparacao_erros_v7.md` | Concluído | Algumas falhas persistem e estão registradas |
| README e reprodutibilidade | 0,5 | `README.md`; seis notebooks executados | Parcial | Execução por avaliador independente; identificar integrantes |

Não há integração real com o MVP: somente consumidor de demonstração e testes de API local. Não atribuímos nota oficial. A revisão humana, as recusas indevidas, os limites de robustez de injeção e a ausência de avaliador independente impedem tratar a entrega acadêmica como finalizada.
