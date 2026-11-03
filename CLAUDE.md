# CLAUDE.md — Ponto de entrada para qualquer IA ou pessoa

Este repositório é um **esqueleto canônico** para projetos de Ciência de Dados do
núcleo de dados da PoliJúnior. Toda a inteligência de execução viaja **dentro** do repo,
versionada — nada depende de conhecimento externo.

Apesar do nome do arquivo, o conteúdo é **neutro**: vale para qualquer IA ou pessoa, não
só para o Claude. Este é o único ponto de entrada da raiz (ver decisão 8 em
`docs/context/decisoes.md`).

## Treinamento (leia primeiro)

Este repositório é de uma equipe de **treinamento** do NDados: o case é simulado e o cliente é
fictício. O enunciado do case está em `context/00_case/` (fonte do que o cliente pediu). O
validador da equipe aprova os PRs (`CODEOWNERS`).

- **Quem trabalha com o Claude no navegador** (Projeto no claude.ai, plano gratuito): você só
  **lê** o repositório. Quem roda comandos e o git é o trainee, no Windows (PowerShell): use
  `python`, não `python3`, e dê os comandos em PowerShell. As seções "Setup do Claude Code" e
  "Para o Claude (checagem automática)" abaixo valem só para quem usa Claude Code: ignore-as.
- **Primeiro PR da equipe:** rodar `python tools/init.py` (nome do projeto, Databricks **N**,
  nome do primeiro modelo) e preencher "Contexto geral do projeto" com o case. Só uma pessoa
  da equipe roda o `init`, numa árvore git limpa, e ele roda uma única vez.
- **Sessões e atas** das skills `odin-sessao` e `odin-ata` ficam em `context/sessions/`.
  Isto é uma exceção do treinamento à regra "todo arquivo novo entra numa etapa".
- **Sem Databricks:** a equipe roda o pipeline local (`uv run python pipeline/entrypoints/run_local.py`).
  Não mexa em `platform/` (o `init` com Databricks **N** já a remove).
- Antes de abrir o PR: `python tools/check.py`. Se o `uv` não estiver instalado, veja o setup do
  ambiente no `manual-treinamento`.

## Contexto geral do projeto

- **Cliente:** <Nome do Cliente>
- **Portfólio:** ciencia-de-dados
- **Objetivo final:** <o que "pronto" significa para o cliente>
- **Escopo:** <o que abrange e o que NÃO abrange>
- **Duração:** início <AAAA-MM-DD> · término previsto <AAAA-MM-DD>
- **Responsáveis:** <analista(s), coordenador(es)>
- **Ferramentas propostas:** <stack previsto>

> Enquanto estiver com os `<...>`, a IA sabe operar o *padrão* do esqueleto
> (documentado em [`docs/`](docs/)), mas não sabe nada do seu problema, dos seus dados
> ou do seu domínio — e vai ter que adivinhar. O detalhamento (problema de negócio,
> fontes de dado, modelos, stakeholders) é registrado ao longo do trabalho no vault
> [`context/`](context/README.md); os termos do domínio, em
> [`context/glossario.md`](context/glossario.md).

## PARA A IA: o que abrir ANTES de ajudar

Você recebe este `CLAUDE.md` automaticamente, mas **não** o conteúdo dos arquivos que
ele cita — você precisa abri-los. Antes de guiar qualquer pessoa, faça nesta ordem:

1. **Descubra a fase do repo:**
   - **Cópia nova, ainda não inicializada** — sinais: existe `tools/init.py`, existe
     `pipeline/models/exemplo_modelo/`, e o `pyproject.toml` ainda tem
     `name = "esqueleto-ciencia-de-dados"`. Nesse caso, **o PRIMEIRO passo é invocar a
     skill `iniciar-projeto-novo-a-partir-do-esqueleto`** (ou abrir
     `.claude/skills/iniciar-projeto-novo-a-partir-do-esqueleto/SKILL.md`), com
     [`docs/GUIA-DO-ANALISTA.md`](docs/GUIA-DO-ANALISTA.md) ao lado para o *porquê* de
     cada passo. Ela conduz o analista da cópia ao primeiro pipeline rodando.
   - **Projeto já inicializado** (o `init.py` já rodou e sumiu) — leia `docs/rules/`
     (obrigatório), a seção **"Contexto geral do projeto"** acima e o vault de trabalho
     [`context/`](context/README.md) (o que ESTE projeto é e o que já foi decidido nele),
     e o guia da camada que você vai tocar em `docs/guides/`.
2. **Só então** responda ou aja.

## As três camadas (padrão do núcleo)

Cada repositório de projeto do núcleo se organiza em três camadas, separadas pela
**natureza** da informação:

- **`CLAUDE.md`** (este arquivo) — camada de **conhecimento**: *o que saber*. O contexto
  geral do projeto (acima) e os ponteiros para todo o resto.
- **`.claude/`** — camada de **capacidade**: *o que fazer*. `rules/`, `skills/`,
  `agents/`, `hooks/` e `settings.json`. **Não** guarda contexto de projeto.
  (Pasta oculta — use `ls -a`; ver [`.claude/README.md`](.claude/README.md).)
- **`context/`** (raiz) — camada de **trabalho**: o vault cronológico do projeto, uma
  pasta por etapa com suas decisões e contextos, mais `99_conclusoes/`. Ao encerrar o
  projeto, é **destilado** para a `core-knowledgebase`. Comece por
  [`context/README.md`](context/README.md).

E, atravessando as três, o manual do molde:

