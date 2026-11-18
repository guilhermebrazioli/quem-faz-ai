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

O assistente local consulta orientações de contratação e segurança, sem certificar profissionais ou decidir pelo usuário. É uma prova de conceito exposta por API REST, com consumidor demonstrativo.

## O que consultar

- [Relatório acadêmico](docs/RELATORIO_FINAL_GENERATIVE_AI.md), [arquitetura](docs/arquitetura.md) e [contrato de integração](docs/integracao_mvp.md).
- [Instruções de instalação e execução](README.md) e [comandos de publicação](COMANDOS_PUBLICACAO.md).
- [Base e fontes](base/trechos.json) e [casos da avaliação final com gabarito](avaliacao/casos_cegos_v1.json).
- Avaliação final: [manifesto de congelamento](avaliacao/congelamento_final.json), [respostas](avaliacao/resultados/final/geracao.jsonl), [recuperação](avaliacao/resultados/final/recuperacao.csv), [placar automático](avaliacao/resultados/final/placar.csv), [revisão humana](avaliacao/resultados/final/revisao_humana.csv) e [placar da revisão humana](avaliacao/resultados/final/placar_revisao_humana.json).
- [Notebooks executados](notebooks/) e [erros históricos](avaliacao/comparacao_erros_v8.md).

Repositório GitHub: [https://github.com/guilhermebrazioli/quem-faz-ai](https://github.com/guilhermebrazioli/quem-faz-ai). Vídeo: [inserir URL].

## Execução

```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull qwen2.5:1.5b
python -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Com o Ollama ativo e em outro terminal, execute `python exemplos/consumidor.py`. Testes: `python -m pytest -q` (30 aprovados na entrega). Auditoria: `python scripts/verificar_entrega.py --testes`.

## Resultados

Avaliação cega de 20 casos (14 com resposta na base, 6 sem) × 3 configurações, com revisão humana das 60 respostas.

| Métrica | A (LLM sem contexto) | B (RAG simples) | C (Agente) |
|---|---|---|---|
| Corretas | 3 (15%) | 14 (70%) | 13 (65%) |
| Com alucinação | 20 (100%) | 2 (10%) | 0 (0%) |
| Respostas sustentadas pelas fontes | 0/20 | 5/11 | 7/7 |
| Recusas adequadas / indevidas | não se aplica | 5 / 4 | 6 / 7 |
| JSON final válido | 20/20 | 20/20 | 20/20 |
| Latência média | 3,417 s | 1,337 s | 0,378 s |

Recall macro@1 = 0,786 e recall macro@3 = 1,000 nos 14 casos com evidência. B teve a maior taxa de acerto; C eliminou as alucinações ao custo de mais recusas indevidas. A latência média inclui recusas sem chamada à LLM.

## Rubrica

| Critério | Máximo | Evidência | Situação |
|---|---:|---|---|
| Tarefa e gabarito, inclusive não consta | 0,5 | `avaliacao/casos_cegos_v1.json` | Concluído: 14 casos consta e 6 não consta |
| Base segmentada com fontes | 1,0 | `base/trechos.json` | Concluído: 15 trechos de 4 fontes públicas |
| Recall e limiar | 1,0 | `avaliacao/resultados/final/recuperacao.csv`, `avaliacao/resultados/v6/calibracao.csv` | Concluído: recall@1 0,786, recall@3 1,0, limiar 0,15 |
| JSON, fontes, fundamentação e recusa | 2,0 | `src/core.py`, `src/agente.py`, `avaliacao/resultados/final/geracao.jsonl` | Concluído: fundamentação e recusas revisadas por humano |
| Agente comparado a RAG | 2,0 | `avaliacao/resultados/final/placar_revisao_humana.json` | Concluído: C elimina alucinações; B acerta mais |
| Placar das três configurações | 2,0 | `avaliacao/resultados/final/placar.csv`, `avaliacao/resultados/final/placar_revisao_humana.json` | Concluído: métricas automáticas e humanas |
| Cinco erros reais | 1,0 | Seção 13 do relatório | Concluído: causa e correção proposta |
| README e reprodução | 0,5 | `README.md`, `requirements.txt`, `notebooks/` | Concluído |

Limitações: amostra pequena e escrita pela equipe; API sem autenticação; A pode alucinar e não deve ser usada para orientação de segurança. Os nomes e RMs são dados pessoais e sua divulgação pública deve ser confirmada pelo grupo.

## Integração com o MVP

- Script: `scripts/demo_integracao_mvp.py` (somente leitura).
- Registro: `avaliacao/resultados/integracao_mvp.json`.
- Integração com o MVP publicado: `scripts/demo_integracao_mvp.py` lê, somente por GET, as categorias e solicitações do MVP Quem Faz publicado na Azure ([repositório do MVP](https://github.com/guilhermebrazioli/quem-faz)) e envia perguntas de demonstração ao assistente local, associando cada uma a uma categoria real do MVP. A execução registrada em `avaliacao/resultados/integracao_mvp.json` leu 5 categorias (Elétrica, Hidráulica, Limpeza, Montagem de móveis e Pintura) e nenhuma solicitação. Na configuração B, a pergunta associada a Pintura foi fundamentada, com `categoria_sugerida` "Reforma", fora da taxonomia do MVP; a associada a Elétrica retornou `informacao_insuficiente`. Essas saídas não passaram por revisão humana e não integram a avaliação dos 60 casos. A integração não grava dados no MVP, o MVP não exibe as respostas e o assistente roda localmente com Ollama.
