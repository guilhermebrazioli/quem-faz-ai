from fastapi import FastAPI, HTTPException
import httpx
from src.core import Input, Response, generate
app = FastAPI(title='Quem Faz AI', version='0.1.0')
@app.get('/health')
def health(): return {'status':'ok'}
@app.post('/api/ai/assistente',response_model=Response)
def assistente(request: Input):
    try: return generate(request)
    except (httpx.HTTPError, KeyError) as exc: raise HTTPException(503, 'Modelo local indisponível ou resposta inválida') from exc
