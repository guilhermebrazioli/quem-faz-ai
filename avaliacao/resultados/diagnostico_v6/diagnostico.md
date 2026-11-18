# Diagnóstico da reexecução v6

A geração original não guardou resposta bruta nem contexto completo. Este diagnóstico é uma nova execução instrumentada da implementação v6 preservada, não uma reconstrução de dados que não foram gravados. Conteúdo e respostas brutas completos em `reexecucao.jsonl`. Pontuações, seleção e verificação se referem a essa reexecução.

## T16
**Pergunta:** Quanto tempo dura o orçamento e como mudar depois da aprovação?
**Gabarito:** dez dias salvo ajuste; mudança por negociação — CDC-02, CDC-03
**Recuperados:** CDC-03 (0.1657): Após aprovação do orçamento, alterações dependem de livre negociação entre as partes.; PROCON-03 (0.0543): O orçamento pode ser cobrado se o consumidor for informado antecipadamente sobre a cobrança.; CDC-04 (0.0526): O consumidor não responde por acréscimos de serviços de terceiros não previstos no orçamento prévio.
**Limiar:** 0.15; aceitos: CDC-03.
**Classificação:** Contexto insuficiente; falha de recuperação para CDC-02; falha de verificação semântica para a parte recuperada.
**Análise:** CDC-03 apareceu acima do limiar; CDC-02 não entrou no top 3. A base cobre validade e alteração, mas o contexto fornecido cobre só alteração.
**Chamada Selection:** validação ok
```text
Pergunta: Quanto tempo dura o orçamento e como mudar depois da aprovação?
Trechos: [{"id": "CDC-03", "texto": "Após aprovação do orçamento, alterações dependem de livre negociação entre as partes."}]
```
Resposta bruta: `{"ids": ["CDC-03"]}`
**Chamada Check:** validação ok
```text
Pergunta: Quanto tempo dura o orçamento e como mudar depois da aprovação?
Trechos: [CDC-03] Após aprovação do orçamento, alterações dependem de livre negociação entre as partes.
```
Resposta bruta: `{"suficiente": false}`
**Validação e motivo final:** consulta_base:CDC-03=0.1657,PROCON-03=0.0543,CDC-04=0.0526; limiar:0.1500;aceitos:1; seleciona_trechos:ok; valida_ids:ok:CDC-03; verifica_suficiencia:ok:false; evidencia_insuficiente

## T17
**Pergunta:** Minha tomada está esquentando e preciso de alguém para verificar.
**Gabarito:** possível problema; profissional qualificado — IPS-01, MME-01
**Recuperados:** IPS-01 (0.1628): Cheiro de queimado, faíscas ou tomadas quentes podem indicar problema elétrico; procure profissional qualificado e não faça improvisos.; IPS-02 (0.0924): Não sobrecarregue tomadas e evite benjamins e extensões em excesso.; MME-03 (0.0615): Evite contato com aparelhos elétricos quando as mãos ou o corpo estiverem molhados; mantenha crianças afastadas de tomadas sem proteção.
**Limiar:** 0.15; aceitos: IPS-01.
**Classificação:** Recusa indevida do modelo; verificação semântica.
**Análise:** IPS-01 foi recuperado e orienta procurar profissional; MME-01 não entrou no top 3. É possível responder ao menos parcialmente.
**Chamada Selection:** validação ok
```text
Pergunta: Minha tomada está esquentando e preciso de alguém para verificar.
Trechos: [{"id": "IPS-01", "texto": "Cheiro de queimado, faíscas ou tomadas quentes podem indicar problema elétrico; procure profissional qualificado e não faça improvisos."}]
```
Resposta bruta: `{"ids": ["IPS-01"]}`
**Chamada Check:** validação ok
```text
Pergunta: Minha tomada está esquentando e preciso de alguém para verificar.
Trechos: [IPS-01] Cheiro de queimado, faíscas ou tomadas quentes podem indicar problema elétrico; procure profissional qualificado e não faça improvisos.
```
Resposta bruta: `{"suficiente": false}`
**Validação e motivo final:** consulta_base:IPS-01=0.1628,IPS-02=0.0924,MME-03=0.0615; limiar:0.1500;aceitos:1; seleciona_trechos:ok; valida_ids:ok:IPS-01; verifica_suficiencia:ok:false; evidencia_insuficiente

