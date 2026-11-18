import os,subprocess,sys
from pathlib import Path
r=subprocess.run([sys.executable,'scripts/verificar_entrega.py','--testes'],capture_output=True,text=True,encoding='utf8',errors='replace',env={**os.environ,'PYTHONIOENCODING':'utf-8'})
p=Path('avaliacao/resultados/auditoria_entrega_v10.txt')
if p.exists():raise SystemExit('Arquivo existente; preservado.')
p.write_text(r.stdout+'\nAvisos:\n'+r.stderr,encoding='utf8')
print(r.stdout)
if r.returncode:raise SystemExit(r.returncode)
