import os,subprocess,sys
from pathlib import Path
cmd=[sys.executable,'scripts/verificar_entrega.py','--testes']
r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8',errors='replace',env={**os.environ,'PYTHONIOENCODING':'utf-8'})
out=Path('avaliacao/resultados/auditoria_entrega_final.txt')
if out.exists():raise SystemExit('Arquivo existente; não sobrescrever.')
out.write_text(r.stdout+'\nAvisos:\n'+r.stderr,encoding='utf8')
print(r.stdout);print('Código:',r.returncode)
if r.returncode:raise SystemExit(r.returncode)