## T18
**Pergunta:** O orçamento precisa conter condições de pagamento e datas?
**Gabarito:** sim — CDC-01
**Recuperados:** CDC-01 (0.4332): O orçamento prévio de serviços deve discriminar mão de obra, materiais, equipamentos, condições de pagamento e datas de início e término.; IPS-03 (0.1696): Não troque o disjuntor por outro mais forte por conta própria; o problema pode estar na fiação.; PROCON-02 (0.1658): O consumidor pode receber cópia da ordem de serviço e recibo de pagamento.
**Limiar:** 0.15; aceitos: CDC-01, IPS-03, PROCON-02.
**Classificação:** Sem falha observada nesta reexecução.
**Análise:** CDC-01 responde à pergunta e foi citado.
**Chamada Selection:** validação ok
```text
Pergunta: O orçamento precisa conter condições de pagamento e datas?
Trechos: [{"id": "CDC-01", "texto": "O orçamento prévio de serviços deve discriminar mão de obra, materiais, equipamentos, condições de pagamento e datas de início e término."}, {"id": "IPS-03", "texto": "Não troque o disjuntor por outro mais forte por conta própria; o problema pode estar na fiação."}, {"id": "PROCON-02", "texto": "O consumidor pode receber cópia da ordem de serviço e recibo de pagamento."}]
```
Resposta bruta: `{"ids": ["CDC-01"]}`
**Chamada Check:** validação ok
```text
Pergunta: O orçamento precisa conter condições de pagamento e datas?
Trechos: [CDC-01] O orçamento prévio de serviços deve discriminar mão de obra, materiais, equipamentos, condições de pagamento e datas de início e término.
```
Resposta bruta: `{"suficiente": true}`
**Validação e motivo final:** consulta_base:CDC-01=0.4332,IPS-03=0.1696,PROCON-02=0.1658; limiar:0.1500;aceitos:3; seleciona_trechos:ok; valida_ids:ok:CDC-01; verifica_suficiencia:ok:true; agente_verifica_integridade_e_instrucao_suspeita:ok; verifica_suporte_textual:exato; valida_json

## T19
**Pergunta:** Meu eletricista deve usar materiais certificados?
**Gabarito:** recomendação de materiais certificados — MME-01
**Recuperados:** MME-01 (0.2471): Para instalações, manutenção e reparos elétricos, procure profissionais qualificados e utilize materiais certificados.; CDC-01 (0.2147): O orçamento prévio de serviços deve discriminar mão de obra, materiais, equipamentos, condições de pagamento e datas de início e término.; CDC-02 (0.0000): Salvo estipulação em contrário, o orçamento vale dez dias a partir de seu recebimento pelo consumidor.
**Limiar:** 0.15; aceitos: MME-01, CDC-01.
**Classificação:** Verificação semântica e seleção com contexto parcialmente irrelevante.
**Análise:** MME-01 responde à pergunta; seleção incluiu também CDC-01, que não é necessário para o quesito.
**Chamada Selection:** validação ok
```text
Pergunta: Meu eletricista deve usar materiais certificados?
Trechos: [{"id": "MME-01", "texto": "Para instalações, manutenção e reparos elétricos, procure profissionais qualificados e utilize materiais certificados."}, {"id": "CDC-01", "texto": "O orçamento prévio de serviços deve discriminar mão de obra, materiais, equipamentos, condições de pagamento e datas de início e término."}]
```
Resposta bruta: `{"ids": ["MME-01", "CDC-01"]}`
**Chamada Check:** validação ok
```text
Pergunta: Meu eletricista deve usar materiais certificados?
Trechos: [MME-01] Para instalações, manutenção e reparos elétricos, procure profissionais qualificados e utilize materiais certificados.
[CDC-01] O orçamento prévio de serviços deve discriminar mão de obra, materiais, equipamentos, condições de pagamento e datas de início e término.
```
Resposta bruta: `{"suficiente": false}`
**Validação e motivo final:** consulta_base:MME-01=0.2471,CDC-01=0.2147,CDC-02=0.0000; limiar:0.1500;aceitos:2; seleciona_trechos:ok; valida_ids:ok:MME-01,CDC-01; verifica_suficiencia:ok:false; evidencia_insuficiente

## T20
**Pergunta:** Posso usar cabos desencapados e extensão permanentemente?
**Gabarito:** não; evitar — MME-02
**Recuperados:** MME-02 (0.5123): Evite o uso permanente de extensão e benjamim e não use aparelhos com cabos desencapados.; CDC-01 (0.0000): O orçamento prévio de serviços deve discriminar mão de obra, materiais, equipamentos, condições de pagamento e datas de início e término.; CDC-02 (0.0000): Salvo estipulação em contrário, o orçamento vale dez dias a partir de seu recebimento pelo consumidor.
**Limiar:** 0.15; aceitos: MME-02.
**Classificação:** Recusa indevida do modelo; verificação semântica.
**Análise:** MME-02 aborda cabos e extensões e foi selecionado, mas a decisão binária negou suficiência.
**Chamada Selection:** validação ok
```text
Pergunta: Posso usar cabos desencapados e extensão permanentemente?
Trechos: [{"id": "MME-02", "texto": "Evite o uso permanente de extensão e benjamim e não use aparelhos com cabos desencapados."}]
```
Resposta bruta: `{"ids": ["MME-02"]}`
**Chamada Check:** validação ok
```text
Pergunta: Posso usar cabos desencapados e extensão permanentemente?
Trechos: [MME-02] Evite o uso permanente de extensão e benjamim e não use aparelhos com cabos desencapados.
```
Resposta bruta: `{"suficiente": false}`
**Validação e motivo final:** consulta_base:MME-02=0.5123,CDC-01=0.0000,CDC-02=0.0000; limiar:0.1500;aceitos:1; seleciona_trechos:ok; valida_ids:ok:MME-02; verifica_suficiencia:ok:false; evidencia_insuficiente

