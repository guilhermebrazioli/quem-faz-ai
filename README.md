# Quem Faz AI

Prova de conceito local de assistência à contratação consciente para o Quem Faz, plataforma que conecta contratantes a prestadores de serviço, inicialmente na cidade de São Paulo. O assistente recebe a descrição de um pedido e devolve orientações para o contratante verificar antes de contratar, fundamentadas em uma base de trechos de fontes públicas (Código de Defesa do Consumidor, Procon-SP, Ministério de Minas e Energia e IPS-ES). Quando a base não sustenta uma resposta, ele recusa (`informacao_insuficiente`).

A plataforma não garante a qualidade dos serviços, e a decisão de contratar é do usuário. Este protótipo não deve ser usado em produção nem em situações de emergência.

Integrantes: Enzo Vazquez Sartorelli (RM94618), Kaue Pastori Teixeira (RM98501), Nicolas Nogueira Boni (RM551965), Guilherme Brazioli (RM98237) e Pedro Oliveira Valotto (RM551445).

## Ficha técnica do MVP — Quem Faz

### 1. Nome do produto

**Quem Faz** — Plataforma de conexão entre contratantes e prestadores de serviços.

### 2. Cidadão e território

Moradores, empresas e profissionais prestadores de serviços da cidade de **São Paulo (SP)**.

### 3. Problema, em uma frase

A dificuldade de encontrar profissionais adequados e confiáveis para a contratação de serviços, enquanto prestadores enfrentam obstáculos para divulgar suas habilidades e conquistar novos clientes.

### 4. Proposta de valor

O Quem Faz propõe uma plataforma que aproxima contratantes e prestadores de serviços por meio da exploração de categorias profissionais e da publicação de solicitações. Os usuários poderão consultar perfis, solicitar propostas e avaliar experiências após a conclusão dos serviços.

No módulo de Generative AI, o Quem Faz AI apoia a contratação segura: responde dúvidas sobre orçamento, direitos do consumidor e riscos elétricos residenciais citando fontes públicas, e recusa quando a base não contém a resposta.

### 5. Arquitetura: componentes

- **API:** FastAPI local, com o endpoint `POST /api/ai/assistente`.
- **Busca:** TF-IDF com radicalização em português e limiar de 0,15 sobre `base/trechos.json`.
- **Geração:** Qwen 2.5 1.5B via Ollama, com resposta em JSON validada e IDs das fontes citadas.
- **Configurações comparadas:** A (LLM sem contexto), B (RAG simples) e C (agente).
- **Integração:** leitura somente por GET das categorias do MVP publicado.

**Fluxo:** Pergunta → API → Busca na base → LLM local → JSON com fontes ou recusa.

### 6. Fontes de dados

15 trechos parafraseados de 4 fontes públicas: Senacon/CDC, Ministério de Minas e Energia, Procon-SP e IPS-ES (acesso em 17/11/2026). A avaliação usa 20 casos cegos: 14 com resposta na base e 6 "não consta". Nenhum dado pessoal real.

### 7. Modelos de IA utilizados

Qwen 2.5 1.5B executado localmente pelo Ollama, com temperatura 0. Especialização por agente (configuração C), sem LoRA nem fine-tuning dos pesos.

### 8. URL do MVP e repositório

- **MVP público:** https://quem-faz.whiteocean-1daba118.eastus.azurecontainerapps.io/
- **Repositório:** https://github.com/guilhermebrazioli/quem-faz-ai
- **Vídeo:** https://youtu.be/U_YzUO2m6UE

### 9. Indicadores de impacto

Recall macro@1 = 0,786 e recall macro@3 = 1,000. Na revisão humana das 60 respostas, as corretas foram 15% (A), 70% (B) e 65% (C), e as respostas com alucinação foram 100% (A), 10% (B) e 0% (C). Nos casos "não consta", B recusou corretamente 5 de 6 e C, 6 de 6. **Esses resultados vêm de uma amostra de teste**, ainda sem medição com usuários reais.

### 10. ODS conectados

**ODS 9 — Indústria, Inovação e Infraestrutura**

O Quem Faz contribui para esse objetivo ao propor uma solução tecnológica que digitaliza processos e facilita a conexão entre profissionais e contratantes. No módulo de Generative AI, uma LLM local fundamentada em fontes públicas demonstra o uso de inteligência artificial de forma segura e explicável.

**ODS 10 — Redução das Desigualdades (Meta 10.2)**

O Quem Faz busca ampliar as oportunidades de trabalho e geração de renda para profissionais autônomos e informais, inclusive aqueles que atuam em bairros periféricos de São Paulo. A plataforma oferece um espaço para que esses profissionais divulguem suas habilidades, encontrem novos clientes e construam sua reputação por meio de avaliações vinculadas aos serviços realizados.

**ODS 11 — Cidades e Comunidades Sustentáveis**

O Quem Faz se conecta a esse objetivo ao propor melhorias no acesso a serviços locais na cidade de São Paulo, facilitando o encontro entre moradores, empresas e profissionais da própria comunidade.

As contribuições aos ODS representam os objetivos e benefícios potenciais da solução, ainda não resultados sociais comprovados em operação real.

