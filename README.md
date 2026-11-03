# <!-- PREENCHER: nome do projeto -->

> **Template.** Este README é herdado do esqueleto canônico de projetos de Ciência de
> Dados do núcleo de dados da PoliJúnior. Os trechos marcados com
> `<!-- PREENCHER: ... -->` devem ser completados por cada projeto-cópia.

> **Treinamento.** Esta é a cópia do `boilerplate-CD` do ODIN para os treinamentos de Ciência de
> Dados, com três ajustes: o `CODEOWNERS` aponta para o time `validadores` da org, existe
> `context/sessions/` (onde ficam as sessões e atas das skills do `skills-navegador`) e o
> `CLAUDE.md` tem um bloco para quem usa o Claude no navegador. O resto é igual ao boilerplate do
> núcleo, e o `docs/` vale como está. Passo a passo para a equipe: **trilha do trainee** e
> **setup do ambiente (Windows)** no `manual-treinamento`.
>
> No Windows, onde este README diz `python3`, use `python`. Sem Databricks: na pergunta do
> `tools/init.py`, responda **N**.

<!-- PREENCHER: uma frase dizendo o que este projeto faz. -->

## 👋 Chegou agora? Comece aqui

Se você é analista e nunca viu este padrão, leia o
**[Guia do Analista](docs/GUIA-DO-ANALISTA.md)** — ele te leva, narrado e sem pressupor
nada, da cópia do repositório até o primeiro pipeline rodando.

## O que é

Este projeto nasceu como **cópia independente** do esqueleto canônico. A documentação
está separada pela natureza: o **manual do molde** (como o esqueleto é composto e como
se mexe nele) mora em [`docs/`](docs/); o **contexto deste projeto** (negócio, dados,
domínio), preenchido ao longo do tempo, mora em [`.claude/`](.claude/). O ponto de
entrada único, para IA ou pessoa, é o [`CLAUDE.md`](CLAUDE.md).

## Como começar (a partir do esqueleto)

1. **Copie** o esqueleto para um novo diretório (cópia independente, sem vínculo com o
   esqueleto original).
2. **Rode o scaffolder uma única vez** (usa só a stdlib — roda ANTES do `uv sync`):
   ```bash
   python3 tools/init.py
   ```
   Ele pergunta o toggle Databricks (S/N), poda `platform/` se Não, define o modo dos
   `pipeline/entrypoints/` e nomeia o projeto. Ao terminar, se autodestrói.
3. **Instale as dependências:**
   ```bash
   uv sync
   ```
4. Comece a trabalhar dentro da estrutura pronta. Passo a passo completo na skill
   [`iniciar-projeto-novo-a-partir-do-esqueleto`](.claude/skills/iniciar-projeto-novo-a-partir-do-esqueleto/SKILL.md).

## Como rodar

O pipeline é dirigido pelo config do modelo (Rule 07). Execução local:

```bash
uv run python pipeline/entrypoints/run_local.py --config pipeline/config/<modelo>.yaml
# saída: run_id: ... / métricas: {'accuracy': ..., 'f1': ...}
```

Antes de commitar, rode o mesmo conjunto do CI:

```bash
python3 tools/check.py     # contrato (barra o merge) + conselho (só avisa)
```

<!-- PREENCHER: se este projeto tem um comando/entrypoint próprio além do acima, descreva-o. -->

## CI: o que barra e o que só avisa

| Job | Verifica | Se falhar |
|---|---|---|
| `contrato` | Estrutura essencial (`CLAUDE.md`, `.claude/settings.json` com o plugin do núcleo, `.github/CODEOWNERS`, `context/README.md`, `context/99_conclusoes/`, `pyproject.toml`); nada versionado nas pastas de dados de `pipeline/data/` (`raw`, `interim`, `processed`, `external`); nenhum `.env` nem `CLAUDE.local.md` versionado; skills que o Claude Code carrega; erros de Python que quebram (sintaxe, nome indefinido); `pytest`; manifesto em sync (Rules 02 e 03) | **Barra o merge** |
| `conselho` | Estrutura recomendada; estilo (`ruff check`, `ruff format`); raiz mínima (Rule 04); MLflow centralizado (Rule 01); plataforma isolada (Rule 06); convenções de nome; arquivos de `context/` acima de 8KB | **Só avisa** no PR |

Arquivo ou pasta nova, inclusive na raiz, não barra o merge: vira aviso, e quem decide a exceção é o coordenador, ao aprovar o PR. As rules de [`docs/rules/`](docs/rules/) continuam valendo; o motivo da divisão está na decisão 13 de [`docs/context/decisoes.md`](docs/context/decisoes.md).

## Onde ficam as regras

**A leitura de [`docs/rules/`](docs/rules/) é obrigatória antes de qualquer alteração.**

Documentação do **molde** (em [`docs/`](docs/)):

- Contexto e arquitetura: [`docs/context/`](docs/context/)
- Rules (o que pode/não pode): [`docs/rules/`](docs/rules/)
- Guias por etapa: [`docs/guides/`](docs/guides/)
- Decisões de arquitetura: [`docs/context/decisoes.md`](docs/context/decisoes.md)
- Skills invocáveis (adicionar modelo, fonte, dependência, iniciar projeto…): [`.claude/skills/`](.claude/skills/)

Contexto **deste projeto** (em [`.claude/`](.claude/), a preencher): problema de
negócio, dados, glossário do domínio e decisões da cópia.

> `.claude/` é uma pasta oculta — use `ls -a` para enxergá-la.

## Estrutura

Ver [`docs/context/arquitetura.md`](docs/context/arquitetura.md) para a estrutura-alvo
completa e os invariantes.

---

<!-- PREENCHER: seção de contato/responsáveis do projeto, se aplicável. -->
