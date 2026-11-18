import json,subprocess,sys,time
from pathlib import Path
import argparse
import httpx
parser=argparse.ArgumentParser();parser.add_argument('--saida');args=parser.parse_args()
if args.saida and Path(args.saida).exists():raise SystemExit('Saída existente; escolha outro arquivo.')
server=subprocess.Popen([sys.executable,'-m','uvicorn','src.api:app','--host','127.0.0.1','--port','18762'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
 for attempt in range(100):
  try:
   if httpx.get('http://127.0.0.1:18762/health',timeout=1).status_code==200:break
  except httpx.HTTPError:pass
  time.sleep(.1)
 else:raise RuntimeError('Servidor não iniciou')
 case=json.loads(Path('avaliacao/casos_teste.json').read_text(encoding='utf8'))[17]
 response=httpx.post('http://127.0.0.1:18762/api/ai/assistente',json={'descricao':case['pergunta'],'configuracao':'C'},timeout=240)
 response.raise_for_status(); result={'http_status':response.status_code,'resposta':response.json()}
 if args.saida:Path(args.saida).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 print('API HTTP',response.status_code,'status',response.json()['status'])
finally:
 server.terminate();server.wait(timeout=10)