## T21
**Pergunta:** Se a pintura falhar, quais opções tenho?
**Gabarito:** reexecução, restituição ou abatimento — PROCON-01
**Recuperados:** PROCON-01 (0.1436): Em caso de serviço com vício, o consumidor pode escolher reexecução sem custo quando cabível, restituição ou abatimento proporcional do preço.; CDC-01 (0.0000): O orçamento prévio de serviços deve discriminar mão de obra, materiais, equipamentos, condições de pagamento e datas de início e término.; CDC-02 (0.0000): Salvo estipulação em contrário, o orçamento vale dez dias a partir de seu recebimento pelo consumidor.
**Limiar:** 0.15; aceitos: nenhum.
**Classificação:** Falha de recuperação pelo limiar; gabarito depende de enquadramento.
**Análise:** PROCON-01 foi o primeiro, com score abaixo de 0,15. Um defeito de pintura pode configurar vício, mas falha não comprova automaticamente o enquadramento jurídico.
**Contexto e resposta da LLM:** não houve chamada após o limiar.
**Validação e motivo final:** consulta_base:PROCON-01=0.1436,CDC-01=0.0000,CDC-02=0.0000; limiar:0.1500;aceitos:0; sem_evidencia

## T22
**Pergunta:** Um profissional pode acrescentar serviço após orçamento aprovado?
**Gabarito:** alterações por livre negociação — CDC-03
**Recuperados:** CDC-03 (0.3659): Após aprovação do orçamento, alterações dependem de livre negociação entre as partes.; CDC-04 (0.1361): O consumidor não responde por acréscimos de serviços de terceiros não previstos no orçamento prévio.; IPS-01 (0.1215): Cheiro de queimado, faíscas ou tomadas quentes podem indicar problema elétrico; procure profissional qualificado e não faça improvisos.
**Limiar:** 0.15; aceitos: CDC-03.
**Classificação:** Recusa indevida do modelo; verificação semântica.
**Análise:** CDC-03 cobre alteração por negociação; o verificador negou suficiência.
**Chamada Selection:** validação ok
```text
Pergunta: Um profissional pode acrescentar serviço após orçamento aprovado?
Trechos: [{"id": "CDC-03", "texto": "Após aprovação do orçamento, alterações dependem de livre negociação entre as partes."}]
```
Resposta bruta: `{"ids": ["CDC-03"]}`
**Chamada Check:** validação ok
```text
Pergunta: Um profissional pode acrescentar serviço após orçamento aprovado?
Trechos: [CDC-03] Após aprovação do orçamento, alterações dependem de livre negociação entre as partes.
```
Resposta bruta: `{"suficiente": false}`
**Validação e motivo final:** consulta_base:CDC-03=0.3659,CDC-04=0.1361,IPS-01=0.1215; limiar:0.1500;aceitos:1; seleciona_trechos:ok; valida_ids:ok:CDC-03; verifica_suficiencia:ok:false; evidencia_insuficiente

## T23
**Pergunta:** Quais dados incluir para orçamento de pintura e qual o prazo de validade?
**Gabarito:** pagamento, datas, mão de obra e materiais; dez dias salvo ajuste — CDC-01, CDC-02
**Recuperados:** CDC-02 (0.1639): Salvo estipulação em contrário, o orçamento vale dez dias a partir de seu recebimento pelo consumidor.; PROCON-03 (0.0595): O orçamento pode ser cobrado se o consumidor for informado antecipadamente sobre a cobrança.; CDC-04 (0.0577): O consumidor não responde por acréscimos de serviços de terceiros não previstos no orçamento prévio.
**Limiar:** 0.15; aceitos: CDC-02.
**Classificação:** Contexto insuficiente; falha de recuperação para CDC-01.
**Análise:** CDC-02 foi aceito; CDC-01 não entrou no top 3. A base cobre itens gerais e validade, não especificações técnicas de pintura.
**Chamada Selection:** validação ok
```text
Pergunta: Quais dados incluir para orçamento de pintura e qual o prazo de validade?
Trechos: [{"id": "CDC-02", "texto": "Salvo estipulação em contrário, o orçamento vale dez dias a partir de seu recebimento pelo consumidor."}]
```
Resposta bruta: `{"ids": ["CDC-02"]}`
**Chamada Check:** validação ok
```text
Pergunta: Quais dados incluir para orçamento de pintura e qual o prazo de validade?
Trechos: [CDC-02] Salvo estipulação em contrário, o orçamento vale dez dias a partir de seu recebimento pelo consumidor.
```
Resposta bruta: `{"suficiente": false}`
**Validação e motivo final:** consulta_base:CDC-02=0.1639,PROCON-03=0.0595,CDC-04=0.0577; limiar:0.1500;aceitos:1; seleciona_trechos:ok; valida_ids:ok:CDC-02; verifica_suficiencia:ok:false; evidencia_insuficiente
