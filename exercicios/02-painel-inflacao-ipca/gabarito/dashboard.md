# Painel - Exercício 02

## Pergunta que o painel responde

O que anda pesando no custo de vida e isso mudou entre [período A] e [período B]?

## Modelo

Duas tabelas: `dim_grupo` (10 linhas) e `ipca_mensal` (uma linha por mês e grupo), ligadas por `id_grupo` (muitos para um).

## Medidas DAX (Modelagem > Nova medida)

    Var Mensal = AVERAGE(ipca_mensal[var_mensal])

    Var 12m = AVERAGE(ipca_mensal[var_12m])

    IPCA 12m Ultimo Mes =
    VAR ultimo = CALCULATE(MAX(ipca_mensal[mes]), ALL(ipca_mensal))
    RETURN
        CALCULATE(
            AVERAGE(ipca_mensal[var_12m]),
            ipca_mensal[mes] = ultimo,
            dim_grupo[nome] = "Índice geral"
        )

    Acumulado Periodo =
    VAR soma_ln =
        SUMX(
            ipca_mensal,
            IF(ISBLANK(ipca_mensal[var_mensal]), 0, LN(1 + ipca_mensal[var_mensal] / 100))
        )
    RETURN
        IF(COUNTROWS(ipca_mensal) = 0, BLANK(), (EXP(soma_ln) - 1) * 100)

    Diferenca vs Geral =
    VAR geral = CALCULATE([Acumulado Periodo], dim_grupo[nome] = "Índice geral")
    RETURN [Acumulado Periodo] - geral

    Impacto pp Ultimo Mes =
    VAR ultimo = CALCULATE(MAX(ipca_mensal[mes]), ALL(ipca_mensal))
    RETURN
        CALCULATE(
            SUMX(ipca_mensal, ipca_mensal[peso_mensal] * ipca_mensal[var_mensal] / 100),
            ipca_mensal[mes] = ultimo
        )

    Media Mensal = AVERAGE(ipca_mensal[var_mensal])
    Mediana Mensal = MEDIAN(ipca_mensal[var_mensal])
    Desvio Mensal = STDEV.S(ipca_mensal[var_mensal])

`Acumulado Periodo` compõe os percentuais (nunca soma), então respeita a segmentação de período.

## Layout (uma página)

1. Título com o achado, por exemplo: "Alimentação e [grupo] puxaram a inflação em [período]".
2. Segmentação de `mes` (intervalo) no canto: ela controla o período do acumulado.
3. Três cartões: `IPCA 12m Ultimo Mes`, `Acumulado Periodo` (filtrado em "Índice geral") e `Impacto pp Ultimo Mes` do grupo de maior impacto, ou o desvio do geral.
4. Gráfico de linhas: eixo `mes`, valor `Var 12m`, filtro visual `nome` = "Índice geral". Título com unidade (%).
5. Barras horizontais: `grupo` x `Acumulado Periodo`, ordenado do maior para o menor, eixo começando em zero. Destaque o Índice geral com outra cor.
6. Barras horizontais: `grupo` x `Impacto pp Ultimo Mes` (sem o Índice geral).
7. Caixa de texto no rodapé: **Fonte** (IBGE, SIDRA, tabela 7060, acesso em [data]) e **Conclusão** (3 frases).

## Página 2 opcional: comparar grupos e períodos

Matriz com `grupo` nas linhas, `mes` nas colunas e `Var Mensal` nos valores, com formatação condicional de cor (escala de calor). Mostra de uma vez em quais meses cada grupo disparou.

## Escolhas deliberadas (Pilar 7)

- Sem pizza: 9 fatias são ilegíveis.
- Uma cor neutra para os grupos e uma cor de destaque só para o índice geral.
- Todos os gráficos com título que diz o que se vê e a unidade (%).
- Fonte sempre visível.

## Cuidados de interpretação (Pilar 5)

- A segmentação de período muda os números: deixe o período escolhido legível no título.
- Impacto alto não é sinônimo de alta forte: depende do peso do grupo.
- O painel mostra o que subiu, não a causa.
