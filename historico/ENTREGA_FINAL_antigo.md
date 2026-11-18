# Quem Faz AI — Entrega acadêmica

FIAP · Global Solution 2026.2 · Engenharia de Software · Generative AI for Engineering · Professor Francisco Elanio Bezerra.

Prazo informado para a entrega: 19/11/2026 às 23h55.

| Integrante | RM |
|---|---|
| Enzo Vazquez Sartorelli | RM94618 |
| Kaue Pastori Teixeira | RM98501 |
| Nicolas Nogueira Boni | RM551965 |
| Guilherme Brazioli | RM98237 |
| Pedro Oliveira Valotto | RM551445 |

O assistente local consulta orientações de contratação e segurança, sem certificar profissionais ou decidir pelo usuário. É uma prova de conceito; não há integração testada com o MVP principal.

## O que consultar

- [Relatório acadêmico](docs/RELATORIO_FINAL_GENERATIVE_AI.md), [arquitetura](docs/arquitetura.md) e [integração demonstrativa](docs/integracao_mvp.md).
- [Instruções de instalação e execução](README.md) e [comandos de publicação](COMANDOS_PUBLICACAO.md).
- [Base e fontes](base/trechos.json), [casos adicionais e gabarito](avaliacao/casos_internos_adicionais.json), [placar da reexecução exploratória](avaliacao/resultados/adicional_v2/placar.csv), [respostas completas](avaliacao/resultados/adicional_v2/geracao.jsonl) e [primeira execução preservada](avaliacao/resultados/adicional_v1/placar.csv).
- [Pré-revisão automática das 60 respostas anteriores](avaliacao/resultados/cega_v2/pre_revisao_automatica.jsonl); regras estruturais, não julgamento humano ou comprovação semântica.
- [Pré-revisão pelo modelo local](avaliacao/resultados/cega_v2/pre_revisao_modelo.jsonl); avaliação automática inconsistente, com 13 falhas de esquema, que não substitui revisão humana.
- [Cinco erros reais](avaliacao/comparacao_erros_v8.md), [sete recusas](avaliacao/investigacao_sete_recusas.md) e [notebooks executados](notebooks/).

Repositório GitHub e vídeo: não informados ou ainda não publicados.

## Execução

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull qwen2.5:1.5b
python -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Com Ollama ativo e em outro terminal, execute `python exemplos/consumidor.py`. Testes: `python -m pytest -q`. Auditoria: `python scripts/verificar_entrega.py --testes`. Consulte o README para experimentos, revisão humana e tratamento de erros.

## Resultados e rubrica

Na amostra adicional interna de 16 perguntas, 10 com gabarito de trechos, recall macro@1 foi 0,9 e recall macro@3 foi 1,0, sem aplicar limiar. Após uma correção de segurança, os mesmos casos foram reexecutados: cada configuração gerou 16 respostas JSON finais válidas; B e C apresentaram quatro respostas com IDs válidos e texto literal e recusaram seis dos dez casos rotulados respondíveis e os seis rotulados não consta. Essa segunda execução é exploratória, não uma nova amostra. Não se conclui superioridade do agente. Correção, suporte semântico e alucinação exigem revisão humana. A amostra foi escrita no próprio projeto e não constitui validação independente.

| Critério | Máximo | Evidência | Situação |
|---|---:|---|---|
| Tarefa e gabarito, inclusive não consta | 0,5 | `avaliacao/casos_teste.json`, `avaliacao/casos_internos_adicionais.json` | Parcial: gabaritos aguardam revisão independente |
| Base segmentada com fontes | 1,0 | `base/trechos.json` | Implementado |
| Recall e limiar | 1,0 | `avaliacao/resultados/adicional_v2/recuperacao.csv`, `avaliacao/resultados/v6/calibracao.csv` | Medido, amostra limitada |
| JSON, fontes, fundamentação e recusa | 2,0 | `src/agente.py`, `avaliacao/resultados/adicional_v2/geracao.jsonl` | Parcial: pertinência semântica não revisada |
| Agente comparado a RAG | 2,0 | `avaliacao/resultados/adicional_v2/placar.csv` | Comparado; benefício não demonstrado |
| Placar das três configurações | 2,0 | `avaliacao/resultados/adicional_v2/placar.csv` | Parcial: métricas humanas pendentes |
| Cinco erros reais | 1,0 | `avaliacao/comparacao_erros_v8.md` | Documentado e reexecutado |
| README e reprodução | 0,5 | `README.md`, `requirements.txt`, `notebooks/` | Documentado; reprodução independente pendente |

A verificação de IDs não confirma suporte semântico. O sistema ainda recusa perguntas respondíveis; a configuração A pode alucinar e não deve ser usada para orientação de segurança. Os nomes e RMs são dados pessoais e sua divulgação pública deve ser confirmada pelo grupo.
