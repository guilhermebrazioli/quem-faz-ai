# Continuação: auditoria e resultados da versão atual

Este documento complementa o [relatório histórico](relatorio_tecnico.md), preservado para registrar a primeira execução. Dados anteriores estão em `avaliacao/resultados/geracao.jsonl`; tentativas intermediárias em `v2` a `v5`; o experimento aqui descrito está em `avaliacao/resultados/v6`. Não houve ajuste dos pesos do modelo. Integrantes e RMs continuam não informados.

## Auditoria e correções

Na primeira versão, B só checava IDs para C, mas atribuía `fundamentado` também a B. O modelo frequentemente omitia as fontes e o agente rejeitava toda a resposta se qualquer item não as tivesse. A recuperação não normalizava flexões. No experimento posterior verificou-se ainda que o modelo rejeitava um trecho correto quando o verificador recebia os dados em forma de objeto JSON; texto simples produziu resultado diferente nesse caso. O registro bruto da saída da LLM anterior era descartado, portanto não se pode distinguir parsing de erro de esquema naquela execução.

A e o mesmo Qwen local continuam como referência. Em B, a LLM seleciona IDs de trechos recuperados, verifica se eles respondem à pergunta e o programa copia literalmente o texto do trecho armazenado na base, verificando seus IDs. Em C, a orquestração acrescenta verificações de integridade, URL HTTPS e detecção limitada de instruções suspeitas; todas as etapas constam no rastreio. A checagem semântica de pertinência é uma opinião da mesma LLM, não prova de entailment, e pode produzir falsos positivos e falsos negativos. O texto emitido é uma paráfrase curada da fonte pública, reproduzida exatamente da base do projeto; não é citação literal do órgão. Os filtros de injeção são heurísticos e não garantem resistência a ataques. A saída não reformula o pedido nem produz perguntas no momento: preserva a descrição recebida e deixa perguntas vazias. Não há seleção automática de prestadores.

## Busca e desenho experimental

Foram comparados TF-IDF anterior, TF-IDF com radicalização em português e equivalências lexicais, e BM25 com a mesma normalização; detalhes por caso em `avaliacao/resultados/v6/recuperacao_metodos.csv`. Embeddings não foram executados: envolveriam outro download e outra dependência; são uma alternativa futura, sem afirmar desempenho. Na calibração, TF-IDF normalizado e BM25 empataram em recall@1 e recall@3 (0,8667 e 1,0000); optou-se por TF-IDF. Limiar 0,15 escolhido no conjunto de calibração, com 17/18 acertos binários entre os limiares testados. A classificação de suficiência não é garantida pelo escore. Registro: `avaliacao/resultados/v6/calibracao.csv`.

**Vazamento de avaliação:** o conjunto final da primeira execução foi inspecionado e motivou o dicionário de equivalências (inclusive esquentar/quente, falhar/vício e validade/vale), e diferentes versões também foram experimentadas no mesmo conjunto. Por isso, a partição final foi reutilizada e os resultados abaixo são exploratórios, não são estimativas cegas independentes. É necessário criar um conjunto novo, não usado no desenvolvimento, para conclusão confiável. A calibração e a final têm perguntas formuladas pelo mesmo projeto, com base pequena e correlacionada.

Recall macro@k = média por pergunta com gabarito da razão entre chunks relevantes no top k e todos os chunks relevantes daquela pergunta. Hit@k = proporção dessas perguntas com pelo menos um chunk relevante no top k. Ambas ignoram limiar e excluem casos sem gabarito. No resultado histórico, os oito casos contribuíram 0,5 + 0 + 1 + 1 + 1 + 0 + 1 + 0 = 4,5; dividido por 8 = **0,5625** para ambos os k. Hit@1 e hit@3 antigos eram 5/8 = 0,625. Empates em score zero foram ordenados por ID; não equivalem a evidência recuperada para fins de geração.

| Recuperação, partição final reutilizada | Recall macro@1 | Recall macro@3 | Hit@1 | Hit@3 |
|---|---:|---:|---:|---:|
| Anterior | 0,5625 | 0,5625 | 0,625 | 0,625 |
| Atual, com equivalências informadas pelos erros | 0,8125 | 0,8125 | 1,000 | 1,000 |

O recall macro@3 atual é 6,5/8: três perguntas têm dois IDs relevantes; retornar apenas um desses IDs conta como 0,5, mesmo que hit@3 seja 1. Para geração, apenas candidatos com score pelo menos 0,15 são aceitos; cobertura final foi 8/14 e o acerto binário do limiar foi 12/14. Isso não prova que as respostas geradas estejam corretas.

## Geração e revisão

