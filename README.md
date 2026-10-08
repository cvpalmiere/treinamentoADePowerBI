# Exercicios de Analise de Dados

Repositorio de pratica integrada em tres ferramentas: Excel, SQL e Power BI.

Fluxo de cada exercicio:

    CSV sujo (gerado por script Python)
      -> limpeza no Excel
      -> importacao no PostgreSQL
      -> investigacao em SQL
      -> dashboard no Power BI

## Estrutura

- `_comum/templates/` modelos de README, enunciado, como-gerar-dados e passo-a-passo
- `_comum/scripts/` scripts Python que geram os CSVs sujos
- `_comum/dados/` copia dos CSVs gerados, prontos para download
- `_comum/docs/` convencoes e guia dos 8 pilares
- `exercicios/` uma subpasta por questao

## Exercicios

| No | Titulo | Pilares principais |
|----|--------|--------------------|
| 01 | [Carmem Sandiego](exercicios/01-carmem-sandiego/README.md) | 1, 2, 3, 4, 5, 6, 7, 8 |

## Como comecar

1. Instale Python, Git e Power BI Desktop.
2. Crie o ambiente: `python -m venv .venv`, ative-o e rode `pip install -r requirements.txt`.
3. Gere o CSV do exercicio desejado (veja o `como-gerar-dados.md` da questao).
4. Siga o `passo-a-passo.md`.

## Documentacao

- [Convencoes](_comum/docs/convencoes.md)
- [Guia dos 8 pilares](_comum/docs/guia-8-pilares.md)