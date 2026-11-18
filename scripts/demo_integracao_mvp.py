"""Integração somente leitura: lê as categorias do MVP Quem Faz publicado e consulta o assistente local."""
import argparse
import json
import sys
import unicodedata
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from src.core import Input, generate  # noqa: E402

MVP_PADRAO = "https://quem-faz.whiteocean-1daba118.eastus.azurecontainerapps.io"
CASOS = [
    ("eletric", "Antes de contratar um serviço elétrico, quais cuidados de segurança devo considerar?"),
    ("pintur", "Antes da reforma, quais itens financeiros e datas devem ser discriminados no orçamento?"),
]


def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    return sem_acento.lower()


def ler_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "quem-faz-ai-demo"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode("utf-8"))


def nome_categoria(item):
    if isinstance(item, dict):
        return item.get("nome") or item.get("name")
    return str(item)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mvp-url", default=MVP_PADRAO)
    p.add_argument("--configuracao", default="B", choices=["A", "B", "C"])
    p.add_argument("--saida", default="avaliacao/resultados/integracao_mvp.json")
    a = p.parse_args()

    base = a.mvp_url.rstrip("/")
    categorias = [n for n in (nome_categoria(c) for c in ler_json(f"{base}/api/categorias")) if n]
    solicitacoes = ler_json(f"{base}/api/solicitacoes")

    resultados = []
    for chave, pergunta in CASOS:
        categoria = next((c for c in categorias if chave in normalizar(c)), None)
        resposta = generate(Input(descricao=pergunta, categoria=categoria, configuracao=a.configuracao))
        resultados.append({
            "categoria_mvp": categoria,
            "descricao": pergunta,
            "configuracao": a.configuracao,
            "resposta": resposta.model_dump(),
        })
        print(f"[{categoria}] status={resposta.status} categoria_sugerida={resposta.categoria_sugerida}")

    registro = {
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "mvp_url": base,
        "modo": "somente leitura (GET /api/categorias e GET /api/solicitacoes); nada é gravado no MVP",
        "categorias_mvp": categorias,
        "solicitacoes_mvp_total": len(solicitacoes) if isinstance(solicitacoes, list) else None,
        "resultados": resultados,
        "limitacao": "O assistente roda localmente com Ollama; o MVP publicado não exibe as respostas.",
    }
    saida = RAIZ / a.saida
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Categorias lidas do MVP: {len(categorias)} | salvo em {a.saida}")


if __name__ == "__main__":
    main()
