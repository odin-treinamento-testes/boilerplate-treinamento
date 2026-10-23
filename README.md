# boilerplate-projetogenerico — Template de Repositório de Projeto (NDados / ODIN)

> **Treinamento.** Cópia do `boilerplate-projetogenerico` do ODIN para os treinamentos. Quem usa o
> Claude no navegador segue a trilha do trainee em `manual-treinamento`; o setup do Claude Code
> abaixo vale para quem tem Claude Code.

Esqueleto para novos projetos do núcleo. Use **"Use this template"** no GitHub para criar `projeto-<slug>` já equipado.

## O que vem de fábrica
- `CLAUDE.md` — contexto geral do projeto (preencher).
- `.claude/` — capacidade: `rules/`, `skills/`, `agents/`, `hooks/`, `settings.json`.
- `context/` — vault de trabalho: etapas → decisões → conclusões.

## Primeiros passos ao criar um projeto
1. Preencha o `CLAUDE.md` (cliente, escopo, objetivo, etapas).
2. Uma vez por máquina, rode `gh auth login` e `gh auth setup-git`; depois abra o projeto no Claude Code e confie na pasta. As skills/agents gerais do núcleo carregam sozinhos (ver `.claude/README.md`).
3. Renomeie/duplique `context/01_etapa-exemplo/` conforme as etapas reais.
4. Ao encerrar, destile as conclusões para a `core-knowledgebase`.

## CI: o que barra e o que só avisa

| Job | Verifica | Se falhar |
|---|---|---|
| `contrato` | `CLAUDE.md`, `.claude/settings.json` com o plugin do núcleo, `.github/CODEOWNERS`, `context/README.md` e `context/99_conclusoes/`; nenhum `.env` nem `CLAUDE.local.md` versionado; skills que o Claude Code carrega | **Barra o merge** |
| `conselho` | Estrutura recomendada (`.claude/README.md`, `context/glossario.md`, `.claude/rules/`, `.claude/skills/`), `.gitignore` e convenções de nome | **Só avisa** no PR |

Pasta ou arquivo novo não barra o merge. Se um item do contrato não faz mais sentido para o projeto, ajuste a lista em `tools/check_estrutura.py` no mesmo PR: quem decide é o coordenador, ao aprovar.

Para rodar localmente: `python3 tools/check_estrutura.py` (contrato) e `python3 tools/check_estrutura.py --conselho`.
