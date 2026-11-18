import json
from pathlib import Path
sources = {
 'CDC': ('Código de Defesa do Consumidor, art. 40', 'Secretaria Nacional do Consumidor', 'https://www.consumidor.gov.br/pages/conteudo/publico/102', '1990-09-11'),
 'MME': ('Saiba como evitar acidentes elétricos dentro de casa', 'Ministério de Minas e Energia', 'https://www.gov.br/mme/pt-br/assuntos/secretarias/secretaria-nacional-energia-eletrica/mais-noticias/saiba-como-evitar-acidentes-eletricos-dentro-de-casa/', '2026-07-31'),
 'PROCON': ('Serviços privados: prestação de serviços', 'Procon-SP', 'https://www.procon.sp.gov.br/codigo/', None),
 'IPS': ('Choques elétricos e incêndios: cuidados no trabalho e em casa', 'Instituto de Previdência dos Servidores do Estado do Espírito Santo', 'https://www.ips.es.gov.br/detalhe-da-materia/info/37052/choques-eletricos-e-incendios-cuidados-no-trabalho-e-em-casa-podem-evitar-acidentes-graves/', None),
}
chunks = [
('CDC-01','CDC','O orçamento prévio de serviços deve discriminar mão de obra, materiais, equipamentos, condições de pagamento e datas de início e término.'),
('CDC-02','CDC','Salvo estipulação em contrário, o orçamento vale dez dias a partir de seu recebimento pelo consumidor.'),
('CDC-03','CDC','Após aprovação do orçamento, alterações dependem de livre negociação entre as partes.'),
('CDC-04','CDC','O consumidor não responde por acréscimos de serviços de terceiros não previstos no orçamento prévio.'),
('MME-01','MME','Para instalações, manutenção e reparos elétricos, procure profissionais qualificados e utilize materiais certificados.'),
('MME-02','MME','Evite o uso permanente de extensão e benjamim e não use aparelhos com cabos desencapados.'),
('MME-03','MME','Evite contato com aparelhos elétricos quando as mãos ou o corpo estiverem molhados; mantenha crianças afastadas de tomadas sem proteção.'),
('MME-04','MME','Em acidente elétrico, interrompa a energia pelo disjuntor ou chave geral quando possível e acione os bombeiros ou o SAMU.'),
('PROCON-01','PROCON','Em caso de serviço com vício, o consumidor pode escolher reexecução sem custo quando cabível, restituição ou abatimento proporcional do preço.'),
('PROCON-02','PROCON','O consumidor pode receber cópia da ordem de serviço e recibo de pagamento.'),
('PROCON-03','PROCON','O orçamento pode ser cobrado se o consumidor for informado antecipadamente sobre a cobrança.'),
('PROCON-04','PROCON','Se o serviço contratado não for realizado, o consumidor pode solicitar cumprimento, prestação equivalente ou rescisão, conforme as condições aplicáveis.'),
('IPS-01','IPS','Cheiro de queimado, faíscas ou tomadas quentes podem indicar problema elétrico; procure profissional qualificado e não faça improvisos.'),
('IPS-02','IPS','Não sobrecarregue tomadas e evite benjamins e extensões em excesso.'),
('IPS-03','IPS','Não troque o disjuntor por outro mais forte por conta própria; o problema pode estar na fiação.'),
]
base=[]
for id,doc,text in chunks:
 title, institution, url, date = sources[doc]
 base.append(dict(id=id,documento=doc,texto=text,titulo=title,instituicao=institution,url=url,publicacao=date,acesso='2026-11-17',formato='HTML',licenca='Não identificada; paráfrase curta para pesquisa com atribuição.'))
Path('base/trechos.json').write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding='utf-8')
