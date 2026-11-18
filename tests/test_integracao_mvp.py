import importlib.util
from pathlib import Path

_caminho = Path(__file__).resolve().parents[1] / "scripts" / "demo_integracao_mvp.py"
_spec = importlib.util.spec_from_file_location("demo_integracao_mvp", _caminho)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


def test_normalizar_remove_acentos():
    assert mod.normalizar("Elétrica") == "eletrica"


def test_nome_categoria_aceita_dict_e_texto():
    assert mod.nome_categoria({"nome": "Pintura"}) == "Pintura"
    assert mod.nome_categoria("Limpeza") == "Limpeza"
