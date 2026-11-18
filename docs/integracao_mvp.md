# Integração com o MVP

A API REST recebe `descricao`, `categoria` opcional e `configuracao` A/B/C. Retorna `categoria_sugerida`, `descricao_aprimorada`, listas de objetos `{texto, fontes}`, `status`, metadados `fontes` e `rastreio`. IDs referenciam `base/trechos.json`. Uma recusa usa `informacao_insuficiente`. Erro de inferência retorna HTTP 503; entrada inválida retorna 422.

O contrato é proposto: nenhum repositório ou contrato do MVP foi disponibilizado. O aplicativo consumidor deve permitir revisão pelo usuário antes de publicar e tratar erros e recusa. Não envia dados de prestadores nem acessa avaliações. Implantação pública requer autenticação, limites, política de retenção e revisão de segurança.

## Evidência da continuação

`exemplos/consumidor.py` é um cliente demonstrativo; `exemplos/verificar_api.py` inicia uma instância local, realiza requisição HTTP real e encerra o processo sem sobrescrever resultados anteriores. O registro histórico está em `avaliacao/resultados/api_live.json`; a verificação final está em `avaliacao/resultados/verificacao_api_final.json`. `tests/test_core.py` cobre o contrato com um cliente em processo e dependências simuladas. Em C, a descrição recebida é preservada, as perguntas vêm vazias e as orientações são os trechos selecionados; em B, esses campos são gerados pela LLM. Nenhum desses testes comprova comunicação com o sistema principal do Quem Faz.

Atualização v7: o objeto pode incluir `observacao`, que informa que os trechos podem responder apenas parte do pedido. A interpretação semântica e o envio de uma eventual publicação continuam sujeitos à revisão do usuário. Evidência comparativa: `docs/relatorio_auditoria_v7.md`.
