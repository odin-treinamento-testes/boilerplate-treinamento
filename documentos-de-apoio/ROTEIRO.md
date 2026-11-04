# Roteiro do projeto: as 6 etapas

Cada etapa tem: o objetivo, o que fazer, **onde mexer no repositório** e o critério de
**pronto**. Uma etapa só está pronta quando o validador aprovou o entregável dela.

Prazo total: **17 dias úteis**.

| Etapa | Dias | Entregável |
|---|---|---|
| [1. Imersão no Contexto](#etapa-1--imersão-no-contexto-1-dia) | 1 | Dicionário de dados, unidade de previsão e métrica |
| [2. Limpeza e Integração](#etapa-2--limpeza-e-integração-dos-dados-3-dias) | 3 | Script de limpeza + relatório de qualidade |
| [3. Análise Exploratória](#etapa-3--análise-exploratória-3-dias) | 3 | Notebook de EDA → **Report 1** |
| [4. Modelagem Preditiva](#etapa-4--modelagem-preditiva-7-dias) | 7 | Notebook de modelagem + modelo final |
| [5. Interface Web](#etapa-5--interface-web-2-dias) | 2 | Aplicação publicada com link |
| [6. Validação e Apresentação](#etapa-6--validação-e-apresentação-final-1-dia) | 1 | Política de manutenção → **Report 2** |

---

## Etapa 1 – Imersão no Contexto (1 dia)

**Objetivo:** transformar o pedido do cliente numa pergunta de ciência de dados clara,
com unidade de previsão e métrica definidas, **antes** de qualquer análise.

**O que fazer**
- [ ] Ler o [`case.md`](case.md) e preparar as perguntas do kickoff.
- [ ] Kickoff com o cliente. Levantar: o que conta como falha, com quanta antecedência
      precisam saber, quanto custa uma parada e quanto custa uma manutenção programada.
- [ ] Reconhecer as tabelas: o que cada linha representa, a chave de cada uma, como se
      relacionam.
- [ ] Configurar o ambiente (ver o [README](../README.md#configuração-do-ambiente-uma-vez-por-máquina)).
- [ ] Ajustar [`src/config.py`](../src/config.py) aos nomes reais de arquivos e colunas.

**Onde mexer:** `docs/dicionario_de_dados.md`, `src/config.py`, `docs/decisoes.md`.

**Pronto quando:** o dicionário está preenchido, a unidade de previsão e a métrica estão
escritas e validadas com o cliente, e `python -m pytest` passa.

---

## Etapa 2 – Limpeza e Integração dos Dados (3 dias)

**Objetivo:** construir uma base única e confiável, com um tratamento **reprodutível**
que possa ser reaplicado a qualquer nova base do cliente.

**O que fazer**
- [ ] Rodar `python scripts/limpar.py` e ler o `data/processed/diagnostico_bruto.csv`.
- [ ] Procurar: duplicatas, valores impossíveis, lacunas na série, inconsistências de
      formato e de nomenclatura, máquinas sem cadastro.
- [ ] Para cada problema: escrever o tratamento em `src/limpeza.py` (e a verificação em
      `src/qualidade.py`, se ainda não existir).
- [ ] Justificar cada tratamento em `docs/relatorio_qualidade.md`.
- [ ] Escrever um teste para cada regra de limpeza importante em `tests/`.

**Onde mexer:** `src/limpeza.py`, `src/qualidade.py`, `src/config.py` (faixas dos
sensores), `docs/relatorio_qualidade.md`, `tests/test_projeto.py`.

**Regra:** a limpeza é **script**, não notebook. Pode explorar num notebook, mas o
tratamento final mora em `src/limpeza.py`.

**Pronto quando:** `python scripts/limpar.py` roda do zero na base bruta e o relatório
explica cada tratamento.

---

## Etapa 3 – Análise Exploratória (3 dias)

**Objetivo:** entender o que acontece com uma máquina antes de uma falha e levantar as
hipóteses que vão orientar a modelagem.

**O que fazer** (cada item é uma seção do notebook)
- [ ] Comportamento dos sensores nas horas e dias que antecedem cada falha, por peça.
- [ ] Cruzamento dos tipos de erro com as falhas registradas.
- [ ] Ciclos de manutenção e de falha por modelo e idade de máquina.
- [ ] Desbalanceamento entre dias com e sem falha.
- [ ] Lista de hipóteses para a modelagem.
- [ ] Slides do **Report 1** em `docs/reports/`.

**Onde mexer:** `notebooks/01_analise_exploratoria.ipynb`, `docs/reports/`.

**Pronto quando:** o notebook roda do início ao fim (*Restart & Run All*), toda seção
tem conclusão escrita e o Report 1 foi apresentado.

---

## Etapa 4 – Modelagem Preditiva (7 dias)

**Objetivo:** encontrar, por comparação justa entre diferentes abordagens, o modelo que
melhor antecipa a falha de cada peça.

**O que fazer**
- [ ] Entender a base de modelagem pronta em `src/features.py`: uma linha por máquina
      por dia, com o que se sabe até as 05:00, e os alvos `falha_comp1`..`falha_comp4`.
- [ ] Criar features por janela de tempo (sensores, erros, manutenção, perfil da
      máquina) em `src/features.py`, a partir das hipóteses da EDA.
- [ ] Definir a validação temporal (data de corte, ou vários cortes) e justificar.
- [ ] Comparar algoritmos **na mesma validação e com a mesma métrica**, a partir de um
      baseline.
- [ ] Analisar os erros e justificar o modelo escolhido.
- [ ] Colocar o vencedor em `scripts/treinar.py` e rodar para gerar `models/modelo.joblib`.

**Onde mexer:** `src/features.py`, `notebooks/02_modelagem.ipynb`, `scripts/treinar.py`.

**Cuidado com vazamento:** nenhuma feature pode usar dado registrado depois das 05:00
do dia da previsão. O teste `test_features_nao_usam_o_futuro` ajuda a pegar isso.

**Pronto quando:** o notebook mostra o comparativo e a justificativa, e o modelo final
está salvo e versionado.

---

## Etapa 5 – Interface Web (2 dias)

**Objetivo:** colocar o modelo nas mãos do cliente, numa ferramenta que recebe a base
bruta e devolve a prioridade de manutenção sem depender da equipe técnica.

**O que fazer**
- [ ] Rodar `streamlit run app/app.py` e testar com a base bruta.
- [ ] Aba **Previsão**: upload → limpeza → modelo → lista priorizada (já funciona; ajustar).
- [ ] Aba **Análise da base**: diagnóstico de qualidade + sensores e erros por máquina
      (já funciona; acrescentar o que a EDA mostrou ser útil).
- [ ] Testar bases fora do padrão (arquivo faltando, coluna com outro nome, data
      errada): a mensagem tem que dizer o que corrigir.
- [ ] Publicar no Streamlit Community Cloud (ver o [README](../README.md#publicar-a-interface-web)).

**Onde mexer:** `app/app.py` (só a tela; a lógica fica em `src/`).

**Pronto quando:** o link público abre, aceita a base e devolve a lista.

---

## Etapa 6 – Validação e Apresentação Final (1 dia)

**Objetivo:** provar o valor da solução numa base que o modelo nunca viu e traduzir o
resultado em decisão de negócio.

**O que fazer**
- [ ] Rodar a interface com a base nova do cliente (demonstração ao vivo).
- [ ] Definir a política: a partir de que probabilidade intervir, e a economia estimada
      em R$ (`modelo.custo_da_politica`, seção 6 do notebook de modelagem).
- [ ] Preencher `docs/politica_manutencao.md`.
- [ ] Slides do **Report 2** em `docs/reports/`, em linguagem de negócio.

**Pronto quando:** o Report 2 foi apresentado e notebooks, código e documentos estão na
`main`.
