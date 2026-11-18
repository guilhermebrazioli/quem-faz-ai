# Sete recusas da avaliação reutilizada — agente C

Registro observacional: top 3, scores e rastreio vêm de `cega_v2/geracao.jsonl`; o experimento não guardou respostas brutas nem prompts exatos. O conjunto foi usado em duas rodadas e não é avaliação cega independente. Não foi feita nova chamada ao modelo. As verificações de adequação do gabarito são preliminares, pendentes de avaliação humana.

## B03
**Pergunta:** O valor acertado pode mudar unilateralmente depois que aceitei o orçamento?
**Gabarito:** mudança mediante livre negociação
**Fontes esperadas:** CDC-03: Após aprovação do orçamento, alterações dependem de livre negociação entre as partes.
**Top 3:** PROCON-03 = 0.0528; CDC-04 = 0.0512; CDC-03 = 0.0472
**Contexto inferível pelo código e limiar:** nenhum trecho; nenhuma chamada à LLM.
**Seleção registrada:** não houve seleção registrada.
**Bloqueio e causa provável:** O trecho sobre mudança de orçamento está no top 3, mas abaixo do limiar; a formulação pressupõe orçamento aprovado, condição explícita no trecho.
**Validação de citações:** não foi realizada, pois não houve seleção.
**Resposta bloqueada:** conteúdo bruto não registrado; não é possível verificar se uma resposta completa e válida foi rejeitada.
**Rastreio:** `consulta_base:PROCON-03=0.0528,CDC-04=0.0512,CDC-03=0.0472 → limiar:0.1500;aceitos:0 → sem_evidencia`

## B04
**Pergunta:** Cobram de mim serviço terceirizado que não apareceu na proposta prévia. Devo pagar o acréscimo?
**Gabarito:** consumidor não responde por acréscimos de terceiros não previstos
**Fontes esperadas:** CDC-04: O consumidor não responde por acréscimos de serviços de terceiros não previstos no orçamento prévio.
**Top 3:** PROCON-03 = 0.1118; CDC-04 = 0.1094; PROCON-04 = 0.0641
**Contexto inferível pelo código e limiar:** nenhum trecho; nenhuma chamada à LLM.
**Seleção registrada:** não houve seleção registrada.
**Bloqueio e causa provável:** CDC-04 está no top 3, mas abaixo do limiar. A fonte cobre acréscimos de terceiros não previstos, sujeitos ao contexto da relação de consumo.
**Validação de citações:** não foi realizada, pois não houve seleção.
**Resposta bloqueada:** conteúdo bruto não registrado; não é possível verificar se uma resposta completa e válida foi rejeitada.
**Rastreio:** `consulta_base:PROCON-03=0.1118,CDC-04=0.1094,PROCON-04=0.0641 → limiar:0.1500;aceitos:0 → sem_evidencia`

## B05
**Pergunta:** Que perfil de trabalhador é recomendado para executar reparos na instalação elétrica?
**Gabarito:** profissional qualificado e materiais certificados
**Fontes esperadas:** MME-01: Para instalações, manutenção e reparos elétricos, procure profissionais qualificados e utilize materiais certificados.
**Top 3:** MME-01 = 0.2891; MME-04 = 0.0497; MME-03 = 0.0478
**Contexto inferível pelo código e limiar:** MME-01: Para instalações, manutenção e reparos elétricos, procure profissionais qualificados e utilize materiais certificados.
**Seleção registrada:** valida_ids:ok:MME-01
**Bloqueio e causa provável:** MME-01 foi enviado e selecionado; o avaliador binário negou suficiência e a confirmação parcial não forneceu ID aceito. O trecho recomenda profissional qualificado.
**Validação de citações:** IDs selecionados passaram na checagem estrutural; nenhuma resposta foi liberada.
**Resposta bloqueada:** conteúdo bruto não registrado; não é possível verificar se uma resposta completa e válida foi rejeitada.
**Rastreio:** `consulta_base:MME-01=0.2891,MME-04=0.0497,MME-03=0.0478 → limiar:0.1500;aceitos:1 → inspeciona_contexto:ok → seleciona_trechos:ok → valida_ids:ok:MME-01 → verifica_suficiencia:ok:false → confirma_suporte_parcial:ok → evidencia_insuficiente`

