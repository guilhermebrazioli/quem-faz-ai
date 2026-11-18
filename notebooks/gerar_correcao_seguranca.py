from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient
root=Path(__file__).resolve().parent.parent
code='''from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
root=Path.cwd()
a=pd.read_csv(root/'avaliacao/resultados/adicional_v1/placar.csv');a['versao']='antes do filtro em B'
b=pd.read_csv(root/'avaliacao/resultados/adicional_v2/placar.csv');b['versao']='depois do filtro em B'
d=pd.concat([a,b]);display(d[['versao','configuracao','total','json_valido','respostas_fontes_ids_validos','recusas_rotulo_consta','recusas_rotulo_nao_consta','latencia_media_s']])
d[d.configuracao.isin(['B','C'])].pivot(index='configuracao',columns='versao',values='recusas_rotulo_consta').plot.bar(rot=0,ylim=(0,10),title='Recusas em casos consta: reexecução exploratória');plt.show()
print('As duas versões usam as mesmas perguntas; o resultado não é uma nova avaliação independente.')
'''
nb=nbf.v4.new_notebook(cells=[nbf.v4.new_markdown_cell('# Comparação após correção de segurança\n\nA alteração foi motivada por auditoria de código; a segunda execução reutiliza os casos.'),nbf.v4.new_code_cell(code)],metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}})
NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute();nbf.write(nb,root/'notebooks/08_correcao_seguranca.ipynb');print('Notebook executado')