- **`docs/`** — o **manual do molde**. Descreve o esqueleto em si: como ele é composto e
  como se mexe nele. Igual em todo projeto do núcleo. **Não muda de projeto para projeto.**
  Atenção: `docs/context/` descreve o **esqueleto**, não o seu projeto.

Regra de ouro: se a informação descreve *o padrão*, mora em `docs/`; se descreve *o que
este projeto fez e decidiu*, mora em `context/`; se é *uma capacidade que a IA executa*,
mora em `.claude/`. **Exceção técnica:** Skills invocáveis (mesmo as do molde) só
funcionam em `.claude/skills/` — o Claude Code não as descobre em `docs/` (decisão 10).

## Onde as coisas moram

No molde (`docs/`):

- `docs/context/`  — o que é o esqueleto, arquitetura, decisões ratificadas, glossário.
- `docs/rules/`    — comportamento **inegociável**: o que você pode e não pode fazer.
  **Leitura obrigatória antes de alterar qualquer coisa.** É verificado pelo CI.
- `docs/guides/`   — um guia por camada (config, data, models, common, entrypoints, platform).
- `docs/context/decisoes.md` — todas as decisões de arquitetura do esqueleto, num arquivo só.
- `docs/GUIA-DO-ANALISTA.md`  — onboarding narrado, da cópia ao primeiro pipeline rodando.

No trabalho deste projeto (`context/`):

- `context/README.md`   — **comece aqui ao herdar o repo**: o índice das etapas.
- `context/<NN_etapa>/` — uma pasta por etapa, em ordem cronológica, com as decisões
  (`NN_decisao_<tema>.md`, padrão ADR-lite) e os contextos técnicos
  (`NN_contexto_<tema>.md`) daquela etapa.
- `context/glossario.md` — os termos do NEGÓCIO deste projeto (arquivo vivo).
- `context/99_conclusoes/` — fechamento: entregáveis, ferramentas realmente usadas,
  fluxo gerado e aprendizados. É o que vira retrospectiva na `core-knowledgebase`.

Na capacidade deste projeto (`.claude/`):

- `.claude/skills/` — **Skills invocáveis** (o Claude descobre e chama sozinho). Todas
  as skills moram aqui — as do molde (adicionar modelo, fonte de dados, dependência,
  iniciar projeto, criar-skill, criar-rule) e as que você criar. Ver decisão 10.
- `.claude/rules/` — regras de comportamento: `00-nucleo.md` (base do núcleo) e as
  regras deste projeto, ligadas via `@import` abaixo.
- `.claude/agents/`, `.claude/hooks/`, `.claude/settings.json` — subagentes, scripts de
  evento e permissões específicos deste projeto.

## Setup do Claude Code (uma vez por máquina)

As skills e os agentes gerais do núcleo vêm do plugin `ndados`, publicado pelo
marketplace `core-plugin` da org. **Este projeto já declara o plugin** no
`.claude/settings.json` (`extraKnownMarketplaces` e `enabledPlugins`): não há
comando de instalação.

1. **Uma vez por máquina**, deixe o git entrar no GitHub sem pedir senha. O
   `core-plugin` é privado, e o Claude Code baixa o plugin usando o seu git:

   ```
   gh auth login
   gh auth setup-git
   ```

2. Abra o projeto no Claude Code e **aceite confiar na pasta**. O Claude Code registra
   o marketplace, liga o plugin e o atualiza sozinho no começo das sessões. As skills
   aparecem como `/ndados:<skill>`.
   A sessão abre no **orquestrador**, o agente principal do núcleo, que o mesmo
   `settings.json` declara (`"agent": "ndados:orquestrador"`): é com ele que você
   conversa, e ele delega as missões aos operários.

As rules gerais do núcleo não vêm do plugin (plugin do Claude Code não carrega rules):
elas já estão em `.claude/rules/`, neste repositório.

Se aparecer o aviso "O plugin do NDados não carregou", refaça o passo 1, feche e
reabra o Claude Code. Último recurso, à mão: `/plugin marketplace add
ODIN-NDados-Poli-Junior/core-plugin` e `/plugin install ndados@core-plugin`.

> **Para o Claude (checagem automática):** antes da sua primeira resposta nesta
> sessão, verifique se o marketplace está registrado rodando
> `grep -q core-plugin ~/.claude/plugins/known_marketplaces.json`. Se o `grep`
> retornar erro (não encontrado), sua **primeira ação** deve ser avisar o usuário
> que o plugin não carregou e mostrar o passo 1 acima, deixando claro que sem ele
> as skills do núcleo não estarão disponíveis. Só depois disso prossiga com a
> tarefa do usuário.
>
> Confira também se você é o **Orquestrador do NDados**. Se não for, avise na mesma
> primeira ação que a sessão não abriu no orquestrador: ou o plugin não carregou, ou
> o `.claude/settings.json` não declara `"agent": "ndados:orquestrador"`.

## Regras específicas deste projeto

Regras de **comportamento desta cópia** (ex.: métrica padrão, nomeação de tabelas),
criadas pela skill `criar-rule` e carregadas em toda sessão via `@import` abaixo. Não
confundir com as rules do molde (`docs/rules/`, verificadas pelo CI) — estas aqui são
soft e específicas do projeto. Enquanto vazio, não há regras específicas ainda.

<!-- criar-rule: inserir os @import das regras do projeto ABAIXO desta linha -->

## Primeiro contato?

Se você é analista e nunca viu este padrão, comece pelo
[`docs/GUIA-DO-ANALISTA.md`](docs/GUIA-DO-ANALISTA.md).

**Antes de alterar qualquer coisa, a leitura de `docs/rules/` é OBRIGATÓRIA.**

## Vault de trabalho

@context/README.md
