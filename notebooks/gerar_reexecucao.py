from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient
root=Path(__file__).resolve().parent.parent
code='''from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
root=Path.cwd()
a=pd.read_csv(root/'avaliacao/resultados/cega_v1/placar.csv');a['rodada']='v1: prompt com caracteres corrompidos'
b=pd.read_csv(root/'avaliacao/resultados/cega_v2/placar.csv');b['rodada']='v2: prompt corrigido, mesmos casos'
d=pd.concat([a,b],ignore_index=True)
display(d[['rodada','configuracao','total','json_valido','respostas_fontes_ids_validos','recusas_rotulo_consta','recusas_rotulo_nao_consta','latencia_media_s']])
x=d[d.configuracao.isin(['B','C'])].pivot(index='configuracao',columns='rodada',values='recusas_rotulo_consta')
x.plot.bar(title='Recusas nos 14 casos rotulados respondíveis',ylim=(0,14),rot=0);plt.show()
print('A segunda rodada reutiliza perguntas já observadas e não é um teste novo independente.')
'''
nb=nbf.v4.new_notebook(cells=[nbf.v4.new_markdown_cell('# Reexecução após correção de codificação\n\nAs duas execuções foram preservadas. Avaliação humana continua pendente.'),nbf.v4.new_code_cell(code)],metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}})
NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
nbf.write(nb,root/'notebooks/06_reexecucao.ipynb');print('Notebook executado.')
