# Decisões do esqueleto

Estas são as decisões de arquitetura **ratificadas** do esqueleto (o molde). Não
reabrir, não questionar — apenas obedecer. Este arquivo é a fonte única das decisões e
substitui a antiga pasta `docs/adr/` (cada decisão abaixo era um ADR separado).

> Escopo: decisões sobre o **molde**. As decisões do SEU projeto vão no vault de
> trabalho, em `context/<etapa>/NN_decisao_<tema>.md` (ver decisão 12).

---

## 0. Distribuição por cópia

**Contexto:** era preciso distribuir um padrão de projeto de DS para vários projetos
futuros. Opções: repo-mãe hospedando N projetos, gerador externo (cookiecutter/cruft),
ou cópia independente.

**Decisão:** um único esqueleto canônico; cada projeto real nasce como **cópia
independente** dele. Sem repo-mãe, sem gerador externo. O scaffolder é embutido
(`tools/init.py`) e roda 1x após a cópia.

**Consequências:** nenhum acoplamento entre projetos, nenhuma infraestrutura extra;
cada projeto é dono do seu destino. O preço — sem sincronização automática — é coberto
pela decisão 5 (forward-only).

## 1. Toggle Databricks

**Contexto:** alguns projetos rodam em Databricks, outros não. A dependência de
plataforma não pode contaminar o núcleo, nem podem existir duas versões do esqueleto.

**Decisão:** `tools/init.py` pergunta "Databricks? S/N". Se Não, poda a pasta
`platform/` e seta o modo dos `pipeline/entrypoints/`. O núcleo nunca é tocado pelo toggle.

**Consequências:** o núcleo permanece neutro e idêntico nos dois cenários; `platform/`
é a casca inteira que o toggle liga/desliga (invariante central); nada do núcleo importa
de `platform/`.

## 2. Fonte única de dependências

**Contexto:** num projeto anterior, `requirements.txt` e `conda.yaml` divergiram,
causando builds inconsistentes. Manter duas listas à mão garante drift.

**Decisão:** `pyproject.toml` + `uv` são a **fonte única**, com `uv.lock` versionado. Os
artefatos de plataforma (`conda.yaml`) são **gerados** a partir dele, nunca à mão.

**Consequências:** uma fonte só, um lockfile, zero divergência; mudar dependência exige
regerar os artefatos no mesmo commit (decisão 3), o que o CI verifica; editar
`conda.yaml` à mão passa a ser proibido.

## 3. Interface de dados neutra

**Contexto:** a origem física do dado varia por projeto e ambiente (tabela Spark,
Parquet, SQL). Acoplar `prepare_data` à origem torna o pipeline rígido e difícil de
testar.

**Decisão:** um `Protocol` `DataSource` em `pipeline/common/`; implementações concretas
(`ParquetSource`, `SparkTableSource`, `SQLSource`) em `pipeline/data/sources/`, escolhidas via
config. O código de preparação só pede o dado à interface; nunca sabe de onde vem.

**Consequências:** trocar a origem é trocar uma linha de config, não reescrever código;
testar fica fácil; a definição do `Protocol` mora em `pipeline/common/`, as implementações em
`pipeline/data/sources/`.

## 4. Mini-cérebro nativo + raiz mínima

> **Atualizada pelas decisões 6 e 8** quanto à localização e ao escopo do conteúdo de
> IA. Os princípios de mini-cérebro nativo e de raiz mínima seguem plenamente válidos.

**Contexto:** conhecimento de execução espalhado (na cabeça das pessoas, em docs
externos, em `_guia.md` soltos) faz o padrão depender de contexto que não viaja com o
repo. E raiz poluída esconde o que importa.

**Decisão:** todo o conteúdo de contexto/rules/guias/skills mora versionado **dentro**
do repo (o "mini-cérebro nativo"). Na raiz, só ponteiros e o que tecnicamente precisa
estar lá.

**Consequências:** quem clona o repo encontra o padrão e o segue sozinho; a raiz vira
vitrine de ponteiros (o CI checa a raiz mínima); proibido regra/guia solto por pasta.

## 5. Evolução forward-only

**Contexto:** templates que fazem back-propagation para projetos vivos (ex.: `cruft
update`) geram conflitos e quebras. Precisamos de um modelo de evolução previsível.

**Decisão:** o esqueleto evolui **pra frente**. Projetos futuros herdam melhorias ao
nascer; projetos em andamento ficam **congelados** na versão em que nasceram. Sem
auto-sync, sem back-propagation.

