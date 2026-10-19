# Gabarito - Exercício 02

Não abra antes de tentar. Aqui não existe uma resposta única: o gabarito mostra como validar o trabalho e como estruturar a conclusão.

## Arquivos

- `investigacao.sql`: conferências e queries das 5 perguntas
- `dashboard.md`: medidas DAX, layout e títulos do painel

## Como validar se o seu trabalho está certo

Valores de referência publicados pelo IBGE para o IPCA acumulado no ano (confira no site do IBGE antes de usar em público):

| Ano | IPCA acumulado |
|-----|----------------|
| 2020 | cerca de 4,52% |
| 2021 | cerca de 10,06% |
| 2023 | cerca de 4,62% |
| 2024 | cerca de 4,83% |
| 2025 | cerca de 4,26% |

- O `var_12m` de dezembro de cada ano, no CSV, deve bater com a tabela acima.
- O acumulado calculado por composição dos 12 meses deve ficar muito próximo (diferença de centésimos, por causa do arredondamento dos meses).
- A soma simples dos 12 meses **não** bate. Essa é a armadilha do Pilar 5.
- A soma dos impactos (peso x variação / 100) dos 9 grupos em um mês deve ficar muito próxima da variação mensal do índice geral.

## Decisões de tratamento esperadas

1. Valores "sem dado" viram vazio, nunca zero.
2. Prefixos numéricos removidos dos nomes dos grupos.
3. Só índice geral e 9 grupos (nenhum subgrupo ou item).
4. Modelo normalizado: `dim_grupo` (10 linhas) e `ipca_mensal` (uma linha por mês e grupo).

## Modelo de conclusão (Pilar 8)

Preencha com os **seus** números. Não copie frases prontas sem conferir nos dados.

- **Contexto:** a diretoria quer saber o que pesa no custo de vida e se isso mudou. Comparei [período A] com [período B] usando o IPCA do IBGE, por grupo.
- **Descoberta:** o IPCA acumulou [x%] em [período A] e [y%] em [período B]. O grupo [nome] foi o que mais subiu ([z%]), mas o grupo [nome] foi o que mais pesou no índice ([w] p.p.), porque [peso maior ou menor].
- **Recomendação:** [ação concreta para a diretoria], levando em conta que o IPCA mede a cesta média das famílias e não o custo de vida de um perfil específico.

Fonte (sempre no painel): IBGE, SIDRA, tabela 7060 (IPCA). Acesso em [data].

## Armadilhas a evitar

- Somar percentuais mensais em vez de compor.
- Escolher o período depois de ver qual dá a conclusão desejada.
- Comparar o acumulado de grupos sem olhar o peso de cada um.
- Gráfico de barras com eixo que não começa em zero.
- Concluir causa (por exemplo, "o preço do combustível causou a alta de alimentos") sem evidência: o painel mostra o que subiu, não o porquê.
