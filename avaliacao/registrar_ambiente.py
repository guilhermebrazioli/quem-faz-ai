import hashlib,json,platform,subprocess
from datetime import datetime
from pathlib import Path
import httpx
model=httpx.get('http://127.0.0.1:11434/api/tags',timeout=5).json()['models']
match=next((x for x in model if x['name']=='qwen2.5:1.5b'),None)
paths={'inicial':'avaliacao/resultados/geracao.jsonl','v6':'avaliacao/resultados/v6/execucao_final/geracao.jsonl','primeira_nova':'avaliacao/resultados/cega_v1/geracao.jsonl','reexecucao_corrigida':'avaliacao/resultados/cega_v2/geracao.jsonl'}
summary={'modelo':match,'ollama_versao':subprocess.check_output(['ollama','--version'],text=True).strip(),'python':platform.python_version(),'sistema':platform.platform(),'processador':platform.processor(),'parametros':{'temperature':0,'seed':42,'num_predict_baseline':450,'num_predict_rag_agente':120,'limiar':0.15},'observacao_datas':'Datas de modificação dos arquivos no relógio local do sistema; servem como vestígio e podem ser alteradas ao copiar arquivos, não provam o horário de inferência.', 'execucoes':{k:{'arquivo':p,'modificado_local':datetime.fromtimestamp(Path(p).stat().st_mtime).isoformat(timespec='seconds'),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()} for k,p in paths.items()},'manifesto':'avaliacao/congelamento_cega_v2.json','dependencias':'requirements.txt e docs/dependencias_ambiente.txt'}
Path('docs/manifesto_experimentos.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
