# Manutenção Preditiva – MaBiYama (treinamento de Ciência de Dados)

Repositório-base dos treinamentos de Ciência de Dados do NDados (Poli Júnior). Cada dupla
de trainees recebe uma cópia dele e desenvolve, em 17 dias úteis, um projeto completo de
manutenção preditiva para a **MaBiYama**, um cliente **fictício**: da imersão no
problema até um modelo publicado numa interface web.

> **Objetivo do projeto:** toda manhã, às 05:00, estimar a probabilidade de cada peça de
> cada máquina falhar até as 06:00 do dia seguinte e entregar à equipe do cliente uma
> lista de manutenção priorizada.

## Comece por aqui

1. Leia o [case](documentos-de-apoio/case.md): a situação do cliente, o que foi vendido
   e as entregas.
2. Leia o [roteiro](documentos-de-apoio/ROTEIRO.md): as 6 etapas, o que fazer em cada
   uma e o critério de **pronto**.
3. Configure o ambiente (seção abaixo).

## Estrutura do repositório

```
.
├── documentos-de-apoio/
│   ├── case.md                          # contexto do cliente e escopo vendido
│   └── ROTEIRO.md                       # as 6 etapas, com checklist e critério de pronto
├── ETL/
│   ├── extracao.py                      # leitura da base bruta do cliente
│   ├── tratamento-geral.py              # limpeza e integração (reprodutível)
│   └── tratamento-pre-exploratoria.py   # ajustes específicos para a EDA
├── dados/
│   ├── extraídos/                       # base bruta, como veio do cliente
│   └── tratados/                        # base limpa e integrada
├── notebooks/
│   ├── 01_analise_exploratoria.ipynb    # Etapa 3 (Report 1)
│   └── 02_modelagem.ipynb               # Etapa 4
├── modelos/                             # modelo final treinado
├── tests/                               # testes que o CI roda (python -m pytest)
├── requirements.txt                     # todas as dependências do projeto
└── .github/
    └── workflows/ci.yml                 # verificações automáticas
```

### Fluxo dos dados

```
dados/extraídos ──► ETL/extracao.py ──► ETL/tratamento-geral.py ──► dados/tratados
                                                                        │
                       ETL/tratamento-pre-exploratoria.py ◄─────────────┤
                                     │                                  │
                                     ▼                                  ▼
                  notebooks/01_analise_exploratoria     notebooks/02_modelagem ──► modelos/
                                                                                     │
                                                                                     ▼
                                                                             interface web
```

- **`ETL/`** guarda o tratamento em **scripts**, não em notebooks. Pode explorar num
  notebook, mas a regra de limpeza final mora aqui para poder ser reaplicada a qualquer
  base nova do cliente.
- **`notebooks/`** já vem com o esqueleto de cada etapa. Mantenha o layout
  *título → código → conclusão* em todas as células.
- **`dados/`** só existe na sua máquina: os arquivos do cliente **nunca** vão para o git
  (veja [Regras](#regras-do-repositório)).

## Configuração do ambiente (uma vez por máquina)

Pré-requisitos: Python 3.11 e git.

```bash
git clone <url-do-repositório-da-sua-equipe>
cd <pasta-do-repositório>

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Depois, coloque os arquivos da base bruta recebidos do cliente em `dados/extraídos/`.

> No macOS/Linux, se `python` não existir, use `python3`.

Precisa de uma biblioteca nova? Adicione-a ao [`requirements.txt`](requirements.txt), uma
por linha, **no mesmo commit** que passa a usá-la.

## Como trabalhar

A equipe trabalha direto na `main`.

1. Antes de começar, traga o que a sua dupla já subiu: `git pull`.
2. Desenvolva seguindo o [roteiro](documentos-de-apoio/ROTEIRO.md).
3. Antes de subir:
   ```bash
   python -m pytest
   ```
   e rode cada notebook alterado do início ao fim (*Kernel → Restart & Run All*).
4. Commit e push na `main`:
   ```bash
   git add <arquivos>
   git commit -m "<o que mudou>"
   git push
   ```
   Se o push for recusado, a sua dupla subiu algo antes: `git pull` e push de novo.
5. Ao fim de cada etapa, avise o validador. **Uma etapa só está pronta quando o validador
   aprovou o entregável dela.**

### O que o CI verifica

A cada push na `main`, o GitHub Actions ([`ci.yml`](.github/workflows/ci.yml)):

| Verificação | Se falhar |
|---|---|
| Nenhum arquivo `.csv`, `.xlsx` ou `.parquet` versionado | O commit fica com ❌ no GitHub: corrija e suba de novo |
| `python -m pytest` passa | O commit fica com ❌ no GitHub: corrija e suba de novo |

## Regras do repositório

- **Dados do cliente nunca entram no git.** O [`.gitignore`](.gitignore) ignora `.csv`,
  `.xlsx` e `.parquet`, e o CI acusa se algum escapar.
- **Segredos nunca entram no git** (`.env` e afins já estão ignorados).
- **Limpeza é script, não notebook.** O tratamento final mora em `ETL/`.
- **Notebooks precisam rodar do zero.** Nada de célula que depende de estado escondido.
- **Sem vazamento de informação:** nenhuma feature pode usar dado registrado depois das
  05:00 do dia da previsão.
- **Toda decisão relevante é registrada** (tratamento escolhido, métrica, validação,
  modelo) junto da entrega da etapa.

## Etapas e entregas

| Etapa | Dias | Entregável |
|---|---|---|
| 1. Imersão no Contexto | 1 | Dicionário de dados, unidade de previsão e métrica |
| 2. Limpeza e Integração | 3 | Scripts em `ETL/` + relatório de qualidade |
| 3. Análise Exploratória | 3 | `notebooks/01_analise_exploratoria.ipynb` → **Report 1** |
| 4. Modelagem Preditiva | 7 | `notebooks/02_modelagem.ipynb` + modelo em `modelos/` |
| 5. Interface Web | 2 | Aplicação Streamlit publicada com link |
| 6. Validação e Apresentação | 1 | Política de manutenção → **Report 2** |

Detalhes de cada etapa no [roteiro](documentos-de-apoio/ROTEIRO.md).

## Publicar a interface web

A interface é feita em [Streamlit](https://streamlit.io) (já incluído no
`requirements.txt`). Para testar localmente:

```bash
streamlit run <caminho-do-app>.py
```

Para publicar no [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Garanta que o app e o modelo final estão na `main`.
2. Entre em share.streamlit.io com a conta do GitHub.
3. **New app** → escolha o repositório, a branch `main` e o arquivo do app.
4. Publique e coloque o link gerado na entrega da Etapa 5.

A tela deve ficar só no app; a lógica (limpeza, features, previsão) fica nos scripts do
projeto, para que a interface aplique exatamente o mesmo tratamento do treino.

## Equipe

- 2 consultores de dados (a dupla de trainees)
- 1 validador técnico, que aprova o entregável de cada etapa
