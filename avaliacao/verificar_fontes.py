import httpx,json
from pathlib import Path
base=json.loads(Path('base/trechos.json').read_text(encoding='utf8')); urls={x['documento']:x['url'] for x in base}; results=[]
with httpx.Client(follow_redirects=True,timeout=20) as client:
 for id,url in urls.items():
  try:
   r=client.get(url);results.append({'documento':id,'url':url,'status':r.status_code,'url_final':str(r.url)})
  except httpx.HTTPError as exc:results.append({'documento':id,'url':url,'erro':str(exc)})
Path('avaliacao/resultados/fontes_http_v7.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
print([(x['documento'],x.get('status','erro')) for x in results])
