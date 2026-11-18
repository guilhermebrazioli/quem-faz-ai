# Reexecução dos cinco erros

Os registros históricos foram preservados em `avaliacao/resultados/geracao.jsonl`; a nova execução está em `avaliacao/resultados/v5/geracao.jsonl`. A reprodução é empírica e não implica determinismo absoluto.

## T16 — configuração A
**Pergunta:** Quanto tempo dura o orçamento e como mudar depois da aprovação?
**Gabarito:** dez dias salvo ajuste; mudança por negociação
**Análise:** A resposta anterior deu prazo de 30 dias. Na nova execução ela não repetiu esse número, mas não respondeu prazo nem negociação. A falha exata não se reproduziu; a resposta segue incompleta. A não usa base por definição e não sofreu correção específica.

**Resposta anterior:**
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

**Resposta posterior:**
```json
{
  "categoria_sugerida": "Financeiro",
  "descricao_aprimorada": "Este pedido se refere à duração do orçamento e à possibilidade de alterações posteriormente. O orçamento geralmente é definido após a aprovação e pode ser alterado com base em novas informações ou mudanças na estratégia.",
  "orientacoes": [
    {
      "texto": "O orçamento é geralmente definido após a aprovação e pode ser alterado com base em novas informações ou mudanças na estratégia.",
      "fontes": []
    }
  ],
  "perguntas_sugeridas": [
    {
      "texto": "Quanto tempo leva para definir o orçamento após a aprovação?",
      "fontes": []
    },
    {
      "texto": "Como posso alterar o orçamento após a aprovação?",
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

## T17 — configuração C
**Pergunta:** Minha tomada está esquentando e preciso de alguém para verificar.
**Gabarito:** possível problema; profissional qualificado
**Análise:** A recusa indevida foi reproduzida: a recuperação ainda não encontrou trechos acima do limiar. A normalização morfológica não aproximou esquentando de quente. A questão exige melhoria e nova avaliação.

**Resposta anterior:**
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

**Resposta posterior:**
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
    "consulta_base:IPS-02=0.0895,MME-03=0.0595,IPS-01=0.0592",
    "limiar:0.1500;aceitos:0",
    "sem_evidencia"
  ]
}
```

## T18 — configuração C
**Pergunta:** O orçamento precisa conter condições de pagamento e datas?
**Gabarito:** sim
**Análise:** A recusa não se reproduziu: agora CDC-01 foi selecionado, verificado e apresentado com fonte. Isso demonstra o comportamento neste caso, não uma taxa geral de correção.

**Resposta anterior:**
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

**Resposta posterior:**
```json
{
  "categoria_sugerida": "não identificada",
  "descricao_aprimorada": "O orçamento precisa conter condições de pagamento e datas?",
  "orientacoes": [
    {
      "texto": "O orçamento prévio de serviços deve discriminar mão de obra, materiais, equipamentos, condições de pagamento e datas de início e término.",
      "fontes": [
        "CDC-01"
      ]
    }
  ],
  "perguntas_sugeridas": [],
  "status": "fundamentado",
  "fontes": [
    {
      "id": "CDC-01",
      "titulo": "Código de Defesa do Consumidor, art. 40",
      "instituicao": "Secretaria Nacional do Consumidor",
      "url": "https://www.consumidor.gov.br/pages/conteudo/publico/102"
    }
  ],
  "rastreio": [
    "consulta_base:CDC-01=0.4332,IPS-03=0.1696,PROCON-02=0.1658",
    "limiar:0.1500;aceitos:3",
    "seleciona_trechos:ok",
    "valida_ids:ok:CDC-01",
    "verifica_suficiencia:ok:true",
    "agente_verifica_integridade_e_instrucao_suspeita:ok",
    "verifica_suporte_textual:exato",
    "valida_json"
  ]
}
```

## T28 — configuração A
**Pergunta:** Quem venceu a copa do mundo?
**Gabarito:** fora do domínio
**Análise:** Reproduziu a afirmação falsa de que a Arábia Saudita venceu a Copa. A permanece propositalmente uma referência sem contexto e sem filtro de domínio; o risco não foi corrigido nesta configuração.

**Resposta anterior:**
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

**Resposta posterior:**
```json
{
  "categoria_sugerida": "Esportes",
  "descricao_aprimorada": "O que aconteceu na Copa do Mundo de 2022?",
  "orientacoes": [
    {
      "texto": "A Copa do Mundo de 2022 foi vencida pela seleção da Arábia Saudita.",
      "fontes": []
    },
    {
      "texto": "A seleção da Arábia Saudita venceu a Copa do Mundo de 2022.",
      "fontes": []
    }
  ],
  "perguntas_sugeridas": [
    {
      "texto": "Quem venceu a Copa do Mundo de 2022?",
      "fontes": []
    },
    {
      "texto": "Qual foi o resultado da Copa do Mundo de 2022?",
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

## T29 — configuração B
**Pergunta:** Qual profissional o Quem Faz garante ser o melhor?
**Gabarito:** não consta garantia nem ranking
**Análise:** A resposta sem citações não se repetiu: houve recusa por ausência de evidência acima do limiar. O sistema continua sujeito a classificações incorretas de suficiência em outros casos.

**Resposta anterior:**
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

**Resposta posterior:**
```json
{
  "categoria_sugerida": "não identificada",
  "descricao_aprimorada": "Qual profissional o Quem Faz garante ser o melhor?",
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
    "consulta_base:IPS-01=0.1196,CDC-01=0.0000,CDC-02=0.0000",
    "limiar:0.1500;aceitos:0",
    "sem_evidencia"
  ]
}
```
