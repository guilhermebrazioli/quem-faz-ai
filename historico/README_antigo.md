# Quem Faz AI

Prova de conceito local de assistência à contratação consciente para o Quem Faz. A plataforma não garante a qualidade dos serviços e o usuário decide a contratação. A pasta não contém o MVP principal: existe um consumidor de demonstração, não uma integração real comprovada. Não usar este protótipo em produção ou em situação de emergência.

O [relatório acadêmico final](docs/RELATORIO_FINAL_GENERATIVE_AI.md) reúne as execuções, critérios e limitações da entrega. O [relatório de auditoria v7](docs/relatorio_auditoria_v7.md), o [relatório v6](docs/relatorio_continuacao.md), o [relatório inicial](docs/relatorio_tecnico.md) e suas medições foram preservados como histórico. A versão atual ainda apresenta muitas recusas indevidas e depende de revisão humana: a verificação automática de pertinência é falível.

Integrantes: Enzo Vazquez Sartorelli (RM94618), Kaue Pastori Teixeira (RM98501), Nicolas Nogueira Boni (RM551965), Guilherme Brazioli (RM98237) e Pedro Oliveira Valotto (RM551445).

A arquitetura usa FastAPI, Ollama/Qwen, busca lexical TF-IDF, trechos JSON e validação Pydantic. A envia a pergunta à LLM, B adiciona RAG e C acrescenta verificações do agente; veja o [diagrama](docs/arquitetura.md). `src/` contém a API e o pipeline, `base/` os trechos, `avaliacao/` os casos e resultados, `notebooks/` as análises executadas, `tests/` os testes e `docs/` os relatórios. O [guia de entrega](ENTREGA_FINAL.md) reúne as evidências da rubrica.

## Instalação no Windows

Requer Python 3.12, Ollama e espaço/memória para o modelo. Nesta máquina foram usados 16 GB de RAM, Python 3.12 e `qwen2.5:1.5b` já instalado. Instale o Ollama pelo site oficial e execute no PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull qwen2.5:1.5b
ollama list
```

Inicie o serviço Ollama quando necessário (`ollama serve` em outro terminal; não inicie um segundo se já estiver ativo). Não há GPU dedicada obrigatória. A base versionada é `base/trechos.json`; `python montar_base.py` a recria a partir de paráfrases identificadas, e `python criar_casos.py` recria casos sintéticos. Não execute esses comandos sobre modificações próprias sem salvá-las. A busca é calculada em memória, sem índice externo.

```powershell
python -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

A documentação interativa fica em `http://127.0.0.1:8000/docs`. Em outro terminal:

```powershell
.\.venv\Scripts\Activate.ps1
python exemplos/consumidor.py
```

Ou envie uma solicitação:

```powershell
$body = @{ descricao = 'O orçamento precisa conter condições de pagamento e datas?'; categoria = 'pintura'; configuracao = 'C' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/ai/assistente -ContentType 'application/json; charset=utf-8' -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) | ConvertTo-Json -Depth 8
```

A resposta possui `status`, `orientacoes`, `fontes` e `rastreio`. Orientações são trechos da base, com IDs associados; descrição é mantida literalmente e perguntas sugeridas estão vazias nesta versão. O modelo pode recusar mesmo com informação disponível. O endpoint retorna 422 para entrada inválida e 503 quando a LLM local não está acessível. `configuracao` aceita A (LLM sem contexto), B (busca e verificação de pertinência pela LLM) e C (B mais checagens explícitas de integridade). B e C rejeitam certos padrões suspeitos antes da inferência, sem garantia contra todos os ataques. A configuração A serve de referência experimental e pode alucinar ou recomendar ações inseguras.

Para comparar as três configurações, altere o valor de `configuracao` no payload para `A`, `B` e `C`; use a mesma descrição para as três chamadas.

