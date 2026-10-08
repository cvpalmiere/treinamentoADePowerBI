# Dashboard - Exercicio 01

## Pergunta que o dashboard responde

Quem e a suspeita e como as pistas reduziram 2000 pessoas a 1?

## Medidas DAX

    Total Suspeitos = COUNTROWS(suspeitos)

    Pct Tatuados =
    DIVIDE(
        CALCULATE(COUNTROWS(suspeitos), suspeitos[tem_tatuagem] = TRUE()),
        COUNTROWS(suspeitos)
    )

    Media Gasto = AVERAGE(suspeitos[valor_gasto_viagens])
    Mediana Gasto = MEDIAN(suspeitos[valor_gasto_viagens])

## Layout (uma pagina)

1. Topo: 3 cartoes (Total Suspeitos, Pct Tatuados, Mediana Gasto).
2. Centro esquerdo: grafico de barras horizontais, suspeitos por profissao, eixo comecando em zero.
3. Centro direito: histograma de altura (agrupe altura_cm em faixas de 5).
4. Base: grafico de funil com a contagem apos cada pista, ou tabela com os numeros do funil da query SQL.
5. Lateral: segmentacoes de ultima_cidade e cor_cabelo.
6. Titulo da pagina com o insight: "Uma unica suspeita satisfaz as 8 pistas".

## Escolhas deliberadas (Pilar 7)

- Sem grafico de pizza (12 profissoes ficam ilegiveis).
- Uma cor de destaque so para a suspeita; o resto em cinza.
- Mediana ao lado da media, para o leitor ver a diferenca.

## Resumo executivo (Pilar 8)

- Contexto: 2000 suspeitos, 8 pistas, uma ladra.
- Descoberta: aplicadas todas as pistas, resta uma pessoa, Helena Montenegro Teixeira, guia turistico com ultima passagem por Lisboa.
- Recomendacao: priorizar a localizacao dela em Lisboa e verificar a unica coincidencia com as pistas de alto valor.