Documentos principais: [relatório acadêmico final](docs/RELATORIO_FINAL_GENERATIVE_AI.md), [guia de entrega com as evidências da rubrica](ENTREGA_FINAL.md), [diagrama de arquitetura](docs/arquitetura.md) e [contrato de integração](docs/integracao_mvp.md).

## Resultados da avaliação final

Avaliação cega de 60 respostas: 20 casos × 3 configurações, sendo 14 casos com resposta na base e 6 sem. Código, base e casos foram congelados por hash antes da execução ([manifesto](avaliacao/congelamento_final.json)).

Arquivos: [respostas](avaliacao/resultados/final/geracao.jsonl), [recuperação](avaliacao/resultados/final/recuperacao.csv), [placar automático](avaliacao/resultados/final/placar.csv), [revisão humana](avaliacao/resultados/final/revisao_humana.csv) e [placar consolidado da revisão](avaliacao/resultados/final/placar_revisao_humana.json).

| Métrica (revisão humana) | A (LLM sem contexto) | B (RAG simples) | C (Agente) |
|---|---|---|---|
| Corretas | 3 (15%) | 14 (70%) | 13 (65%) |
| Parciais | 4 | 1 | 0 |
| Incorretas | 13 | 5 | 7 |
| Com alucinação | 20 (100%) | 2 (10%) | 0 (0%) |
| Respostas sustentadas pelas fontes | 0/20 | 5/11 | 7/7 |
| Recusas adequadas / indevidas | não se aplica | 5 / 4 | 6 / 7 |

Recuperação (14 casos com evidência, sem limiar): recall macro@1 = 0,786 e recall macro@3 = 1,000.

**Análise.** Sem recuperação (A), o modelo alucinou em todas as respostas e não recusou nenhum caso fora da base. A recuperação (B) elevou a taxa de acerto para 70% e reduziu as alucinações para 10%. O agente (C) eliminou as alucinações, e todas as suas respostas ficaram sustentadas pelas fontes. Em troca, recusou com mais frequência: seus 7 erros são recusas indevidas, em que a informação estava na base.

**Análise de erros.** (1) A: conteúdo genérico, entidades e fontes inventadas. (2) B: acréscimos não sustentados pelos trechos e uma citação de trecho não pertinente. (3) B e C: 4 recusas indevidas porque nenhum trecho atingiu o limiar de 0,15 (maior score entre 0,05 e 0,12). (4) C: 3 recusas indevidas adicionais em que o trecho correto foi recuperado, mas a verificação de suficiência do agente rejeitou a resposta. Detalhes na seção 13 do [relatório](docs/RELATORIO_FINAL_GENERATIVE_AI.md).

**Metodologia da revisão.** Revisão humana cega das 60 respostas pelo autor na interface de revisão (ordem embaralhada, configuração oculta), com conferência por um segundo revisor.

**Próximo passo.** Ampliar a recuperação (expansão de consulta ou busca semântica) e tornar a verificação de suficiência do agente menos conservadora, aceitando suporte parcial com observação em vez de recusar.

## Arquitetura

FastAPI, Ollama com Qwen (`qwen2.5:1.5b` por padrão), busca lexical TF-IDF com stemming em português, trechos em JSON e validação com Pydantic.

- **A:** envia a pergunta diretamente à LLM, sem contexto (referência experimental).
- **B:** recupera até 3 trechos, aplica o limiar de 0,15 e a LLM gera a resposta com citação dos IDs, sem verificação posterior.
- **C:** agente que recupera, inspeciona o contexto contra instruções suspeitas, seleciona trechos, verifica suficiência e integridade e devolve o texto exato dos trechos confirmados; recusa quando não há sustentação.

Estrutura: `src/` (API e pipeline), `base/` (trechos e metadados), `avaliacao/` (casos, scripts e resultados), `notebooks/` (análises executadas), `tests/` (testes automatizados), `docs/` (relatórios), `historico/` (arquivos substituídos, preservados).

## Instalação

Requer Python 3.12, Ollama e memória suficiente para o modelo (os experimentos foram executados em máquinas com 16 GB de RAM). Não é obrigatório ter GPU dedicada.

**macOS**
```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
ollama pull qwen2.5:1.5b
```

**Windows (PowerShell)**
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull qwen2.5:1.5b
```

Deixe o Ollama em execução (aplicativo aberto ou `ollama serve`; não inicie uma segunda instância). No macOS, evite manter o projeto em pastas sincronizadas com o iCloud (Mesa/Documentos): o download dos arquivos sob demanda deixa as importações muito lentas.

`OLLAMA_MODEL`, `OLLAMA_URL` e `RAG_THRESHOLD` são variáveis de ambiente opcionais. O `.env.example` não é carregado automaticamente. O limiar padrão de 0,15 foi calibrado em casos sintéticos.

## Uso da API

```bash
python -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Documentação interativa: `http://127.0.0.1:8000/docs`. Consumidor de demonstração: `python exemplos/consumidor.py`.

