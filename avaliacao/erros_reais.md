# Cinco falhas observadas

Dados originais integrais em `resultados/geracao.jsonl`; os textos abaixo foram extra?dos dessa execu??o. Corre??es propostas n?o foram implementadas nem retestadas.

## T16 ? configura??o A
**Pergunta:** Quanto tempo dura o orçamento e como mudar depois da aprovação?
**Esperado:** dez dias salvo ajuste; mudança por negociação
**Resposta obtida:**
```json
{
  "categoria_sugerida": "Financeiro",
  "descricao_aprimorada": "Este é um pedido sobre o tempo de duração do orçamento e como alterar a aprovação posteriormente.",
  "orientacoes": [
    {
      "texto": "O orçamento geralmente é projetado para durar até 30 dias após a aprovação.",
      "fontes": []
    },
    {
      "texto": "Para alterar a aprovação do orçamento, é necessário entrar em contato com o departamento responsável e solicitar a alteração.",
      "fontes": []
    }
  ],
  "perguntas_sugeridas": [
    {
      "texto": "Quanto tempo dura o orçamento após a aprovação?",
      "fontes": []
    },
    {
      "texto": "Como faço para alterar a aprovação do orçamento?",
      "fontes": []
    }
  ],
  "status": "sem_contexto",
  "fontes": [],
  "rastreio": [
    "gera_json_llm"
  ]
}
```
**Erro:** Resposta incorreta sobre validade e altera??o; a base prev? dez dias salvo estipula??o e altera??o por negocia??o.
**Causa prov?vel:** Conhecimento do modelo sem recupera??o.
**Corre??o proposta:** Recuperar CDC-02 e CDC-03 e exigir verifica??o de suporte. Resultado da corre??o: n?o testado.

## T17 ? configura??o C
**Pergunta:** Minha tomada está esquentando e preciso de alguém para verificar.
**Esperado:** possível problema; profissional qualificado
**Resposta obtida:**
```json
{
  "categoria_sugerida": "não identificada",
  "descricao_aprimorada": "Minha tomada está esquentando e preciso de alguém para verificar.",
  "orientacoes": [
    {
      "texto": "Não consta na base de conhecimento informação suficiente para responder com segurança.",
      "fontes": []
    }
  ],
  "perguntas_sugeridas": [],
  "status": "informacao_insuficiente",
  "fontes": [],
  "rastreio": [
    "consulta_base",
    "verifica_limiar",
    "sem_evidencia"
  ]
}
```
**Erro:** Recusa apesar de haver informa??es pertinentes sobre tomada quente e profissional qualificado.
**Causa prov?vel:** Busca lexical n?o relaciona tomada/tomadas nem esquentando/quente.
**Corre??o proposta:** Normalizar flex?es e avaliar busca sem?ntica local. Resultado da corre??o: n?o testado.

## T18 ? configura??o C
**Pergunta:** O orçamento precisa conter condições de pagamento e datas?
**Esperado:** sim
**Resposta obtida:**
```json
{
  "categoria_sugerida": "não identificada",
  "descricao_aprimorada": "O orçamento precisa conter condições de pagamento e datas?",
  "orientacoes": [
    {
      "texto": "Não consta na base de conhecimento informação suficiente para responder com segurança.",
      "fontes": []
    }
  ],
  "perguntas_sugeridas": [],
  "status": "informacao_insuficiente",
  "fontes": [],
  "rastreio": [
    "consulta_base",
    "verifica_limiar",
    "gera_json_llm",
    "valida_citacoes",
    "citacao_ausente_ou_invalida"
  ]
}
```
**Erro:** Recusa uma pergunta expressamente respondida por CDC-01.
**Causa prov?vel:** A valida??o de cita??es rejeitou pelo menos um item com fonte ausente ou inv?lida.
**Corre??o proposta:** Melhorar formato de sa?da e tentar novamente com erros de valida??o. Resultado da corre??o: n?o testado.

## T28 ? configura??o A
**Pergunta:** Quem venceu a copa do mundo?
**Esperado:** fora do domínio
**Resposta obtida:**
```json
{
  "categoria_sugerida": "Esportes",
  "descricao_aprimorada": "Descubra quem venceu a Copa do Mundo de 2022.",
  "orientacoes": [
    {
      "texto": "A Copa do Mundo de 2022 foi vencida pela seleção da Arábia Saudita.",
      "fontes": []
    },
    {
      "texto": "A Copa do Mundo de 2022 foi vencida pela seleção da Arábia Saudita.",
      "fontes": []
    }
  ],
  "perguntas_sugeridas": [
    {
      "texto": "Quem venceu a Copa do Mundo de 2022?",
      "fontes": []
    }
  ],
  "status": "sem_contexto",
  "fontes": [],
  "rastreio": [
    "gera_json_llm"
  ]
}
```
**Erro:** Respondeu pergunta fora do dom?nio e inventou que a Ar?bia Saudita venceu a Copa.
**Causa prov?vel:** Aus?ncia de filtro de dom?nio e de evid?ncia na refer?ncia sem contexto.
**Corre??o proposta:** Aplicar recusa para perguntas fora do dom?nio e avaliar roteamento. Resultado da corre??o: n?o testado.

## T29 ? configura??o B
**Pergunta:** Qual profissional o Quem Faz garante ser o melhor?
**Esperado:** não consta garantia nem ranking
**Resposta obtida:**
```json
{
  "categoria_sugerida": "Eletricista",
  "descricao_aprimorada": "Profissional qualificado para diagnóstico e reparo de problemas elétricos.",
  "orientacoes": [
    {
      "texto": "Consulte um profissional qualificado para diagnosticar e reparar problemas elétricos.",
      "fontes": []
    },
    {
      "texto": "Evite fazer improvisos, pois podem levar a problemas ainda maiores.",
      "fontes": []
    }
  ],
  "perguntas_sugeridas": [
    {
      "texto": "Quais são os sinais de queimado, faíscas ou tomadas quentes que podem indicar um problema elétrico?",
      "fontes": []
    },
    {
      "texto": "Como posso garantir que o profissional qualificado é o melhor para o meu caso?",
      "fontes": []
    }
  ],
  "status": "fundamentado",
  "fontes": [],
  "rastreio": [
    "consulta_base",
    "verifica_limiar",
    "gera_json_llm"
  ]
}
```
**Erro:** Retornou dicas el?tricas sem responder ? pergunta sobre garantia e melhor profissional; status fundamentado sem fontes.
**Causa prov?vel:** Limiar lexical n?o avalia sufici?ncia e B n?o exige IDs nas afirma??es.
**Corre??o proposta:** Detectar perguntas sem suporte e validar fontes; avaliar o efeito sobre casos respond?veis. Resultado da corre??o: n?o testado.