## B06
**Pergunta:** Que prevenção a base indica para cabos com isolamento rompido e uso contínuo de extensões?
**Gabarito:** não usar cabos desencapados e evitar extensão permanente
**Fontes esperadas:** MME-02: Evite o uso permanente de extensão e benjamim e não use aparelhos com cabos desencapados.
**Top 3:** MME-02 = 0.1998; IPS-02 = 0.1251; IPS-01 = 0.0827
**Contexto inferível pelo código e limiar:** MME-02: Evite o uso permanente de extensão e benjamim e não use aparelhos com cabos desencapados.
**Seleção registrada:** valida_ids:ok:MME-02
**Bloqueio e causa provável:** MME-02 foi enviado e selecionado; a confirmação parcial não forneceu ID aceito. Cabo com isolamento rompido é interpretado como cabo desencapado, hipótese sujeita à revisão humana.
**Validação de citações:** IDs selecionados passaram na checagem estrutural; nenhuma resposta foi liberada.
**Resposta bloqueada:** conteúdo bruto não registrado; não é possível verificar se uma resposta completa e válida foi rejeitada.
**Rastreio:** `consulta_base:MME-02=0.1998,IPS-02=0.1251,IPS-01=0.0827 → limiar:0.1500;aceitos:1 → inspeciona_contexto:ok → seleciona_trechos:ok → valida_ids:ok:MME-02 → verifica_suficiencia:ok:false → confirma_suporte_parcial:ok → evidencia_insuficiente`

## B07
**Pergunta:** As mãos úmidas mudam os cuidados com equipamentos elétricos?
**Gabarito:** evitar contato com aparelhos quando molhado
**Fontes esperadas:** MME-03: Evite contato com aparelhos elétricos quando as mãos ou o corpo estiverem molhados; mantenha crianças afastadas de tomadas sem proteção.
**Top 3:** CDC-01 = 0.1982; MME-03 = 0.1355; MME-01 = 0.0642
**Contexto inferível pelo código e limiar:** CDC-01: O orçamento prévio de serviços deve discriminar mão de obra, materiais, equipamentos, condições de pagamento e datas de início e término.
**Seleção registrada:** valida_ids:ok:CDC-01
**Bloqueio e causa provável:** MME-03 está no top 3, mas abaixo do limiar. Apenas CDC-01 foi aceito e selecionado; não há evidência de que MME-03 tenha sido enviado ao modelo.
**Validação de citações:** IDs selecionados passaram na checagem estrutural; nenhuma resposta foi liberada.
**Resposta bloqueada:** conteúdo bruto não registrado; não é possível verificar se uma resposta completa e válida foi rejeitada.
**Rastreio:** `consulta_base:CDC-01=0.1982,MME-03=0.1355,MME-01=0.0642 → limiar:0.1500;aceitos:1 → inspeciona_contexto:ok → seleciona_trechos:ok → valida_ids:ok:CDC-01 → verifica_suficiencia:ok:false → confirma_suporte_parcial:ok → evidencia_insuficiente`

## B11
**Pergunta:** Fui avisado antes de que a elaboração da proposta seria cobrada; isso pode acontecer?
**Gabarito:** pode cobrar com informação prévia
**Fontes esperadas:** PROCON-03: O orçamento pode ser cobrado se o consumidor for informado antecipadamente sobre a cobrança.
**Top 3:** PROCON-03 = 0.1155; CDC-01 = 0.0000; CDC-02 = 0.0000
**Contexto inferível pelo código e limiar:** nenhum trecho; nenhuma chamada à LLM.
**Seleção registrada:** não houve seleção registrada.
**Bloqueio e causa provável:** PROCON-03 foi o primeiro resultado, mas ficou abaixo do limiar. A fonte cobre cobrança informada antecipadamente; proposta é interpretada como orçamento.
**Validação de citações:** não foi realizada, pois não houve seleção.
**Resposta bloqueada:** conteúdo bruto não registrado; não é possível verificar se uma resposta completa e válida foi rejeitada.
**Rastreio:** `consulta_base:PROCON-03=0.1155,CDC-01=0.0000,CDC-02=0.0000 → limiar:0.1500;aceitos:0 → sem_evidencia`

## B14
**Pergunta:** Devo substituir sozinho o disjuntor por um de amperagem maior?
**Gabarito:** não por conta própria
**Fontes esperadas:** IPS-03: Não troque o disjuntor por outro mais forte por conta própria; o problema pode estar na fiação.
**Top 3:** IPS-03 = 0.0974; MME-04 = 0.0852; CDC-01 = 0.0000
**Contexto inferível pelo código e limiar:** nenhum trecho; nenhuma chamada à LLM.
**Seleção registrada:** não houve seleção registrada.
**Bloqueio e causa provável:** IPS-03 foi o primeiro resultado, mas ficou abaixo do limiar. O trecho se refere a disjuntor mais forte; amperagem maior é interpretação técnica que deve ser revisada.
**Validação de citações:** não foi realizada, pois não houve seleção.
**Resposta bloqueada:** conteúdo bruto não registrado; não é possível verificar se uma resposta completa e válida foi rejeitada.
**Rastreio:** `consulta_base:IPS-03=0.0974,MME-04=0.0852,CDC-01=0.0000 → limiar:0.1500;aceitos:0 → sem_evidencia`
