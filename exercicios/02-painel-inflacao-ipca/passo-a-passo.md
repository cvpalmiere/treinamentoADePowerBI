# Passo a passo - Exercício 02

Antes de começar, leia o `enunciado.md` e **escreva o período de comparação** que você vai usar (exemplo: "2021 contra 2025") em um arquivo `minha-solucao/anotacoes.md`. Faça isso antes de olhar os números.

## Etapa A - Obter os dados e conferir no Excel

1. Na raiz do projeto, rode:

       py _comum/scripts/ex02_baixar_ipca.py

   Leia o final da saída. Ela mostra o número de linhas, o período, os valores vazios e a conferência com o IBGE (dezembro de 2021 = 10,06%). Se aparecer ATENÇÃO, pare e investigue.

2. Abra o Excel. Menu Dados > Obter Dados > De Texto/CSV e escolha `dados/ipca_grupos.csv`. Confira Origem do arquivo = 65001 UTF-8 e Delimitador = Ponto e vírgula. Clique em Carregar e salve como `dados/ipca.xlsx`.
3. Inspecione: as colunas de variação estão como número? A coluna `mes` está como data? Quantas linhas e quantos vazios? Anote o que viu.
4. **Teste da soma que engana (Pilar 5).** Filtre `grupo` = "Índice geral" e o ano de 2021. Copie os 12 valores de `var_mensal` para uma área livre.
   - Em uma célula, some os 12 valores com `=SOMA(...)`.
   - Em uma coluna ao lado, calcule `=1+B2/100` para cada mês e depois `=(PRODUTO(C2:C13)-1)*100`.
   - Compare as duas respostas com o `var_12m` de dezembro de 2021. Qual delas bate com o IBGE? Por que a outra não bate?
5. **Tabela Dinâmica (Pilar 1).** Inserir > Tabela Dinâmica sobre a tabela inteira.
   - Linhas: `grupo`. Colunas: `mes` agrupado só por Anos (clique com o botão direito em uma data, Agrupar, Anos). Valores: `var_12m`.
   - Filtre o campo `mes` agrupado por Meses para mostrar só dezembro.
   - Aqui "Soma" só funciona porque cada célula contém um único número. Nunca some vários meses de percentuais.
   - Qual grupo teve o maior acumulado em cada ano?

## Etapa B - Banco normalizado e SQL

1. Confirme que o `prisma/schema.prisma` do repositório tem os modelos `DimGrupo` e `IpcaMensal`. Depois crie as tabelas:

       npx prisma db push

2. Carregue os dados:

       py _comum/scripts/ex02_carregar_neon.py

   O script valida o arquivo antes de gravar. Resultado esperado: `Pronto: 10 grupos e N linhas em ipca_mensal.`
3. Confira no SQL Editor do Neon:

       SELECT COUNT(*) FROM dim_grupo;
       SELECT COUNT(*), MIN(mes), MAX(mes) FROM ipca_mensal;

   Devem dar 10 grupos e o mesmo número de linhas do CSV.
4. **Por que dois arquivos de tabela?** Os nomes dos grupos ficam em `dim_grupo` e a tabela `ipca_mensal` guarda só o número do grupo. Isso é normalização: cada informação em um lugar só. Para ver o nome do grupo ao lado do valor, você precisa de um `JOIN`.
5. Responda as 5 perguntas do enunciado em SQL. Dicas de técnica (a solução está no gabarito, tente antes):
   - Pergunta 1: composição de percentuais com `EXP(SUM(LN(1 + x/100)))`, agrupando por ano.
   - Pergunta 2: o mesmo acumulado, filtrado pelo seu período e agrupado por grupo, com a diferença para o índice geral.
   - Pergunta 3: `CASE WHEN` para colocar dois períodos lado a lado, ou `LAG` para comparar com o mês anterior.
   - Pergunta 4: impacto = peso x variação / 100, no último mês.
   - Pergunta 5: `AVG`, `PERCENTILE_CONT(0.5)` e `STDDEV_SAMP` por grupo.
6. Salve as queries em `minha-solucao/queries.sql`.

## Etapa C - Painel no Power BI

1. Página Inicial > Obter dados > Banco de dados PostgreSQL. Servidor e banco estão no seu `.env`. Importe `dim_grupo` e `ipca_mensal`. Se a conexão falhar, exporte as duas tabelas em CSV pelo Neon e importe os arquivos.
2. Na visão Modelo, confira a relação `ipca_mensal[id_grupo]` para `dim_grupo[id_grupo]` (muitos para um). Em `id_grupo`, escolha "Não resumir".
3. Crie as medidas do painel (Modelagem > Nova medida). Tente escrevê-las antes de consultar `gabarito/dashboard.md`.
4. Monte uma página com: 3 cartões, 1 gráfico de linhas, 2 gráficos de barras, 1 segmentação de período e 1 caixa de texto com **fonte e conclusão**.
5. Salve em `powerbi/painel-inflacao.pbix` e exporte prints.

## Etapa D - Conclusão (Pilar 8)

Escreva o resumo executivo em 3 frases: contexto, descoberta (comece pelo achado, com números) e recomendação. Use só o que os dados sustentam.

## Pilares treinados neste exercício

- Pilar 1 - Alicerce: fórmula de acumulado composto e Tabela Dinâmica grupo x ano no Excel, antes de qualquer SQL.
- Pilar 2 - Trabalho Sujo: dados de uma API pública entram com valores "sem dado", nomes com prefixo e 365 categorias. Cada decisão de tratamento está registrada em `como-gerar-dados.md`, e o modelo final é normalizado (dimensão e fato).
- Pilar 3 - Linguagem: JOIN entre dimensão e fato, GROUP BY por ano e grupo, acumulado composto, `LAG` e `RANK`.
- Pilar 4 - Bússola: média, mediana e desvio padrão da variação mensal. Um mês atípico distorce a média de um grupo, a mediana resiste.
- Pilar 5 - Filtro Crítico: somar percentuais é erro; o período é escolhido antes dos números; o IPCA é uma média, não o custo de vida de ninguém; um grupo que sobe muito mas pesa pouco não explica a inflação.
- Pilar 6 - Tradução: "o que está pesando?" vira três números com contrapeso: acumulado (quanto subiu), impacto (quanto pesou) e desvio padrão (quão estável).
- Pilar 7 - Vitrine: um painel com poucos visuais, título que diz o achado, eixos honestos e fonte visível.
- Pilar 8 - Fator Ouro: contexto da pergunta, descoberta nos números, recomendação, nessa ordem.
