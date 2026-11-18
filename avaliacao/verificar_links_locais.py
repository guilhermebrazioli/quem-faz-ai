import re
from pathlib import Path
paths=[Path('README.md'),Path('docs/RELATORIO_FINAL_GENERATIVE_AI.md'),Path('docs/CHECKLIST_ENTREGA.md')]
errors=[]
for p in paths:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
  if target.startswith(('https://','http://','#')):continue
  resolved=(p.parent/target.split('#')[0]).resolve()
  if not resolved.exists():errors.append((str(p),target))
print('Links relativos quebrados:',errors)
