# Exercicio 01 - Carmem Sandiego

## Visao geral

Uma ladra internacional escapou. Existem 2000 suspeitos em uma planilha cheia de erros. Limpe os dados, descubra quem e a culpada com SQL e conte a historia em um dashboard.

## Arquivos

- [Enunciado](enunciado.md)
- [Como os dados sao gerados](como-gerar-dados.md)
- [Passo a passo](passo-a-passo.md)
- [Gabarito](gabarito/README.md)

## Dados para download

- CSV sujo: [`dados/suspeitos_sujo.csv`](dados/suspeitos_sujo.csv)
- Copia: [`../../_comum/dados/ex01_suspeitos_sujo.csv`](../../_comum/dados/ex01_suspeitos_sujo.csv)
- Para regenerar: `python _comum/scripts/ex01_gerar_dados.py`

## Pilares treinados

| Pilar | Como e treinado |
|-------|-----------------|
| 1 Alicerce | funcoes de texto, PROCV e Tabela Dinamica na limpeza |
| 2 Trabalho Sujo | duplicatas, nulos, formatos de data, valor e booleano |
| 3 Linguagem | WHERE, IN, BETWEEN, LIKE, AND/OR para reduzir 2000 a 1 |
| 4 Bussola | media x mediana do valor gasto em viagens |
| 5 Filtro Critico | correlacao x causalidade e eixos honestos |
| 6 Traducao | "quem e suspeito?" vira numeros e um funil |
| 7 Vitrine | dashboard enxuto com cartoes, barras e filtros |
| 8 Fator Ouro | resumo executivo em 3 passos |