# .claude/ — Camada de Capacidade do Projeto

O que o Claude Code carrega deste diretório (escopo "project", commitado no git):
- `rules/*.md` — regras do projeto, carregadas automaticamente junto do `CLAUDE.md`.
- `skills/<nome>/SKILL.md` — skills **específicas deste projeto** (auto-descobertas).
- `agents/*.md` — subagentes específicos deste projeto.
- `hooks/` — scripts de hook (registrados em `settings.json`).
- `settings.json` — permissões, hooks, o plugin do núcleo e configurações (commitado). `settings.local.json` é local (gitignored).

## Skills e agents GERAIS do núcleo
Não ficam aqui — vêm do plugin `ndados`, do marketplace **core-plugin**, para não duplicar entre repos. O `settings.json` já declara o plugin (`extraKnownMarketplaces` e `enabledPlugins`): ao abrir o projeto no Claude Code e confiar na pasta, ele carrega sozinho e se atualiza no começo das sessões.

Pré-requisito, uma vez por máquina: `gh auth login` e `gh auth setup-git`. O `core-plugin` é privado, e o Claude Code o baixa com as suas credenciais git, sem poder pedir senha. Passo a passo na seção "Setup do Claude Code" do `CLAUDE.md`.

Use `skills/` e `agents/` aqui **apenas** para o que é exclusivo deste projeto.
