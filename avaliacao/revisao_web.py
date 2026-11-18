"""Revisão manual local. Nenhuma avaliação é atribuída sem envio explícito."""
import csv, hashlib, html, json, os
from pathlib import Path
from urllib.parse import parse_qs
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

app=FastAPI(title='Revisão humana Quem Faz AI')
DEFAULT=Path('avaliacao/resultados/v6/execucao_final/revisao_humana.csv')
PATH=Path(os.getenv('REVISAO_CSV',str(DEFAULT))).resolve()
FIELDS=['correcao_humana','fundamentacao_humana','alucinacao_humana','adequacao_recusa']
OPTIONS={'correcao_humana':['','correta','parcial','incorreta','nao_avaliavel'], 'fundamentacao_humana':['','sustentada','parcial','nao_sustentada','nao_aplicavel'], 'alucinacao_humana':['','sim','nao','nao_avaliavel'], 'adequacao_recusa':['','adequada','indevida','nao_aplicavel','nao_avaliavel']}
def read():
    with PATH.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);rows=list(reader);return reader.fieldnames,rows

def esc(s): return html.escape(str(s or ''))
def anonymous_response(raw):
    try:
        result=json.loads(raw)
        if isinstance(result,dict):
            result.pop('rastreio',None)
            if result.get('status') in ('sem_contexto','fundamentado'):
                result['status']='resposta'
        return json.dumps(result,ensure_ascii=False,indent=2)
    except (TypeError,ValueError):
        return raw

def order(rows):
    # Stable pseudorandom order prevents the usual A/B/C sequence revealing labels.
    return sorted(range(len(rows)),key=lambda i:hashlib.sha256(f"{i}:{rows[i].get('id')}:{rows[i].get('configuracao')}".encode()).hexdigest())
def widget(name,current):
    opts=''.join(f'<option value="{esc(v)}"'+(' selected' if v==current else '')+'>'+esc(v or 'Pendente')+'</option>' for v in OPTIONS[name])
    return f'<label>{esc(name)} <select name="{name}">{opts}</select></label><br>'

@app.get('/',response_class=HTMLResponse)
def page(i:int=0):
    try: _,rows=read()
    except (OSError,csv.Error): raise HTTPException(500,'Não foi possível abrir o arquivo de revisão.')
    if not rows: raise HTTPException(404,'Arquivo sem registros.')
    i=max(0,min(i,len(rows)-1));index=order(rows)[i];r=rows[index]
    blocks=''.join(f'<h3>{esc(label)}</h3><pre>{esc(anonymous_response(r.get(key)) if key=="resposta" else r.get(key))}</pre>' for label,key in [('Pergunta','pergunta'),('Gabarito','gabarito'),('Resposta e citações','resposta'),('Documentos recuperados','evidencias_recuperadas'),('Critério','criterio')])
    selects=''.join(widget(k,r.get(k,'')) for k in FIELDS)
    return f'''<!doctype html><html lang="pt-br"><meta charset="utf-8"><title>Revisão humana</title>
<style>body{{font:16px sans-serif;max-width:1000px;margin:2em auto;padding:0 1em}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f4f4;padding:1em}} label{{display:block;margin:.7em}} textarea{{width:95%;height:8em}}</style>
<h1>Revisão humana</h1><p>Resposta {i+1}/{len(rows)} — configuração oculta</p>
<p>Arquivo: {esc(PATH.name)}. Os campos vazios permanecem pendentes.</p>{blocks}
<form method="post" action="/salvar"><input type="hidden" name="i" value="{i}">{selects}<label>Justificativa<br><textarea name="observacoes_revisor">{esc(r.get('observacoes_revisor',''))}</textarea></label><br><button>Salvar avaliação</button></form>
<p><a href="/?i={max(0,i-1)}">Anterior</a> | <a href="/?i={min(len(rows)-1,i+1)}">Próximo</a></p></html>'''

@app.post('/salvar')
async def save(request:Request):
    form=parse_qs((await request.body()).decode('utf8'),keep_blank_values=True)
    try:
        i=int(form['i'][0]); headers,rows=read()
        if i < 0 or i >= len(rows): raise IndexError
        row=rows[order(rows)[i]]
    except (KeyError,ValueError,IndexError,OSError): raise HTTPException(400,'Registro inválido')
    for field in FIELDS:
        if field not in headers: headers.append(field)
    for field in FIELDS:
        val=form.get(field,[''])[0]
        if val not in OPTIONS[field]: raise HTTPException(400,'Valor de avaliação inválido')
        row[field]=val
    note=form.get('observacoes_revisor',[''])[0].strip()
    if any(row[k] for k in FIELDS) and not note: raise HTTPException(400,'Informe a justificativa da avaliação.')
    row['observacoes_revisor']=note
    # A local browser action is the sole writer; replace atomically after completing the CSV.
    tmp=PATH.with_name(PATH.name+'.tmp')
    with tmp.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=headers);writer.writeheader();writer.writerows(rows)
    tmp.replace(PATH)
    return RedirectResponse('/?i='+str(i),status_code=303)
