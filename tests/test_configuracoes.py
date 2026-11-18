import json
from src import core

def fake_ollama(monkeypatch, content):
    """Substitui o Ollama por uma resposta fixa e guarda o payload enviado."""
    sent={}
    class R:
        def raise_for_status(self): pass
        def json(self): return {'message':{'content':json.dumps(content,ensure_ascii=False)}}
    class Client:
        def __init__(self,**kwargs): pass
        def __enter__(self): return self
        def __exit__(self,*args): pass
        def post(self,url,json=None): sent.update(json); return R()
    monkeypatch.setattr(core.httpx,'Client',Client)
    return sent

PEDIDO='orçamento condições de pagamento datas'

def test_rag_simples_gera_texto_proprio_com_citacao(monkeypatch):
    sent=fake_ollama(monkeypatch,{'categoria_sugerida':'reforma','descricao_aprimorada':PEDIDO,
        'orientacoes':[{'texto':'Peça orçamento com valores e datas discriminados.','fontes':['CDC-01']}],'perguntas_sugeridas':[]})
    out=core.generate(core.Input(descricao=PEDIDO,configuracao='B'))
    original=next(x['texto'] for x in core.BASE if x['id']=='CDC-01')
    assert out.status=='fundamentado'
    assert out.orientacoes[0].texto!=original          # B gera texto, não copia o trecho
    assert [f['id'] for f in out.fontes]==['CDC-01']
    assert 'CDC-01' in sent['messages'][1]['content']   # contexto recuperado foi enviado
    assert 'valida_citacoes' not in out.rastreio        # B não verifica citações

def test_rag_simples_nao_bloqueia_citacao_inventada(monkeypatch):
    fake_ollama(monkeypatch,{'categoria_sugerida':'reforma','descricao_aprimorada':PEDIDO,
        'orientacoes':[{'texto':'Afirmação sem suporte.','fontes':['INVENTADA']}],'perguntas_sugeridas':[]})
    out=core.generate(core.Input(descricao=PEDIDO,configuracao='B'))
    assert out.status=='fundamentado' and out.fontes==[]  # fragilidade do RAG simples, medida no placar
    assert out.orientacoes[0].fontes==['INVENTADA']

def test_rag_simples_recusa_sem_evidencia_acima_do_limiar(monkeypatch):
    def never(**kwargs): raise AssertionError('não deveria chamar a LLM')
    monkeypatch.setattr(core.httpx,'Client',never)
    out=core.generate(core.Input(descricao='Xilofone quasar galáxia',configuracao='B'))
    assert out.status=='informacao_insuficiente' and 'sem_evidencia' in out.rastreio

def test_rag_simples_json_fora_do_contrato_recusa(monkeypatch):
    fake_ollama(monkeypatch,{'qualquer':'coisa'})
    out=core.generate(core.Input(descricao=PEDIDO,configuracao='B'))
    assert out.status=='informacao_insuficiente' and 'json_invalido' in out.rastreio

def test_sem_contexto_nao_consulta_base(monkeypatch):
    sent=fake_ollama(monkeypatch,{'categoria_sugerida':'x','descricao_aprimorada':PEDIDO,
        'orientacoes':[{'texto':'Resposta livre.','fontes':[]}],'perguntas_sugeridas':[]})
    out=core.generate(core.Input(descricao=PEDIDO,configuracao='A'))
    assert out.status=='sem_contexto' and out.fontes==[]
    assert 'sem contexto' in sent['messages'][1]['content']

def test_rag_simples_normaliza_formato_do_id(monkeypatch):
    fake_ollama(monkeypatch,{'categoria_sugerida':'reforma','descricao_aprimorada':PEDIDO,
        'orientacoes':[{'texto':'Discriminar valores e datas.','fontes':['Fonte 1: CDC-01']}],'perguntas_sugeridas':[]})
    out=core.generate(core.Input(descricao=PEDIDO,configuracao='B'))
    assert out.orientacoes[0].fontes==['CDC-01'] and [f['id'] for f in out.fontes]==['CDC-01']