Exemplo no macOS/Linux:
```bash
curl -s -X POST http://127.0.0.1:8000/api/ai/assistente \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{"descricao":"O orçamento precisa conter condições de pagamento e datas?","categoria":"pintura","configuracao":"C"}'
```

Exemplo no Windows:
```powershell
$body = @{ descricao = 'O orçamento precisa conter condições de pagamento e datas?'; categoria = 'pintura'; configuracao = 'C' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/ai/assistente -ContentType 'application/json; charset=utf-8' -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) | ConvertTo-Json -Depth 8
```

A resposta contém `categoria_sugerida`, `descricao_aprimorada`, `orientacoes` e `perguntas_sugeridas` (cada item com os IDs das fontes), além de `status`, `fontes`, `rastreio` e `observacao`. Em C, as orientações reproduzem o texto exato dos trechos confirmados, a descrição é mantida e as perguntas sugeridas vêm vazias. Em B, descrição, orientações e perguntas são geradas pela LLM a partir dos trechos recuperados. O endpoint retorna 422 para entrada inválida e 503 quando a LLM local não está acessível. Para comparar as configurações, envie a mesma descrição com `configuracao` igual a `A`, `B` e `C`.

## Testes e reprodução

```bash
python -m pytest -q
python scripts/verificar_entrega.py --testes
```

Estado na entrega: 30 testes automatizados aprovados.

Reprodução da avaliação (use sempre um destino novo; o executor não sobrescreve execuções existentes e confere os hashes congelados):
```bash
python -m avaliacao.executar_cega --destino avaliacao/resultados/minha_cega --manifesto avaliacao/congelamento_final.json
python -m avaliacao.consolidar_cega --diretorio avaliacao/resultados/minha_cega
```

Revisão humana na interface cega (cada avaliação exige justificativa e só é salva ao clicar em "Salvar avaliação"):
```bash
export REVISAO_CSV=avaliacao/resultados/minha_cega/revisao_humana.csv
python -m uvicorn avaliacao.revisao_web:app --host 127.0.0.1 --port 8001
python -m avaliacao.consolidar_revisao avaliacao/resultados/minha_cega/revisao_humana.csv --saida avaliacao/resultados/minha_cega/placar_revisao_humana.json
```
No Windows, substitua o `export` por `$env:REVISAO_CSV = "..."`. A interface não tem autenticação e não deve ser exposta à rede.

## Limitações

- Os 20 casos foram congelados antes da inferência, mas escritos pela própria equipe. A amostra é pequena e não permite generalização estatística.
- A interface cega oculta a configuração, mas ela ainda pode ser inferida pelo estilo da resposta ou pelas citações.
- A configuração C recusa casos que poderiam ser respondidos (recusas indevidas); B pode citar trechos não pertinentes, pois não verifica as citações.
- O filtro contra instruções maliciosas (prompt injection) em B e C é limitado. A API não tem autenticação nem proteção para exposição pública.
- Não inclua dados pessoais reais: os experimentos salvam perguntas e respostas.

## Histórico preservado

As versões anteriores foram mantidas para rastreabilidade: [relatório de auditoria v7](docs/relatorio_auditoria_v7.md), [relatório v6](docs/relatorio_continuacao.md), [relatório inicial](docs/relatorio_tecnico.md), [diagnóstico v6](avaliacao/resultados/diagnostico_v6/diagnostico.md) e [erros históricos](avaliacao/comparacao_erros_v8.md). As execuções anteriores estão em `avaliacao/resultados/` (`v3` a `v8_dev`, `cega_v1`, `cega_v2`, `adicional_v1` e `adicional_v2`). Os [16 casos internos adicionais](avaliacao/casos_internos_adicionais.json) e as rodadas `cega_v2` e `adicional_v2` são exploratórios e não fazem parte dos resultados finais.

## Publicação do repositório

Depois de revisar o conteúdo e criar um repositório vazio no GitHub, substitua a URL e execute:

```bash
git init
git add .
git status --short
git commit -m "Entrega acadêmica Quem Faz AI"
git branch -M main
git remote add origin https://github.com/USUARIO/REPOSITORIO.git
git push -u origin main
```

Confira o `git status` antes do commit: `.venv`, caches, `.env` e o mapa local de revisão devem ficar fora do Git.

## Integração com o MVP publicado

Integração com o MVP publicado: `scripts/demo_integracao_mvp.py` lê, somente por GET, as categorias e solicitações do MVP Quem Faz publicado na Azure ([repositório do MVP](https://github.com/guilhermebrazioli/quem-faz)) e envia perguntas de demonstração ao assistente local, associando cada uma a uma categoria real do MVP. A execução registrada em `avaliacao/resultados/integracao_mvp.json` leu 5 categorias (Elétrica, Hidráulica, Limpeza, Montagem de móveis e Pintura) e nenhuma solicitação. Na configuração B, a pergunta associada a Pintura foi fundamentada, com `categoria_sugerida` "Reforma", fora da taxonomia do MVP; a associada a Elétrica retornou `informacao_insuficiente`. Essas saídas não passaram por revisão humana e não integram a avaliação dos 60 casos. A integração não grava dados no MVP, o MVP não exibe as respostas e o assistente roda localmente com Ollama.
