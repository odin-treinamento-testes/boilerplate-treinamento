# Contexto de Trabalho — <Nome do Projeto>

> Vault de trabalho do projeto (versionado). Registra o **passo a passo** da execução: cada etapa com suas decisões e contextos, em ordem cronológica, e as conclusões ao final. É a matéria-prima que depois é **destilada** para a `core-knowledgebase` (resumo + retrospectiva + learnings).

## Estrutura
- `NN_<etapa>/` — uma pasta por etapa (prefixo numérico dá a ordem).
  - `README.md` — resumo da etapa.
  - `NN_decisao_<tema>.md` — decisão no padrão ADR-lite.
  - `NN_contexto_<tema>.md` — contexto técnico (fontes, restrições, descobertas).
- `99_conclusoes/` — fechamento: entregáveis, ferramentas realmente usadas, fluxo gerado, aprendizados.

## Etapas
- [01_etapa-exemplo](./01_etapa-exemplo/) — <renomeie/duplique conforme as etapas reais>
- [99_conclusoes](./99_conclusoes/)

> Convenções (frontmatter, nomes): seguem o padrão da KB (`governance/conventions.md`).
