# Rule 04 — Raiz mínima

A raiz é uma vitrine de ponteiros. Só fica na raiz o que tecnicamente não funciona em
outro lugar (ver a tabela em `docs/context/arquitetura.md`).

**Faça:** colocar qualquer novo arquivo dentro da subpasta certa (`docs/` para doc do
molde, `context/` para o trabalho do projeto, `.claude/` para capacidade, `tools/`, etc.).
**Não faça:** criar arquivo na raiz sem requisito técnico que o obrigue a estar lá.
Documentação do molde mora em `docs/`; o registro do trabalho do projeto, em `context/`;
a capacidade (rules, skills, agents, hooks), em `.claude/`. O CI avisa quando a raiz
mínima é violada (job `conselho`): não barra o merge, e quem decide a exceção é o
coordenador, no PR. Exceção aceita entra na allowlist de `tools/check_root.py`.
