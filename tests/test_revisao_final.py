import csv,json,shutil
from fastapi.testclient import TestClient
from avaliacao import revisao_web

def test_revisao_percorre_60_respostas_sem_revelar_configuracao(monkeypatch,tmp_path):
    path=tmp_path/'revisao.csv'
    shutil.copyfile('avaliacao/resultados/cega_v2/revisao_humana.csv',path)
    monkeypatch.setattr(revisao_web,'PATH',path)
    client=TestClient(revisao_web.app)
    for i in range(60):
        page=client.get('/',params={'i':i})
        assert page.status_code==200
        assert 'configuração oculta' in page.text
        assert 'adequacao_recusa' in page.text
        assert 'rastreio' not in page.text
    _,rows=revisao_web.read()
    assert len(revisao_web.order(rows))==len(set(revisao_web.order(rows)))==60

def test_recusa_pode_ser_registrada_sem_modificar_outros_casos(monkeypatch,tmp_path):
    path=tmp_path/'revisao.csv'
    shutil.copyfile('avaliacao/resultados/cega_v2/revisao_humana.csv',path)
    monkeypatch.setattr(revisao_web,'PATH',path)
    client=TestClient(revisao_web.app)
    response=client.post('/salvar',data={'i':'0','adequacao_recusa':'indevida','observacoes_revisor':'exemplo de teste'})
    assert response.status_code==200
    with path.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    assert sum(row['adequacao_recusa']=='indevida' for row in rows)==1

def test_exportacao_remove_identidade_e_preserva_pendencias(tmp_path):
    import subprocess,sys
    out=tmp_path/'copia.csv'; mapping=tmp_path/'mapa.json'
    subprocess.run([sys.executable,'-m','avaliacao.exportar_segunda_revisao','avaliacao/resultados/cega_v2/revisao_humana.csv','--saida',str(out),'--mapa',str(mapping)],check=True,capture_output=True)
    with out.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    refs=json.loads(mapping.read_text(encoding='utf8'))
    assert len(rows)==len(refs)==60
    assert all(row['configuracao']=='oculta' and row['id'] in refs for row in rows)
    assert all(not row['adequacao_recusa'] and not row['correcao_humana'] for row in rows)
    for row in rows:
        response=json.loads(row['resposta'])
        assert 'rastreio' not in response and response.get('status')!='sem_contexto'
