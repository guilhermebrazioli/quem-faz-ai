"""Auditoria local de entrega: presença não comprova mérito acadêmico."""
import argparse,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from fastapi.testclient import TestClient
from src.api import app
parser=argparse.ArgumentParser();parser.add_argument('--testes',action='store_true');args=parser.parse_args()
results=[]
def check(label,condition,detail=''):
 status='PASSOU' if condition else 'FALHOU';results.append((status,label));print(f'{status}: {label}'+(f' — {detail}' if detail else ''))
def manual(label):results.append(('REQUER VERIFICAÇÃO MANUAL',label));print('REQUER VERIFICAÇÃO MANUAL:',label)
required=['README.md','ENTREGA_FINAL.md','COMANDOS_PUBLICACAO.md','requirements.txt','.gitignore','.env.example','src/api.py','src/agente.py','src/retrieval.py','base/trechos.json','avaliacao/casos_teste.json','avaliacao/casos_internos_adicionais.json','avaliacao/resultados/cega_v2/geracao.jsonl','avaliacao/resultados/cega_v2/pre_revisao_automatica.jsonl','avaliacao/resultados/adicional_v1/placar.csv','avaliacao/resultados/adicional_v2/placar.csv','avaliacao/pre_revisao_automatica.py','avaliacao/comparacao_erros_v8.md','docs/RELATORIO_FINAL_GENERATIVE_AI.md','docs/arquitetura.md','exemplos/consumidor.py']
missing=[p for p in required if not (ROOT/p).is_file()]
check('Arquivos necessários',not missing,', '.join(missing))
rubric={'tarefa e gabarito':'avaliacao/casos_teste.json','base e fontes':'base/trechos.json','recuperação':'avaliacao/resultados/adicional_v2/recuperacao.csv','geração e recusa':'avaliacao/resultados/adicional_v2/geracao.jsonl','agente':'src/agente.py','placar':'avaliacao/resultados/adicional_v2/placar.csv','cinco erros':'avaliacao/comparacao_erros_v8.md','reprodutibilidade':'README.md'}
check('Arquivos de evidência dos oito critérios',all((ROOT/p).is_file() for p in rubric.values()),'presença não comprova avaliação acadêmica')
try:
 base=json.loads((ROOT/'base/trechos.json').read_text(encoding='utf8')); ids=[x['id'] for x in base]
 check('Base e metadados',len(ids)==len(set(ids)) and all(x.get('url','').startswith('https://') and x.get('texto') for x in base),f'{len(ids)} trechos')
except Exception as e:check('Base e metadados',False,str(e))
try:
 response=TestClient(app).get('/openapi.json'); spec=response.json();check('Contrato da API',response.status_code==200 and '/api/ai/assistente' in spec['paths'] and 'post' in spec['paths']['/api/ai/assistente'])
except Exception as e:check('Contrato da API',False,str(e))
notebooks=list((ROOT/'notebooks').glob('*.ipynb')); bad=[]
for p in notebooks:
 try:
  nb=json.loads(p.read_text(encoding='utf8'));code=[x for x in nb['cells'] if x['cell_type']=='code'];
  if not code or any(c.get('execution_count') is None or not c.get('outputs') for c in code):bad.append(p.name)
 except Exception:bad.append(p.name)
check('Notebooks com saídas',len(notebooks)>=6 and not bad,', '.join(bad) if bad else str(len(notebooks)))
links=[]
for p in [ROOT/'README.md',ROOT/'ENTREGA_FINAL.md',ROOT/'COMANDOS_PUBLICACAO.md',ROOT/'docs/RELATORIO_FINAL_GENERATIVE_AI.md']:
 if not p.exists():continue
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
  if target.startswith(('http://','https://','#')):continue
  if not (p.parent/target.split('#')[0]).exists():links.append(f'{p.name}: {target}')
check('Links relativos principais',not links,', '.join(links))
patterns=[re.compile('sk-'+'[A-Za-z0-9]{20,}'),re.compile('-----BEGIN '+'(?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]
found=[];skip={'.venv','.git','__pycache__','.pytest_cache'}
for p in ROOT.rglob('*'):
 if not p.is_file() or any(x in skip for x in p.relative_to(ROOT).parts) or p.suffix.lower() not in {'.py','.md','.json','.jsonl','.csv','.txt','.env','.ipynb'} or p.stat().st_size>10_000_000:continue
 if p.name=='mapa_segunda_revisao.json':continue
 try:
  content=p.read_text(encoding='utf-8-sig')
  if any(pat.search(content) for pat in patterns):found.append(str(p.relative_to(ROOT)))
 except UnicodeError:pass
check('Padrões básicos de credenciais',not found,', '.join(found))
check('Arquivo .env não presente',not (ROOT/'.env').exists())
proc=subprocess.run([sys.executable,'-m','avaliacao.executar_adicional','--help'],cwd=ROOT,text=True,capture_output=True)
check('Comando básico do experimento',proc.returncode==0)
if args.testes:
 proc=subprocess.run([sys.executable,'-m','pytest','-q'],cwd=ROOT,text=True,capture_output=True)
 check('Testes automatizados',proc.returncode==0,proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else proc.stderr[-200:])
else:manual('Executar pytest -q ou chamar este script com --testes.')
manual('Conferir suporte semântico, correção, alucinação e adequação das recusas por avaliador independente.')
manual('Conferir rubrica, licenças, segurança, proteção de dados, nomes e RMs antes da publicação.')
manual('Comprovar integração com o MVP real; o projeto contém apenas demonstração local.')
print('\nResumo:',{s:sum(x[0]==s for x in results) for s in ['PASSOU','FALHOU','REQUER VERIFICAÇÃO MANUAL']})
sys.exit(1 if any(s=='FALHOU' for s,_ in results) else 0)
