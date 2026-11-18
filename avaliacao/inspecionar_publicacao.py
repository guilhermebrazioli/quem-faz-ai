from pathlib import Path
skip={'.venv','.git','.pytest_cache','__pycache__'}
files=[]
for p in Path('.').rglob('*'):
 if p.is_file() and not any(x in skip for x in p.parts) and p.name!='mapa_segunda_revisao.json':files.append((p.stat().st_size,p.as_posix()))
print('Arquivos revisáveis:',len(files),'tamanho total MB:',round(sum(x[0] for x in files)/1e6,2))
for size,path in sorted(files,reverse=True)[:5]:print(round(size/1e6,2),'MB',path)
