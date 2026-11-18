# Checklist de entrega — Quem Faz AI

| Requisito | Situação | Evidência | Pendência |
|---|---|---|---|
| Identificação dos integrantes e RMs | Concluído | `docs/RELATORIO_FINAL_GENERATIVE_AI.md` | Conferência pelo grupo |
| Tarefa e gabaritos com não consta | Parcial | `avaliacao/casos_teste.json`, `avaliacao/casos_cegos_v1.json` | Revisão independente dos rótulos |
| Base segmentada e fontes | Concluído | `base/trechos.json`; `avaliacao/resultados/fontes_http_v7.json` | Conferir condições de uso |
| Busca, recall e limiar | Concluído | `avaliacao/resultados/cega_v2/recuperacao.csv`, `avaliacao/resultados/v6/calibracao.csv` | Amostra maior e gabarito independente |
| JSON, fontes, recusa e suporte | Parcial | `src/agente.py`; respostas em `avaliacao/resultados/cega_v2/geracao.jsonl` | Revisão semântica e redução das recusas indevidas |
| Agente em comparação com RAG | Parcial | `avaliacao/resultados/cega_v2/placar.csv` | Benefício adicional não demonstrado |
| Placar das três configurações | Parcial | `avaliacao/resultados/cega_v2/placar.csv` | Métricas humanas não preenchidas |
| Cinco erros reais e reexecução | Concluído | `avaliacao/comparacao_erros_v8.md` | Há falhas ainda reproduzíveis |
| Sete recusas investigadas | Concluído com ressalva | `avaliacao/investigacao_sete_recusas.md` | Respostas brutas históricas não foram registradas; interpretação depende de revisão |
| Revisão humana e segunda pessoa | Preparada | `avaliacao/revisao_web.py`; `avaliacao/resultados/cega_v2/segunda_revisao.csv` | Nenhuma avaliação humana atribuída; mapa local necessário para consolidar |
| Reprodutibilidade | Parcial | `README.md`, `docs/manifesto_experimentos.json`, seis notebooks, testes | Reprodução por avaliador independente |
| Integração com plataforma | Demonstrativa | `exemplos/consumidor.py`; `avaliacao/resultados/verificacao_api_final.json` | MVP principal indisponível; integração real não testada |
| Publicação GitHub | Preparada | `.gitignore`; comandos no `README.md` | Repositório GitHub, revisão e publicação pelo responsável |

A checagem de IDs é estrutural e não equivale à fundamentação semântica. Os nomes e RMs fornecidos para identificação acadêmica são dados pessoais e ficarão públicos se o relatório for publicado; o grupo deve confirmar essa divulgação antes de enviar ao GitHub. Os endereços eletrônicos não foram adicionados. O mapa da segunda revisão é local e está ignorado pelo Git. Esta lista não atribui nota oficial.
