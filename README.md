# Exercicios de Analise de Dados

Repositorio de pratica integrada em tres ferramentas: Excel, SQL e Power BI.

Fluxo dos exercicios de investigacao (01):

    CSV sujo (gerado por script Python)
      -> limpeza no Excel
      -> importacao no PostgreSQL
      -> investigacao em SQL
      -> dashboard no Power BI

Fluxo dos exercicios de estudo com dados reais (02):

    dados publicos (API do IBGE, baixados por script Python)
      -> conferencia e Tabela Dinamica no Excel
      -> modelo normalizado no PostgreSQL
      -> perguntas respondidas em SQL
      -> painel no Power BI com fonte e conclusao

## Estrutura

- `_comum/templates/` modelos de README, enunciado, como-gerar-dados e passo-a-passo
- `_comum/scripts/` scripts Python que geram ou baixam os dados e carregam no banco
- `_comum/dados/` copia dos CSVs prontos para download
- `_comum/docs/` convencoes e guia dos 8 pilares
- `exercicios/` uma subpasta por questao
- `prisma/schema.prisma` tabelas do banco (todos os exercicios)

## Exercicios

| No | Titulo | Tipo | Pilares principais |
|----|--------|------|--------------------|
| 01 | [Carmem Sandiego](exercicios/01-carmem-sandiego/README.md) | investigacao de caso | 1, 2, 3, 4, 5, 6, 7, 8 |
| 02 | [Painel de inflacao (IPCA / IBGE)](exercicios/02-painel-inflacao-ipca/README.md) | estudo com dados reais | 1, 2, 3, 4, 5, 6, 7, 8 |

## Como comecar

1. Instale Python, Git, Node e Power BI Desktop.
2. Instale as bibliotecas: `pip install pandas numpy openpyxl "psycopg[binary]" python-dotenv`.
3. Configure o arquivo `.env` na raiz com `DATABASE_URL` e `DATABASE_URL_UNPOOLED` do Neon.
4. Rode `npx prisma db push` para criar as tabelas.
5. Siga o `passo-a-passo.md` do exercicio desejado.

## Documentacao

- [Convencoes](_comum/docs/convencoes.md)
- [Guia dos 8 pilares](_comum/docs/guia-8-pilares.md)
