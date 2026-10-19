# Como os dados são obtidos - Exercício 02

Aqui os dados são reais. Em vez de gerar um CSV com erros propositais, o script baixa os números do IBGE e deixa o arquivo pronto para análise, registrando cada decisão de tratamento.

## Script

`_comum/scripts/ex02_baixar_ipca.py`

## Como rodar

    py _comum/scripts/ex02_baixar_ipca.py

Precisa de internet. Se a API do IBGE estiver instável, tente de novo mais tarde.

## Saída

| Arquivo | Conteúdo |
|---------|----------|
| `exercicios/02-painel-inflacao-ipca/dados/ipca_grupos.csv` | IPCA por grupo e mês |
| `_comum/dados/ex02_ipca_grupos.csv` | cópia |

## Tamanho esperado

10 categorias (Índice geral e 9 grupos) vezes um mês por linha, de janeiro de 2020 ao último mês divulgado: cerca de 800 linhas e 7 colunas.

## De onde vêm os números

API do SIDRA/IBGE, tabela 7060 (IPCA, a partir de janeiro de 2020), nível Brasil. Variáveis usadas: variação mensal, acumulada no ano, acumulada em 12 meses e peso mensal. A classificação 315 contém 365 categorias (índice geral, grupos, subgrupos, itens e subitens). O script usa só o índice geral e os 9 grupos.

## Decisões de tratamento (Pilar 2)

| Situação | O que o script faz | Por quê |
|----------|-------------------|---------|
| A API devolve tudo em texto | converte para número | permite cálculo |
| Valor "sem dado" (`...`, `-`, `X`) | vira vazio, nunca zero | zero seria uma inflação inventada |
| Nome do grupo vem com prefixo ("1.Alimentação e bebidas") | remove o número do início | rótulo limpo para os gráficos |
| 365 categorias | mantém só índice geral e 9 grupos | os subgrupos e itens não são o foco deste exercício |
| Decimal | grava com vírgula | o Excel em português lê como número |
| Peso mensal indisponível | o CSV sai sem peso e o script avisa | o resto do exercício continua possível |

## Conferência

Ao final, o script compara o IPCA acumulado em 12 meses de dezembro de 2021 com o valor divulgado pelo IBGE (10,06%) e escreve OK ou ATENÇÃO. Se aparecer ATENÇÃO, os dados não estão confiáveis: não siga em frente sem entender o motivo.

## Limitações

- Só nível Brasil (sem regiões).
- A tabela 7060 começa em janeiro de 2020. Os anos anteriores ficam em outra tabela do IBGE, com outra estrutura de itens.
- O IPCA mede a cesta média de famílias com renda de 1 a 40 salários mínimos. Não é a inflação de uma pessoa específica.

## Gabarito escondido

Não há resposta única. A conferência é feita contra números públicos do IBGE (veja `gabarito/README.md`).