`OLLAMA_MODEL`, `OLLAMA_URL` e `RAG_THRESHOLD` são variáveis de ambiente opcionais; `.env.example` não é carregado automaticamente. O limiar padrão 0,15 foi calibrado em casos sintéticos. O filtro de injeção é limitado; não há autenticação ou proteção para exposição pública. Não inclua dados pessoais reais nos experimentos, que salvam perguntas e respostas.

## Testes e experimentos

```powershell
python -m pytest -q
python exemplos/verificar_api.py
python -m avaliacao.verificar_fluxo_cliente
python scripts/verificar_entrega.py --testes
python -m avaliacao.executar_v6 --destino avaliacao/resultados/minha_execucao
python -m avaliacao.consolidar_v6 --diretorio avaliacao/resultados/minha_execucao
python notebooks/gerar_notebooks.py
```

Use um destino novo em cada execução: o gerador recusa sobrescrever `geracao.jsonl`. A consolidação preserva um arquivo existente de revisão humana. Os resultados versionados de referência estão em `avaliacao/resultados/v6/execucao_final`; as tentativas anteriores continuam em `avaliacao/resultados/` e subpastas. Os notebooks são gerados e executados com saídas reais e leem o conjunto de referência salvo; regenerá-los substitui os notebooks existentes. A comparação e a calibração podem ser refeitas por `python -m avaliacao.comparar_busca_v6` e `python -m avaliacao.calibrar_v6`; por padrão, os novos arquivos ficam em `avaliacao/resultados/recalculo_busca`, sem sobrescrever os históricos.

A planilha `avaliacao/resultados/v6/execucao_final/revisao_humana.csv` tem campos vazios para correção, suporte e alucinação. Nenhum desses julgamentos foi atribuído automaticamente. O conjunto antes chamado final foi utilizado durante ajustes e precisa ser substituído por avaliação cega independente; resultados e condições estão no relatório atualizado.

## Avaliação nova e revisão humana

O [diagnóstico v6](avaliacao/resultados/diagnostico_v6/diagnostico.md) registra a reexecução dos oito casos. Os 20 casos novos foram congelados antes da inferência, mas escritos pela mesma equipe do projeto; a revisão semântica humana independente ainda está pendente. Os resultados estão em `avaliacao/resultados/cega_v1/` e no [relatório v7](docs/relatorio_auditoria_v7.md).

```powershell
python -m avaliacao.executar_cega --destino avaliacao/resultados/minha_cega
python -m avaliacao.consolidar_cega --diretorio avaliacao/resultados/minha_cega
python notebooks/gerar_avaliacao_cega.py
```

O executor verifica os hashes congelados e não sobrescreve uma execução existente. A versão atual corrige a codificação do prompt e precisa de um manifesto correspondente para reprodução; consulte o relatório.

Para revisar a planilha v6, execute o serviço abaixo e abra `http://127.0.0.1:8001`. Cada avaliação exige justificativa e só é salva por ação explícita:

```powershell
python -m uvicorn avaliacao.revisao_web:app --host 127.0.0.1 --port 8001
```

Para revisar outra planilha, defina antes de iniciar o serviço `$env:REVISAO_CSV = "avaliacao/resultados/cega_v1/revisao_humana.csv"`. Para consolidar a revisão, escolha um arquivo de saída ainda inexistente:

```powershell
python -m avaliacao.consolidar_revisao avaliacao/resultados/v6/execucao_final/revisao_humana.csv --saida avaliacao/resultados/minha_revisao.json
```

Não exponha a interface à rede: ela não tem autenticação. As taxas são calculadas somente sobre itens avaliados; campos vazios permanecem pendentes.

## Amostra adicional interna

