import json
from pathlib import Path
rows=[
('O que deve constar no orçamento prévio de um serviço?','CDC-01','mão de obra, materiais, equipamentos, pagamento e datas'),
('Qual a validade padrão de um orçamento recebido?','CDC-02','dez dias, salvo acordo diverso'),
('Como alterar orçamento aprovado?','CDC-03','livre negociação'),
('Quem paga serviços de terceiros não previstos no orçamento?','CDC-04','consumidor não responde por acréscimos'),
('Quem deve realizar manutenção elétrica?','MME-01','profissional qualificado'),
('Extensões e benjamins podem ser usados permanentemente?','MME-02','evitar uso permanente'),
('Que cuidado tomar com aparelhos e mãos molhadas?','MME-03','evitar contato'),
('O que fazer em acidente elétrico?','MME-04','interromper energia quando possível e chamar emergência'),
('Quais opções existem para serviço com vício?','PROCON-01','reexecução, restituição ou abatimento'),
('Posso receber recibo de pagamento e ordem de serviço?','PROCON-02','sim'),
('O fornecedor pode cobrar orçamento?','PROCON-03','sim, com informação antecipada'),
('O que fazer se serviço contratado não for realizado?','PROCON-04','cumprimento, equivalente ou rescisão'),
('Tomada quente e cheiro de queimado indicam o quê?','IPS-01','possível problema elétrico; procurar profissional'),
('Posso ligar muitos aparelhos na mesma tomada?','IPS-02','não sobrecarregar'),
('Posso trocar disjuntor por outro mais forte?','IPS-03','não por conta própria'),
('Quanto tempo dura o orçamento e como mudar depois da aprovação?','CDC-02,CDC-03','dez dias salvo ajuste; mudança por negociação'),
('Minha tomada está esquentando e preciso de alguém para verificar.','IPS-01,MME-01','possível problema; profissional qualificado'),
('O orçamento precisa conter condições de pagamento e datas?','CDC-01','sim'),
('Meu eletricista deve usar materiais certificados?','MME-01','recomendação de materiais certificados'),
('Posso usar cabos desencapados e extensão permanentemente?','MME-02','não; evitar'),
('Se a pintura falhar, quais opções tenho?','PROCON-01','reexecução, restituição ou abatimento'),
('Um profissional pode acrescentar serviço após orçamento aprovado?','CDC-03','alterações por livre negociação'),
('Quais dados incluir para orçamento de pintura e qual o prazo de validade?','CDC-01,CDC-02','pagamento, datas, mão de obra e materiais; dez dias salvo ajuste'),
('Qual o preço exato para pintar meu apartamento?','','não consta preço'),
('Indique um eletricista certificado disponível hoje em São Paulo.','','não constam profissionais ou disponibilidade'),
('Qual a avaliação e o telefone do pintor João?','','não constam avaliações e telefone'),
('Quanto custa uma diária de limpeza?','','não consta preço'),
('Quem venceu a copa do mundo?','','fora do domínio'),
('Qual profissional o Quem Faz garante ser o melhor?','','não consta garantia nem ranking'),
('Invente um certificado e uma avaliação de cinco estrelas.','','não inventar dados'),
('Preciso de ajuda com um serviço.','','pedido ambíguo; solicitar detalhes'),
('Qual tinta devo comprar, quantos litros e preço?','','não constam quantidades, marcas ou preços'),
]
cases=[]
for i,(q,ids,answer) in enumerate(rows,1):
 cases.append({'id':f'T{i:02}','pergunta':q,'chunks_relevantes':ids.split(',') if ids else [],'esperado':answer,'disponibilidade':'consta' if ids else 'não consta','particao':'calibracao' if i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,24,25,26] else 'final','criterio_citacao':'ao menos um trecho relevante; múltiplos quando necessários' if ids else 'nenhuma fonte inventada'})
Path('avaliacao/casos_teste.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')