Os mesmos 14 casos foram usados nas três configurações, em sequência, com temperatura 0 e semente 42. A saída final foi validada por Pydantic; recusa substitui falhas, portanto JSON final válido não mede a taxa de JSON bruto da LLM. Valores abaixo vêm de `avaliacao/resultados/v6/execucao_final/placar.csv`; tempos incluem recusas sem inferência e não comparam custos equivalentes.

| Medida | A | B | C |
|---|---:|---:|---:|
| Casos | 14 | 14 | 14 |
| JSON final válido | 14 | 14 | 14 |
| Recusas totais | 2 | 13 | 13 |
| Recusas em casos rotulados não consta | 0/6 | 6/6 | 6/6 |
| Recusas em casos rotulados consta | 2/8 | 7/8 | 7/8 |
| Respostas com IDs válidos e texto exato da base | não se aplica | 1 | 1 |
| Latência média, segundos | 1,574 | 0,335 | 0,322 |

O caso ambíguo T31 está rotulado como não consta, mas uma boa resposta deveria pedir detalhes; a simples contagem de recusa pelo rótulo não mede isso. O RAG e o agente recusam a maior parte do que a base contém: o projeto ainda não demonstra utilidade suficiente nem superioridade do agente. A extração literal comprova apenas identidade com o trecho interno, não a pertinência à pergunta ou correção do conteúdo. C fez verificações adicionais, mas nesta amostra não melhorou o placar em relação a B.

Revisão humana **não realizada**. A planilha `avaliacao/resultados/v6/execucao_final/revisao_humana.csv` contém pergunta, gabarito, resposta, evidências e campos vazios; `corretas`, `incorretas`, suporte semântico e alucinações permanecem pendentes. Critério proposto: correção exige atender ao gabarito sem fatos não sustentados; alucinação é ao menos uma afirmação factual não sustentada ou contraditória; recusa indevida é aquela que deixa de responder questão respondível. Revisão independente deve considerar suporte de cada afirmação e distinguir resposta parcial de recusa. Não interpretar citações estruturalmente válidas como citações semanticamente corretas.

## Cinco erros e integração

A comparação dos cinco casos, com JSON integral anterior e posterior, encontra-se em `avaliacao/comparacao_erros_v6.md`. T17 continua em recusa indevida, embora IPS-01 agora seja recuperado: o verificador rejeita a evidência. T18 passou a apresentar CDC-01; T29 recusou; T28 A repetiu uma alucinação. Não há garantia de reprodução determinística de todos os textos. As URLs das quatro fontes retornaram HTTP 200 em verificação registrada em `avaliacao/resultados/fontes_http.json`; acesso HTTP não valida automaticamente o conteúdo nem as condições de uso.

A API foi testada via HTTP local com Ollama, além dos testes de contrato com cliente de testes; registro em `avaliacao/resultados/api_live.json`. `exemplos/consumidor.py` demonstra consumo. Não há repositório do MVP nesta pasta, portanto não se afirma integração real. A API não tem autenticação e é experimental.

## Auditoria da rubrica

| Critério | Máximo | Implementação | Evidência | Estado | Pendência |
|---|---:|---|---|---|---|
| Tarefa e casos com gabarito e não consta | 0,5 | 32 casos sintéticos | `avaliacao/casos_teste.json` | Parcial | Novo conjunto independente e revisão dos rótulos ambíguos |
| Base segmentada e fontes | 1,0 | 15 trechos com metadados | `base/trechos.json` | Concluído | Ampliar fontes quando necessário |
| Busca, recall e limiar | 1,0 | TF-IDF, BM25 comparados | `avaliacao/resultados/v6/calibracao.csv` | Parcial | Medição cega após congelar o sistema |
| JSON, citação, fundamentação e recusa | 2,0 | Esquema, IDs, seleção e verificação | `src/agente.py`; `avaliacao/resultados/v6/execucao_final/geracao.jsonl` | Parcial | Revisão semântica independente; reduzir recusas indevidas; segurança |
| Especialização por agente versus RAG | 2,0 | Ferramentas de verificação e rastreio | `src/agente.py`; placar v6 | Parcial | Demonstrar benefício mensurado e reduzir falsas recusas |
| Placar comparativo de três configurações | 2,0 | Mesmo conjunto e latências | `avaliacao/resultados/v6/execucao_final/placar.csv` | Parcial | Preencher correção, fundamentação e alucinação após revisão humana |
| Cinco erros reais | 1,0 | Histórico e reexecução | `avaliacao/comparacao_erros_v6.md` | Concluído | T17 e referência A continuam falhando |
| README e reprodutibilidade | 0,5 | Instalação, testes, notebooks | `README.md`; `notebooks/` | Parcial | Reprodução independente e informações de equipe |

Não foi atribuída nota oficial. A aplicação continua uma prova de conceito local; não é adequada para produção, emergências ou decisões automáticas de contratação.
