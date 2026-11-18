from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient
root=Path(__file__).resolve().parent.parent
code='''from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
root=Path.cwd()
p=root/'avaliacao/resultados/cega_v1'
d=pd.read_csv(p/'placar.csv')
display(d)
r=pd.read_csv(p/'recuperacao.csv')
r=r[r.relevantes.notna()]
print('Casos respondíveis:',len(r),'Recall@1:',r.recall1.mean(),'Recall@3:',r.recall3.mean())
d.set_index('configuracao')[['recusas','json_valido']].plot.bar(title='Amostra nova: recusas e JSON final válido',ylim=(0,21),rot=0);plt.show()
print('Correção e fundamentação semântica: pendentes de revisão humana.')
'''
nb=nbf.v4.new_notebook(cells=[nbf.v4.new_markdown_cell('# Avaliação de 20 casos congelados antes da execução\n\nConstruídos pela mesma equipe do projeto; a revisão semântica independente permanece pendente.'),nbf.v4.new_code_cell(code)],metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}})
NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
nbf.write(nb,root/'notebooks/05_avaliacao_cega.ipynb');print('Notebook executado.')
