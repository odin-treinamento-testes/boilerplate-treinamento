# Contexto de Trabalho — <Nome do Projeto>

> Vault de trabalho do projeto (versionado). Registra o **passo a passo** da execução: cada etapa com suas decisões e contextos, em ordem cronológica, e as conclusões ao final. É a matéria-prima que depois é **destilada** para a `core-knowledgebase` (resumo + retrospectiva + learnings).

## Estrutura
- `project-context.md` — resumo vivo do projeto: objetivo, escopo, stakeholders e o
  histórico de sessões.
- `NN_<etapa>/` — uma pasta por etapa (prefixo numérico dá a ordem).
  - `README.md` — resumo da etapa.
  - `NN_decisao_<tema>.md` — decisão no padrão ADR-lite.
  - `NN_contexto_<tema>.md` — contexto técnico (fontes, restrições, descobertas).
- `99_conclusoes/` — fechamento: entregáveis, ferramentas realmente usadas, fluxo gerado, aprendizados.

## Etapas
- [01_etapa-exemplo](./01_etapa-exemplo/) — <renomeie/duplique conforme as etapas reais>
- [99_conclusoes](./99_conclusoes/)

## Como registrar

- **Todo arquivo novo entra numa etapa.** Antes de gravar uma sessão, ata, weekly, decisão ou
  contexto, o Claude pergunta em qual pasta `NN_<etapa>/` (ou `99_conclusoes/`) ele entra. Etapa que
  ainda não existe é criada com o próximo número antes do `99` e entra na lista de etapas acima.
- **Nome:** `NN_<tipo>_<tema>.md`, com `NN` = próximo número livre da pasta. Tipos: `decisao`,
  `contexto`, `sessao`, `ata`, `weekly`.
- **Na raiz** ficam só os arquivos fixos: este índice, o [`project-context.md`](./project-context.md),
  o [`glossario.md`](./glossario.md) e os do kickoff (contrato, confidencialidade, onboarding).
- **Até 8KB por arquivo** (8192 bytes; letra acentuada conta 2). Passou, divide entre seções: a
  parte 1 mantém o nome, as seguintes viram `<nome>_pt2.md`, `<nome>_pt3.md`..., cada uma com o
  frontmatter, o H1 com "(parte N)" e o link para a próxima, e todas entram no `README.md` da etapa.
  O `project-context.md` fica fora do limite: é o resumo vivo do projeto. O plugin do núcleo avisa o
  Claude quando um arquivo passa do limite, e o CI avisa no PR.

> Convenções (frontmatter, nomes): seguem o padrão da KB (`governance/conventions.md`).
