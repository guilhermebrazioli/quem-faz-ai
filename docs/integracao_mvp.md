# Integração com o MVP

A API REST recebe `descricao`, `categoria` opcional e `configuracao` A/B/C. Retorna `categoria_sugerida`, `descricao_aprimorada`, listas de objetos `{texto, fontes}`, `status`, metadados `fontes` e `rastreio`. IDs referenciam `base/trechos.json`. Uma recusa usa `informacao_insuficiente`. Erro de inferência retorna HTTP 503; entrada inválida retorna 422.

O contrato é proposto: o MVP publicado ([repositório](https://github.com/guilhermebrazioli/quem-faz)) não consome este endpoint; a integração existente é somente de leitura e está descrita na seção final. O aplicativo consumidor deve permitir revisão pelo usuário antes de publicar e tratar erros e recusa. Não envia dados de prestadores nem acessa avaliações. Implantação pública requer autenticação, limites, política de retenção e revisão de segurança.

## Evidência da continuação

`exemplos/consumidor.py` é um cliente demonstrativo; `exemplos/verificar_api.py` inicia uma instância local, realiza requisição HTTP real e encerra o processo sem sobrescrever resultados anteriores. O registro histórico está em `avaliacao/resultados/api_live.json`; a verificação final está em `avaliacao/resultados/verificacao_api_final.json`. `tests/test_core.py` cobre o contrato com um cliente em processo e dependências simuladas. Em C, a descrição recebida é preservada, as perguntas vêm vazias e as orientações são os trechos selecionados; em B, esses campos são gerados pela LLM. Nenhum desses testes comprova comunicação com o sistema principal do Quem Faz.

Atualização v7: o objeto pode incluir `observacao`, que informa que os trechos podem responder apenas parte do pedido. A interpretação semântica e o envio de uma eventual publicação continuam sujeitos à revisão do usuário. Evidência comparativa: `docs/relatorio_auditoria_v7.md`.

## Integração somente leitura com o MVP publicado

Integração com o MVP publicado: `scripts/demo_integracao_mvp.py` lê, somente por GET, as categorias e solicitações do MVP Quem Faz publicado na Azure ([repositório do MVP](https://github.com/guilhermebrazioli/quem-faz)) e envia perguntas de demonstração ao assistente local, associando cada uma a uma categoria real do MVP. A execução registrada em `avaliacao/resultados/integracao_mvp.json` leu 5 categorias (Elétrica, Hidráulica, Limpeza, Montagem de móveis e Pintura) e nenhuma solicitação. Na configuração B, a pergunta associada a Pintura foi fundamentada, com `categoria_sugerida` "Reforma", fora da taxonomia do MVP; a associada a Elétrica retornou `informacao_insuficiente`. Essas saídas não passaram por revisão humana e não integram a avaliação dos 60 casos. A integração não grava dados no MVP, o MVP não exibe as respostas e o assistente roda localmente com Ollama.
