import json
from pathlib import Path
p=Path('avaliacao/resultados/auditoria_dependencias.json');d=json.loads(p.read_text(encoding='utf8'));print('dependências:',len(d['dependencies']),'vulnerabilidades:',sum(len(x['vulns']) for x in d['dependencies']),'serviço:',d.get('fixes'))
