# Arquitetura

## Estrutura-alvo do repo

```
.
├── CLAUDE.md                 ← ponto de entrada ÚNICO (IA ou pessoa); aponta para docs/ e .claude/
├── README.md
├── *.pdf                     ← manuais do molde (exceção editorial à raiz mínima — decisão 11)
├── pyproject.toml            ← FONTE ÚNICA de dependências (uv)
├── uv.lock
├── .gitignore
├── .github/workflows/        ← CI: lint, testes, check de raiz mínima, check de manifesto em sync
├── docs/                     ← MANUAL DO MOLDE — igual em todo projeto do núcleo
│   ├── context/              ← o que é o esqueleto, arquitetura, decisões, glossário
│   ├── rules/                ← comportamento: o que se pode e não pode fazer (verificado no CI)
│   ├── guides/               ← 1 guia por etapa: config, data, models, common, entrypoints, platform
│   └── GUIA-DO-ANALISTA.md   ← onboarding narrado, da cópia ao primeiro pipeline
├── .claude/                  ← CAPACIDADE DESTE PROJETO — o que a IA executa (pasta oculta; decisão 12)
│   ├── skills/               ← Skills invocáveis: molde (adicionar modelo…) + do projeto (decisão 10)
│   ├── rules/                ← 00-nucleo.md (base) + regras do projeto (via @import no CLAUDE.md)
│   ├── agents/ hooks/        ← subagentes e scripts de evento específicos do projeto
│   └── settings.json         ← permissões e hooks (commitado; settings.local.json é local)
├── context/                  ← TRABALHO DESTE PROJETO — vault cronológico (decisão 12)
│   ├── NN_<etapa>/           ← uma pasta por etapa: decisões (ADR-lite) + contextos técnicos
│   ├── glossario.md          ← termos do NEGÓCIO deste projeto
│   └── 99_conclusoes/        ← entregáveis, ferramentas, fluxo, aprendizados → core-knowledgebase
├── tools/
│   └── init.py               ← roda 1x após copiar: pergunta o toggle, poda platform/, nomeia o projeto
├── tests/                    ← testes do molde
├── pipeline/                 ← ★ ONDE O ANALISTA TRABALHA (decisão 9)
│   ├── config/               ← config por modelo (pipeline config-driven)
│   ├── notebooks/            ← notebooks (.ipynb): análise exploratória, tratamento, merges
│   ├── data/                 ← implementações concretas da interface de dados (data/sources/)
│   ├── models/<modelo>/      ← anatomia OBRIGATÓRIA de 5 arquivos por modelo:
│   │   ├── prepare_data.py
│   │   ├── build_model.py
│   │   ├── train.py
│   │   ├── evaluate_model.py
│   │   └── orchestrator.py   ← espinha dorsal + ÚNICO ponto de contato com MLflow
│   ├── common/               ← lógica compartilhada entre modelos (contratos, tracking, splits)
│   └── entrypoints/          ← launchers finos (modo local/serverless, conforme toggle)
└── platform/                 ← infra opcional; SÓ sobrevive se toggle = SIM (fica FORA de pipeline/)
    ├── databricks.yml
    ├── resources/
    ├── MLProject
    └── conda.yaml            ← GERADO a partir do pyproject, nunca escrito à mão
```

## Invariante central

**O núcleo é IDÊNTICO com ou sem Databricks.** O pipeline
`config → prepare → build → train → evaluate → orchestrator` não depende de
plataforma. `platform/` é a casca inteira que o toggle liga/desliga. Nada do núcleo
importa de `platform/`; se o toggle for Não, o repo tem que rodar com `platform/`
inexistente.

MLflow é **OBRIGATÓRIO sempre**. O toggle decide apenas ONDE ele guarda os dados
(local vs. Databricks), nunca SE ele existe.

## Princípio da raiz mínima

A raiz é uma **vitrine de ponteiros**, não um depósito. Só fica na raiz o que
tecnicamente não funciona em outro lugar. O critério é **requisito técnico**, não
gosto (com as exceções registradas — ver decisões 11 e 12). A documentação do molde mora
em `docs/`; o registro do trabalho do projeto, em `context/`; a capacidade (rules,
skills, agents, hooks), em `.claude/`.

### Por que cada arquivo da raiz não pode sair de lá

| Arquivo                  | Motivo técnico (por que não pode sair da raiz)                         |
| ------------------------ | --------------------------------------------------------------------- |
| `pyproject.toml` / `uv.lock` | O `uv` só procura na raiz.                                         |
| `.gitignore`             | O Git só lê neste caminho exato.                                      |
| `.github/workflows/`     | O GitHub Actions só executa a partir daqui.                          |
| `README.md`              | É o que o GitHub renderiza na página do repo.                        |
| `CLAUDE.md`              | Tool discovery: ponto de entrada único; é como uma IA que clona o repo descobre sozinha que há um padrão a seguir. |
| `*.pdf` (os 2 manuais)   | **Exceção editorial, não técnica** (decisão 11): ficam na vitrine porque é onde quem abre o repo os encontra. Não é precedente. |
| `context/`               | Vault de trabalho do projeto (decisão 12): etapas + conclusões, destilado para a `core-knowledgebase` ao final. Caminho fixado pelo padrão do núcleo — é o contrato de interoperabilidade entre os repos de projeto. |
| `.claude/`               | Camada de **capacidade** (decisão 12): o Claude Code só carrega rules/skills/agents/hooks/settings deste caminho exato. |

**Qualquer outro arquivo na raiz é violação da regra.** A allowlist viva é a de
`tools/check_root.py`, verificada pelo CI.

## Anatomia de 5 arquivos (por modelo)

Todo modelo em `pipeline/models/<nome>/` tem exatamente:

1. `prepare_data.py`   — prepara os dados (pede o dado à interface `DataSource`, nunca sabe de onde vem).
2. `build_model.py`    — constrói o modelo.
3. `train.py`          — treina.
4. `evaluate_model.py` — avalia.
5. `orchestrator.py`   — espinha dorsal + **único ponto de contato com MLflow** (via `pipeline/common/tracking.py`).

## Interface de dados neutra

Um `Protocol` `DataSource` definido em `pipeline/common/`, com implementações concretas
(`SparkTableSource`, `ParquetSource`, `SQLSource`) em `pipeline/data/sources/`, escolhidas
via config. O código de preparação só pede o dado à interface; nunca sabe de onde ele vem.
