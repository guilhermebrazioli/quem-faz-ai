import json,subprocess,sys,time
from pathlib import Path
import os
import argparse
import httpx
parser=argparse.ArgumentParser();parser.add_argument('--saida');args=parser.parse_args()
if args.saida and Path(args.saida).exists():raise SystemExit('Saída existente; escolha outro arquivo.')
p=subprocess.Popen([sys.executable,'-m','uvicorn','src.api:app','--host','127.0.0.1','--port','8000'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
 for _ in range(100):
  if p.poll() is not None:raise RuntimeError('Porta 8000 indisponível ou servidor não iniciou.')
  try:
   if httpx.get('http://127.0.0.1:8000/health',timeout=.5).status_code==200:break
  except httpx.HTTPError:time.sleep(.1)
 else:raise RuntimeError('Servidor não iniciou')
 run=subprocess.run([sys.executable,'exemplos/consumidor.py'],capture_output=True,encoding='utf8',errors='strict',timeout=240,env={**os.environ,'PYTHONIOENCODING':'utf-8'})
 if run.returncode:raise RuntimeError(run.stderr)
 data=json.loads(run.stdout)
 if args.saida:Path(args.saida).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
 print('Cliente demonstrativo -> API HTTP -> Ollama:',data['status'],'fontes:',len(data['fontes']))
finally:p.terminate();p.wait(timeout=10)
