# Publicação no GitHub

A publicação é realizada pelo responsável. Os comandos abaixo pressupõem um repositório remoto vazio e que esta pasta não é atualmente um repositório Git. Não foram executados automaticamente.

1. Confirme com os integrantes a divulgação pública de nomes e RMs. A revisão humana, a conferência das fontes e a avaliação das limitações continuam necessárias.
2. Crie o repositório vazio no GitHub, sem adicionar README, licença ou `.gitignore` pelo site.
3. No PowerShell, na pasta do projeto, substitua a URL e execute:

```powershell
git init
git add .
git status --short
# Inspecione a lista e o conteúdo antes de criar o commit.
git diff --cached --stat
git commit -m "Entrega acadêmica Quem Faz AI"
git branch -M main
git remote add origin https://github.com/USUARIO/REPOSITORIO.git
git push -u origin main
```

`.venv/`, caches, `.env` e o mapa local da segunda revisão estão no `.gitignore`. Confirme também que não há credenciais, dados reais de clientes, modelos pesados ou arquivos locais inesperados no staging. Se já houver repositório ou remoto configurado, inspecione `git status` e `git remote -v` antes de executar qualquer comando e adapte o procedimento.

Depois da publicação, abra o README, relatório, notebooks e arquivos de evidência no GitHub; confira links relativos, renderização de tabelas e Mermaid, permissões e conteúdo. Adicione a URL do repositório ou vídeo ao relatório somente quando existirem. Não inclua o mapa da revisão com o material enviado ao segundo avaliador.
