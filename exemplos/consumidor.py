"""Consumidor de demonstração: executa contra API local já iniciada."""
import json
import httpx

payload={'descricao':'O orçamento precisa conter condições de pagamento e datas?', 'configuracao':'C'}
response=httpx.post('http://127.0.0.1:8000/api/ai/assistente',json=payload,timeout=240)
response.raise_for_status()
print(json.dumps(response.json(),ensure_ascii=False,indent=2))
