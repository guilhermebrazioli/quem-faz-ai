from pathlib import Path
p=Path('avaliacao/executar_cega.py');s=p.read_text(encoding='utf8')
s=s.replace("default='avaliacao/resultados/cega_v1'","default='avaliacao/resultados/adicional_v1'").replace("default='avaliacao/congelamento_cega_v2.json'","default='avaliacao/congelamento_adicional.json'").replace("Path('avaliacao/casos_cegos_v1.json')","Path('avaliacao/casos_internos_adicionais.json')")
Path('avaliacao/executar_adicional.py').write_text(s,encoding='utf8')
p=Path('avaliacao/consolidar_cega.py');s=p.read_text(encoding='utf8').replace("default='avaliacao/resultados/cega_v1'","default='avaliacao/resultados/adicional_v1'").replace("Path('avaliacao/casos_cegos_v1.json')","Path('avaliacao/casos_internos_adicionais.json')")
Path('avaliacao/consolidar_adicional.py').write_text(s,encoding='utf8')
