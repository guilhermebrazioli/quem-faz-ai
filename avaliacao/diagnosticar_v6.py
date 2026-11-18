import importlib.util,json,time
from pathlib import Path
import httpx
from src import core
spec=importlib.util.spec_from_file_location('agente_v6',Path('avaliacao/snapshots/v6/agente.py'))
agente=importlib.util.module_from_spec(spec);spec.loader.exec_module(agente)
cases=json.loads(Path('avaliacao/casos_teste.json').read_text(encoding='utf8'))
selected=[x for x in cases if x['particao']=='final' and x['disponibilidade']=='consta']
p=Path('avaliacao/resultados/diagnostico_v6/reexecucao.jsonl')
if p.exists(): raise SystemExit('Diagnóstico já existe; preserve-o antes de outra execução.')
with p.open('w',encoding='utf8') as f:
 for case in selected:
  calls=[]
  def monitored(system,user,schema,url,model):
   body={'model':model,'stream':False,'format':schema.model_json_schema(),'options':{'temperature':0,'seed':42,'num_predict':120},'messages':[{'role':'system','content':system},{'role':'user','content':user}]}
   with httpx.Client(timeout=240) as client:
    response=client.post(url+'/api/chat',json=body);response.raise_for_status();raw=response.json()['message']['content']
   try: parsed=schema.model_validate_json(raw); err='ok'
   except Exception: parsed=None;err='json_ou_esquema_invalido'
   calls.append({'schema':schema.__name__,'contexto_exato':user,'prompt_sistema':system,'resposta_bruta':raw,'validacao':err})
   return parsed,err
  original=agente.chat; agente.chat=monitored
  try:
   start=time.perf_counter();result=agente.run(core.Input(descricao=case['pergunta'],configuracao='C'),core.BASE,.15,core.URL,core.MODEL,core.Response,core.Claim,core.refusal).model_dump();duration=time.perf_counter()-start
  finally:agente.chat=original
  retrieval=agente.rank(case['pergunta'],core.BASE)
  row={'id':case['id'],'pergunta':case['pergunta'],'gabarito':case['esperado'],'ids_gabarito':case['chunks_relevantes'],'recuperacao':retrieval,'limiar':.15,'aceitos':[x['id'] for x in retrieval if x['score']>=.15],'chamadas':calls,'resultado':result,'latencia_s':duration}
  f.write(json.dumps(row,ensure_ascii=False)+'\n');f.flush();print(case['id'],result['status'],result['rastreio'][-1],flush=True)