**Consequências:** estabilidade — um projeto vivo nunca é surpreendido por mudança de
template; melhorias valem para quem nasce depois; combina com a distribuição por cópia
(decisão 0).

## 6. Localização do mini-cérebro em `.claude/`

> **Atualizada pela decisão 8** quanto ao escopo (o que fica em `.claude/` vs `docs/`).

**Contexto:** a decisão 4 falava em "conteúdo de IA num lugar só", com argumento de
neutralidade. Na prática, o Claude Code é a ferramenta usada no dia a dia, e `.claude/`
é o diretório que ele reconhece por convenção.

**Decisão:** usar `.claude/` (em vez de um `ai/` genérico) como área do mini-cérebro,
mantendo a estrutura interna (`context/`, `rules/`, `guides/`, `skills/`).

**Consequências:** menor atrito com a ferramenta de fato usada; o conteúdo permanece
neutro (qualquer pessoa/IA lê os mesmos `.md`). Trade-off aceito: `.claude/` é oculta
(some do `ls`/GitHub) — mitigado por ponteiros na raiz.

## 7. As cancelas sobrevivem ao toggle de plataforma

**Contexto:** ao virar as rules em cancelas de CI (`tools/check_*.py`), surgiu a
pergunta: com Databricks = Não, o `init.py` deveria podar também os verificadores?

**Decisão:** as cancelas são **infraestrutura de núcleo**, não artefatos de plataforma.
Sobrevivem ao toggle. Só `tools/gen_conda.py` é podado. `tools/check_manifest.py` pula
com sucesso quando `platform/` não existe.

**Consequências:** o CI é o mesmo com ou sem Databricks; a garantia de qualidade do
núcleo não depende da casca de plataforma; a lista `ARTEFATOS_DE_PLATAFORMA` do
`init.py` é a fronteira explícita entre o que é podado e o que sobrevive.

## 8. Separação molde (`docs/`) × projeto (`.claude/`) e entrada única no `CLAUDE.md`

> **Atualiza as decisões 4 e 6** quanto ao escopo/localização do conteúdo de IA.
> **Atualizada pela decisão 10** quanto às skills: elas saíram de `docs/` e passaram a
> viver todas em `.claude/skills/`.

**Contexto:** o mini-cérebro em `.claude/` misturava dois tipos de informação: a que
descreve o **molde** (igual em todo projeto do núcleo) e a que descreve o **projeto**
específico (preenchida ao longo do tempo). Quem chegava não distinguia uma da outra.
Além disso, a raiz tinha dois pontos de entrada — `AGENTS.md` com o conteúdo e um
`CLAUDE.md` quase vazio apontando para ele —, redundância sem ganho.

**Decisão:** separar por pasta, pela natureza da informação:
- **`docs/`** passa a conter TODA a documentação do molde — `context/` (projeto,
  arquitetura, glossário, decisões do esqueleto), `rules/`, `guides/`, `skills/` e este
  `decisoes.md`. É o "manual do esqueleto".
- **`.claude/`** passa a conter só o contexto do **projeto** — `context/` a preencher, e
  `rules/`/`guides/`/`skills/` como espaço para acréscimos específicos do projeto.
- O ponto de entrada único é o **`CLAUDE.md`** na raiz; o `AGENTS.md` é removido.

**Consequências:**
- Quem chega distingue na hora "o que é o molde" (`docs/`) de "o que é este projeto"
  (`.claude/`) — some a confusão que motivou esta decisão.
- As rules do molde continuam valendo e sendo **verificadas pelo CI**; agora
  documentadas em `docs/rules/`.
- Trade-off aceito: manter só o `CLAUDE.md` acopla o nome do arquivo de entrada ao
  Claude Code (a ferramenta usada no núcleo). O conteúdo segue neutro — qualquer
  pessoa/IA lê os mesmos `.md`; se outra ferramenta virar padrão, renomeia-se o
  ponteiro sem reescrever conteúdo.
- A raiz mínima é reforçada: um único arquivo de entrada em vez de dois.

## 9. Uma pasta só para o trabalho do analista: `pipeline/`

**Contexto:** a raiz tinha seis pastas de código lado a lado (`common/`, `config/`,
`data/`, `entrypoints/`, `models/`, `platform/`), o que diluía "onde eu de fato
trabalho" e confundia analistas na hora de executar.

**Decisão:** agrupar sob uma única pasta **`pipeline/`** tudo que o analista cria e
edita — `common/`, `config/`, `data/`, `entrypoints/` e `models/`. `platform/` fica
**de fora** (é infra de deploy, opcional e pouco tocada, mais próxima de `tools/` e
`.github/`). Usa-se um **src-layout**: o `pipeline/` entra no `sys.path` (via o editable
install e o `pythonpath` do pytest), então os imports continuam de primeiro nível
(`from common...`, `from models...`) — sem prefixo `pipeline.` no código.