Os [16 casos adicionais](avaliacao/casos_internos_adicionais.json) e o código foram congelados antes da execução; o conjunto foi elaborado no próprio projeto, sem validação independente. A [pré-revisão automática](avaliacao/resultados/cega_v2/pre_revisao_automatica.jsonl) verifica apenas estrutura e rótulos, não correção semântica nem alucinações. Na amostra adicional, recall macro@1 foi 0,9 e recall macro@3 foi 1,0 sobre dez casos com referências. B e C recusaram seis desses dez e tiveram quatro respostas com IDs estruturais válidos; esses números não comprovam fundamentação semântica.

Uma [segunda pré-revisão](avaliacao/resultados/cega_v2/pre_revisao_modelo.jsonl) foi produzida pelo mesmo modelo local para 60 respostas. Houve 13 falhas de esquema e inconsistências na classificação de recusas; seus julgamentos não são confiáveis como métricas e não substituem avaliadores humanos. Para repeti-la sem sobrescrever os dados, execute `python -m avaliacao.pre_revisao_modelo --saida avaliacao/resultados/minha_pre_revisao.jsonl`.

Após uma correção de segurança que estendeu a B o filtro limitado de instruções suspeitas, os mesmos casos foram reexecutados em `avaliacao/resultados/adicional_v2/`. A repetição é exploratória; o código da execução anterior foi preservado em `avaliacao/snapshots/v8/agente.py`. O manifesto padrão dos comandos abaixo corresponde à versão corrigida.

```powershell
python -m avaliacao.executar_adicional --destino avaliacao/resultados/minha_amostra_adicional
python -m avaliacao.consolidar_adicional --diretorio avaliacao/resultados/minha_amostra_adicional
```

## Revisão independente e exportação

A interface apresenta todas as respostas em ordem embaralhada e oculta o nome da configuração, o rastreio e o status que identificava o modo sem contexto. Isso reduz, mas não elimina, a possibilidade de inferir a configuração pela própria resposta ou pelas citações. Além de correção, fundamentação e alucinação, há campo para adequação da recusa; deixe campos não avaliados em branco e forneça justificativa ao salvar.

A [cópia preparada para uma segunda pessoa](avaliacao/resultados/cega_v2/segunda_revisao.csv) contém 60 respostas, sem julgamentos humanos preenchidos. Entregue somente esse CSV ao avaliador e mantenha separado o arquivo local `avaliacao/resultados/cega_v2/mapa_segunda_revisao.json`: ele permite recompor as configurações e está no `.gitignore`. Para abrir a cópia na interface, configure antes de iniciar:

```powershell
$env:REVISAO_CSV = "avaliacao/resultados/cega_v2/segunda_revisao.csv"
python -m uvicorn avaliacao.revisao_web:app --host 127.0.0.1 --port 8001
```

Após receber a cópia preenchida, consolide com o mapa local:

```powershell
python -m avaliacao.consolidar_revisao avaliacao/resultados/cega_v2/segunda_revisao.csv --mapa avaliacao/resultados/cega_v2/mapa_segunda_revisao.json --saida avaliacao/resultados/cega_v2/placar_humano.json
```

Para gerar outra cópia, escolha caminhos novos com `python -m avaliacao.exportar_segunda_revisao ENTRADA --saida SAIDA --mapa MAPA`. Preserve o mapa fora do material enviado ao avaliador e cuide dele como artefato necessário à consolidação. A cópia e o mapa não comprovam que a revisão foi realizada.

## Publicação do repositório

A pasta ainda não é um repositório Git. Depois de revisar o conteúdo e criar um repositório vazio no GitHub, o responsável pode executar os comandos abaixo, substituindo a URL. Eles não foram executados automaticamente.

```powershell
git init
git add .
git status --short
git commit -m "Entrega acadêmica Quem Faz AI"
git branch -M main
git remote add origin https://github.com/USUARIO/REPOSITORIO.git
git push -u origin main
```

Confira o `git status` antes do commit: `.venv`, caches, `.env` e o mapa local de revisão devem permanecer fora do Git. Os nomes e RMs informados são necessários à identificação acadêmica; os e-mails fornecidos não foram incluídos no relatório.
