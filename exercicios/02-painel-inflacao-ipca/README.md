# Exercício 02 - Painel de inflação (IPCA / IBGE)

Tipo: estudo guiado com dados reais. Não há culpado nem gabarito único: o objetivo é comparar grupos e períodos, mostrar gráficos, citar a fonte e chegar a uma conclusão que os números sustentem.

## Visão geral

O IPCA é o índice oficial de inflação do Brasil, calculado pelo IBGE. Neste exercício você baixa o IPCA por grupo de produtos e serviços (alimentação, habitação, transportes etc.), organiza os dados em um banco normalizado, responde perguntas em SQL e monta um painel no Power BI.

## Arquivos

- [Enunciado](enunciado.md)
- [Como os dados são obtidos](como-gerar-dados.md)
- [Passo a passo](passo-a-passo.md)
- [Gabarito](gabarito/README.md)

## Dados

- CSV: `dados/ipca_grupos.csv` (criado pelo script; não vem pronto)
- Cópia: `../../_comum/dados/ex02_ipca_grupos.csv`
- Para baixar: `py _comum/scripts/ex02_baixar_ipca.py`
- Fonte: IBGE, Sistema IBGE de Recuperação Automática (SIDRA), tabela 7060 (IPCA, a partir de janeiro de 2020)

## Pilares treinados

| Pilar | Como é treinado |
|-------|-----------------|
| 1 Alicerce | conferir o acumulado anual com fórmula no Excel e montar a Tabela Dinâmica grupo x ano |
| 2 Trabalho Sujo | ETL de uma API pública: valores "sem dado", prefixos nos nomes, modelo normalizado (dimensão e fato) |
| 3 Linguagem | JOIN, GROUP BY, funções de janela (RANK) e acumulado composto em SQL |
| 4 Bússola | média, mediana e desvio padrão da variação mensal de cada grupo |
| 5 Filtro Crítico | não somar percentuais, escolher o período antes de ver os números, eixos honestos |
| 6 Tradução | transformar "o que está pesando no bolso?" em acumulado, impacto (peso x variação) e volatilidade |
| 7 Vitrine | painel de uma página com poucos visuais, fonte e conclusão |
| 8 Fator Ouro | resumo executivo em 3 passos: contexto, descoberta, recomendação |
