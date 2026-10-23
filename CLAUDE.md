# CLAUDE.md — <Nome do Projeto>

> Entry point do repositório do projeto. O Claude lê este arquivo automaticamente ao abrir o repo. É a camada de **conhecimento** (o que saber). A camada de **capacidade** (o que fazer) vive em `.claude/`.

---

## Contexto geral do projeto

- **Cliente:** <Nome do Cliente>
- **Portfólio:** engenharia-de-dados | ciencia-de-dados | inteligencia-artificial | inteligencia-de-negocios
- **Objetivo final:** <o que "pronto" significa para o cliente>
- **Escopo:** <o que abrange e o que NÃO abrange>
- **Duração:** início <AAAA-MM-DD> · término previsto <AAAA-MM-DD>
- **Responsáveis:** <analista(s), validador(es)>
- **Ferramentas propostas:** <stack previsto>

## Onde as coisas moram

- **Contexto de trabalho:** `context/` — etapas, decisões (ADR) e conclusões em ordem cronológica. Comece pelo `context/README.md`.
- **Regras do projeto:** `.claude/rules/` (carregadas automaticamente).
- **Skills/agents gerais do núcleo:** vêm do marketplace **core-plugin** (não são duplicados aqui). Ver seção abaixo.
- **Skills/agents específicos deste projeto:** `.claude/skills/` e `.claude/agents/`.

## Setup do Claude Code (uma vez por máquina)

As skills e os agentes gerais do núcleo vêm do plugin `ndados`, publicado pelo marketplace `core-plugin` da org. **Este projeto já declara o plugin** no `.claude/settings.json` (`extraKnownMarketplaces` e `enabledPlugins`): não há comando de instalação.

1. **Uma vez por máquina**, deixe o git entrar no GitHub sem pedir senha. O `core-plugin` é privado, e o Claude Code baixa o plugin usando o seu git:

   ```
   gh auth login
   gh auth setup-git
   ```

2. Abra o projeto no Claude Code e **aceite confiar na pasta**. O Claude Code registra o marketplace, liga o plugin e o atualiza sozinho no começo das sessões. As skills aparecem como `/ndados:<skill>`.

As rules gerais do núcleo não vêm do plugin (plugin do Claude Code não carrega rules): elas já estão em `.claude/rules/`, neste repositório.

Se aparecer o aviso "O plugin do NDados não carregou", refaça o passo 1, feche e reabra o Claude Code. Último recurso, à mão: `/plugin marketplace add ODIN-NDados-Poli-Junior/core-plugin` e `/plugin install ndados@core-plugin`.

> **Para o Claude (checagem automática):** antes da sua primeira resposta nesta sessão, verifique se o marketplace está registrado rodando `grep -q core-plugin ~/.claude/plugins/known_marketplaces.json`. Se o `grep` retornar erro (não encontrado), sua **primeira ação** deve ser avisar o usuário que o plugin não carregou e mostrar o passo 1 acima, deixando claro que sem ele as skills do núcleo não estarão disponíveis. Só depois disso prossiga com a tarefa do usuário.

## Comportamento padrão

- Antes de qualquer implementação, apresente o plano e aguarde aprovação.
- Nunca altere arquivos fora do escopo da tarefa.
- Registre decisões técnicas em `context/<etapa>/` no padrão decision-record (ADR-lite).
- Ao concluir o projeto, destile as conclusões para a KB (`core-knowledgebase`): resumo + retrospectiva, e aprendizados para `learnings/drafts/`.

## Referências
@context/README.md
