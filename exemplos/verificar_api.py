import json, subprocess, sys, time
import httpx
server=subprocess.Popen([sys.executable,'-m','uvicorn','src.api:app','--host','127.0.0.1','--port','18761'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
 for _ in range(100):
  try:
   if httpx.get('http://127.0.0.1:18761/health',timeout=1).status_code==200: break
  except httpx.HTTPError: pass
  time.sleep(.1)
 with httpx.Client(timeout=240) as client:
  r=client.post('http://127.0.0.1:18761/api/ai/assistente',json={'descricao':'O orçamento precisa conter condições de pagamento e datas?', 'configuracao':'C'})
  data=r.json(); assert r.status_code==200
  print('HTTP',r.status_code,'status',data['status'])
finally:
 server.terminate();server.wait(timeout=10)