**Consequências:**
- A raiz vira uma vitrine enxuta; o analista tem um lugar óbvio para trabalhar.
- Reforça a raiz mínima (decisão 4): as pastas de código não têm requisito técnico para
  estar na raiz.
- Custo: os comandos ficam um nível mais longos
  (`uv run python pipeline/entrypoints/run_local.py --config pipeline/config/<modelo>.yaml`).
- `check_root.py` passa a permitir `pipeline/` (uma entrada) no lugar das cinco pastas;
  `check_platform.py` varre `pipeline/`; o `init.py` opera sob `pipeline/`. `platform/`
  segue na raiz, verificada como antes.

## 10. Skills invocáveis vivem todas em `.claude/skills/` (não em `docs/`)

> **Atualiza a decisão 8** quanto à localização das skills.

**Contexto:** a decisão 8 colocou as "skills" (procedimentos: adicionar modelo, fonte de
dados, dependência, iniciar projeto) em `docs/skills/`, como documentação do molde. Mas o
Claude Code só **descobre e invoca** Skills que estejam em `.claude/skills/<nome>/SKILL.md`
(com frontmatter). Em `docs/`, elas eram só texto que a IA lia quando apontada — nunca
capacidades invocáveis.

**Decisão:** todas as skills invocáveis moram em **`.claude/skills/`**, no formato
`<nome>/SKILL.md`. A pasta `docs/skills/` é **removida**. Isso inclui as skills do molde
(que passam a vir versionadas em `.claude/skills/`) e as específicas do projeto. É uma
**exceção técnica** à separação molde/projeto da decisão 8: skill invocável só funciona em
`.claude/skills/`, então é lá que todas ficam, independentemente de serem "do molde".

**Consequências:**
- O Claude passa a **invocar** essas skills sozinho quando a situação bate com o
  `description` (ex.: "quero adicionar um modelo" → dispara `adicionar-novo-modelo`), em
  vez de depender de ser apontado para um `.md`.
- `docs/` fica só com `context/`, `rules/`, `guides/` e o `GUIA-DO-ANALISTA.md`.
- Há skills que **criam** artefatos no formato certo: `criar-skill` (novas skills) e
  `criar-rule` (regras de projeto em `.claude/rules/`, ligadas via `@import` no `CLAUDE.md`).
- Ressalva: uma skill nova só é descoberta ao iniciar uma **nova sessão** do Claude Code.

## 11. Os manuais em PDF ficam na raiz (exceção editorial à raiz mínima)

**Contexto:** o esqueleto passou a ser distribuído com dois manuais em PDF —
`Descrição do Repositorio.pdf` e `Guia do Repositorio.pdf`. Eles não têm requisito
técnico que os obrigue à raiz: tecnicamente funcionariam em `docs/`. Mas a raiz é a
vitrine que o GitHub renderiza, e é onde quem chega pela primeira vez olha antes de
abrir qualquer pasta.

**Decisão:** manter os dois PDFs na raiz, registrados na allowlist de
`tools/check_root.py`. É uma exceção **editorial** explícita, não um requisito
técnico — e é assim que está escrito na allowlist, para não mentir sobre o critério
da Rule 04.

**Consequências:**
- A Rule 04 continua valendo com o mesmo rigor para todo o resto: a allowlist segue
  fechada, e qualquer arquivo novo na raiz reprova o CI.
- Estas duas entradas **não são precedente**. Um `.md` sobre o molde continua indo
  para `docs/`; contexto de projeto, para `.claude/`. O que se abriu aqui foi uma
  exceção nomeada, não a porteira.
- Custo aceito: o critério da raiz deixa de ser "só requisito técnico" e passa a ser
  "requisito técnico, mais as exceções registradas nesta decisão".

**Nota de implementação:** ao registrar os PDFs, apareceu um bug na própria cancela —
`entradas_versionadas()` lia `git ls-files` sem `-z`, e o git devolve nomes não-ASCII
escapados em octal (`Descri\303\247\303\243o...`), que nunca batiam com a allowlist.
Corrigido com `-z` + split em NUL. Valia para qualquer arquivo acentuado na raiz, não
só para estes.

## 12. `context/` na raiz — vault de trabalho do projeto

> **Atualiza a decisão 8** quanto ao papel de `.claude/`: ela deixa de ser "o contexto
> deste projeto" e passa a ser exclusivamente a camada de **capacidade**.

