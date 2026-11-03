# O case: Manutenção Preditiva para a MaBiYama

> Case **simulado** de treinamento. O cliente é fictício. Fonte: a proposta comercial
> "Manutenção Preditiva Aplicada à Frota Industrial" (MaBiYama & Poli Júnior).

## Situação

A MaBiYama (bombas e sistemas hidráulicos) opera uma frota de **100 máquinas
industriais** de **4 modelos**, com idades entre **0 e 20 anos**. Cada máquina registra,
**a cada hora**, quatro leituras de sensores, além de alertas de erro, histórico de
manutenção e histórico de falhas de componentes. Esses dados existem há anos, mas
ninguém usa: a manutenção segue um **calendário fixo** e, quando uma peça quebra antes
do previsto, a linha de produção para.

O que o cliente disse:

- "A gente troca peça que estava boa e deixa quebrar a que estava ruim."
- "Cada parada não planejada desorganiza a semana inteira da produção."
- "Os sensores apitam o tempo todo, ninguém sabe mais o que é alerta de verdade."
- "Eu queria chegar de manhã e saber em qual máquina mexer primeiro."

## Complicação

Em um ano, a frota registrou **mais de 700 falhas de componentes**. Cada uma significou
parada não planejada, técnico acionado às pressas e peça comprada em caráter de
urgência. Ao mesmo tempo, a manutenção por calendário troca peças ainda boas. Os dados
que permitiriam antecipar as falhas estão espalhados em fontes que nunca foram cruzadas.

- **Custo:** uma parada não planejada custa muito mais que uma manutenção programada.
- **Alertas ignorados:** muito erro, nenhuma priorização.
- **Falta de visibilidade:** não se sabe quais máquinas e peças concentram o risco.
- **Estoque no escuro:** a compra de peças não acompanha o risco real de falha.

## O que foi vendido

Integrar as fontes numa visão única por máquina e desenvolver um modelo de Machine
Learning que, **toda manhã às 05:00**, estima a **probabilidade de cada peça de cada
máquina falhar até as 06:00 do dia seguinte**.

O resultado é entregue numa **interface web**: a equipe sobe os dados do dia e recebe a
lista de máquinas e peças priorizadas para manutenção, junto com um diagnóstico da
qualidade dos dados recebidos.

```
Base bruta (6 tabelas) → Limpeza e integração → Base de modelagem (máquina × dia)
    → Modelo preditivo → Interface web (previsão + análise da base) → Lista de prioridade
```

## Entregas

| Entrega | Etapa | Onde fica no repositório |
|---|---|---|
| Dicionário de dados, unidade de previsão e métrica validados | 1 | `docs/dicionario_de_dados.md` |
| Base integrada, script de limpeza e relatório de qualidade | 2 | `src/limpeza.py`, `scripts/limpar.py`, `docs/relatorio_qualidade.md` |
| Notebook de análise exploratória (Report 1) | 3 | `notebooks/01_analise_exploratoria.ipynb` |
| Notebook de modelagem com comparativo e modelo final | 4 | `notebooks/02_modelagem.ipynb`, `models/modelo.joblib` |
| Interface web publicada | 5 | `app/app.py` |
| Recomendação de política de manutenção (Report 2) | 6 | `docs/politica_manutencao.md`, `docs/reports/` |

## Prazo e alinhamentos

- **17 dias úteis** (~3,5 semanas). Etapas: 1 dia · 3 · 3 · 7 · 2 · 1.
- **Report 1** ao fim da Análise Exploratória. **Report 2** na Apresentação Final.
- Equipe: 2 consultores de dados + 1 validador técnico (aprova os PRs).
