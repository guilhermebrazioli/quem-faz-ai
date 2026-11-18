from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient
root=Path(__file__).resolve().parent.parent
shared="""from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
root=Path.cwd()
pd.set_option('display.max_colwidth',100)
"""
items=[
('01_base.ipynb','Exploração da base',"""base=pd.read_json(root/'base/trechos.json')
print('Total de trechos:',len(base))
display(base.groupby(['documento','instituicao','formato','licenca']).size().rename('trechos').reset_index())
display(base[['id','texto','url']].head())
"""),
('02_recuperacao.ipynb','Recuperação e recall',"""d=pd.read_csv(root/'avaliacao/resultados/v6/calibracao.csv')
display(d[(d.metodo=='tfidf_stem') & (d.limiar==0.15)])
r=pd.read_csv(root/'avaliacao/resultados/v6/recuperacao_metodos.csv')
for name,g in r[r.relevantes.notna()].groupby(['metodo','particao']):
 print(name, 'recall@1=',round(g.recall1.mean(),4),'recall@3=',round(g.recall3.mean(),4),'hit@3=',round(g.hit3.mean(),4))
d[d.particao=='calibracao'].pivot(index='limiar',columns='metodo',values='corretos_binarios').plot(marker='o', title='Acertos binários por limiar na calibração',xlabel='Limiar (escalas diferentes)',ylabel='Acertos / 18',figsize=(8,4));plt.show()
"""),
('03_comparacao.ipynb','Comparação experimental',"""d=pd.read_csv(root/'avaliacao/resultados/v6/execucao_final/placar.csv')
display(d)
d.set_index('configuracao')[['recusas','json_valido']].plot.bar(title='Recusas e respostas finais válidas, n=14',ylim=(0,15),rot=0,figsize=(7,4));plt.show()
print('Correção e fundamentação semântica são pendentes de revisão humana.')
"""),
('04_erros.ipynb','Análise de erros observados',"""before=[json.loads(x) for x in (root/'avaliacao/resultados/geracao.jsonl').read_text(encoding='utf-8').splitlines()]
after=[json.loads(x) for x in (root/'avaliacao/resultados/v6/execucao_final/geracao.jsonl').read_text(encoding='utf-8').splitlines()]
keys=[('T16','A'),('T17','C'),('T18','C'),('T28','A'),('T29','B')]
rows=[]
for id,cfg in keys:
 a=next(x for x in before if x['id']==id and x['configuracao']==cfg)
 b=next(x for x in after if x['id']==id and x['configuracao']==cfg)
 rows.append({'caso':id,'configuração':cfg,'antes':a['resultado']['status'],'depois':b['resultado']['status'],'motivo_depois':b['resultado']['rastreio'][-1]})
display(pd.DataFrame(rows))
print('Rótulos de status não comprovam correção semântica; leia as respostas completas.')
""")]
for filename,title,code in items:
 nb=nbf.v4.new_notebook(cells=[nbf.v4.new_markdown_cell('# '+title+'\n\nResultados reais carregados dos artefatos do projeto.'),nbf.v4.new_code_cell(shared+code)],metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.12'}})
 NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
 nbf.write(nb,root/'notebooks'/filename)
 print('Executado:',filename)