**Contexto:** o núcleo (NDados) padronizou todo repositório de projeto em **três
camadas**: `CLAUDE.md` = conhecimento (o que saber), `.claude/` = capacidade (o que
fazer: rules, skills, agents, hooks, settings) e `context/` na raiz = trabalho (vault
cronológico de etapas e conclusões, destilado ao final para a `core-knowledgebase`). O
`boilerplate-CD` divergia desse padrão: guardava o contexto-de-projeto em
`.claude/context/` — usando `.claude/` com um significado que, no resto do núcleo,
pertence a `context/` — e não tinha vault de trabalho nenhum.

**Decisão:** alinhar o CD ao boilerplate genérico do núcleo. O contexto-de-projeto sai
de `.claude/context/` (pasta **removida**) e passa a viver em dois lugares: o **contexto
geral** vira uma seção do `CLAUDE.md` ("Contexto geral do projeto"), e o **registro do
trabalho** vira o vault `context/` na raiz — etapas cronológicas (`NN_<etapa>/`, com
decisões em ADR-lite e contextos técnicos), `glossario.md` e `99_conclusoes/`.
`.claude/` passa a ser exclusivamente a camada de **capacidade**.

**Consequências:**
- `context/` entra na allowlist de raiz (`tools/check_root.py`, Rule 04) — sem isso o CI
  reprova. É a terceira pasta da raiz sem requisito técnico puro: existe por ser o
  contrato de interoperabilidade com a `core-knowledgebase`.
- A descrição de `.claude/` muda de "contexto do projeto" para "capacidade do projeto"
  no `CLAUDE.md`, na allowlist e na tabela de raiz de `arquitetura.md`.
- `docs/context/` (o contexto do **MOLDE**) **permanece inalterado**. A colisão de nomes
  entre `docs/context/` (esqueleto) e `context/` (projeto) é o custo aceito para não
  reescrever o manual do molde nem destoar do genérico.
- Ao encerrar o projeto, `context/` é destilado para a `core-knowledgebase`
  (`projects/<slug>/retrospectiva.md` + `learnings/drafts/`).
- `.claude/` ganha a paridade que faltava: `README.md`, `settings.json`, `agents/`,
  `hooks/` e `rules/00-nucleo.md`.

**Compatibilidade:** a **decisão 8** continua válida — o ponto de entrada único da raiz
segue sendo o `CLAUDE.md`; `context/` é pasta de trabalho, não ponto de entrada. A
**decisão 10** continua válida — skills invocáveis só em `.claude/skills/`, intocadas.

## 13. CI em dois jobs: o contrato barra, o conselho avisa

> **Atualiza as decisões 4 e 11** quanto ao efeito da raiz mínima no CI ("qualquer
> arquivo novo na raiz reprova o CI") e o cabeçalho antigo do `ci.yml` ("se uma rule
> for violada, o merge não passa").

**Contexto:** o CI tratava toda rule do molde como cancela de merge: arquivo novo na
raiz, `import mlflow` fora do `tracking.py` ou o núcleo importando de `platform/`
reprovavam o PR do mesmo jeito que um teste quebrado. Com a regra de CI da organização
exigindo o check, isso viraria barreira a qualquer flexibilização de escopo (um
`Dockerfile`, uma pasta `app/`, uma integração nova), mesmo com o coordenador de acordo.

**Decisão:** o CI passa a ter dois jobs. `contrato` barra o merge e só verifica o que,
se quebrar, quebra o projeto sem ninguém perceber: estrutura essencial e plugin do
núcleo, dados e segredos fora do git, skills que o Claude Code carrega, erros de Python
que quebram (ruff E9, F63, F7 e F82), `pytest` e manifesto em sync. `conselho` só avisa:
estrutura recomendada, estilo (ruff), raiz mínima, MLflow centralizado, plataforma
isolada e convenções. É o `contrato` que a regra de CI da organização deve exigir.

**Consequências:**
- As rules de `docs/rules/` continuam valendo. O que muda é o efeito da violação de uma
  rule de arquitetura: vira aviso no PR, e quem decide a exceção é o coordenador.
- A allowlist de `tools/check_root.py` continua sendo o lugar de registrar uma exceção
  da raiz; sem registrar, o aviso reaparece em todo PR.
- `tools/check.py` espelha a divisão e sai com erro só quando o contrato reprova.
- O mesmo modelo vale para os outros boilerplates do núcleo (genérico, DD e IA), para a
  regra de CI da organização exigir um único job, `contrato`, em todos.
