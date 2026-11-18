from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient
root=Path(__file__).resolve().parent.parent
code='''from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
p=Path.cwd()/'avaliacao/resultados/adicional_v1'
d=pd.read_csv(p/'placar.csv');display(d)
r=pd.read_csv(p/'recuperacao.csv');r=r[r.relevantes.notna()]
print('Recall macro@1:',r.recall1.mean(),'Recall macro@3:',r.recall3.mean(),'casos com gabarito:',len(r))
d.set_index('configuracao')[['recusas_rotulo_consta','recusas_rotulo_nao_consta']].plot.bar(title='Recusas por rótulo — amostra adicional interna',rot=0,ylabel='Número de casos');plt.show()
print('Fontes estruturais não comprovam suporte semântico; revisão humana pendente.')
'''
nb=nbf.v4.new_notebook(cells=[nbf.v4.new_markdown_cell('# Avaliação adicional interna\n\nCasos criados pelo projeto; não representam avaliação humana independente.'),nbf.v4.new_code_cell(code)],metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}})
NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
nbf.write(nb,root/'notebooks/07_amostra_adicional.ipynb');print('Notebook executado.')
