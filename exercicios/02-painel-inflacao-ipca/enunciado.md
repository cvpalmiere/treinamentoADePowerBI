# Enunciado 02 - Painel de inflação (IPCA / IBGE)

## Contexto

Você é analista de dados em uma consultoria e precisa apresentar um painel de inflação para a diretoria. A pergunta da diretoria é simples: "o que anda pesando no custo de vida e isso mudou ao longo dos anos?" O painel precisa comparar grupos de produtos e períodos, mostrar gráficos, citar a fonte e terminar com uma conclusão.

## O que você recebe

Um script que baixa o IPCA do IBGE e cria `dados/ipca_grupos.csv` (separador `;`, decimal com vírgula, UTF-8). Uma linha por mês e por grupo, de janeiro de 2020 ao último mês divulgado.

| Coluna | Significado |
|--------|-------------|
| `mes` | primeiro dia do mês de referência |
| `codigo_sidra` | código da categoria no IBGE |
| `grupo` | "Índice geral" ou um dos 9 grupos |
| `var_mensal` | variação do preço no mês (%) |
| `var_ano` | variação acumulada no ano (%) |
| `var_12m` | variação acumulada em 12 meses (%) |
| `peso_mensal` | peso do grupo no índice (%) |

## Regras do estudo

1. **Defina o período de comparação antes de olhar os números** e anote por quê (exemplo: "2021 contra 2025"). Escolher o recorte depois de ver o resultado é uma forma de manipular a conclusão.
2. **Variações percentuais não se somam.** Para acumular meses, componha os percentuais.
3. Todo gráfico precisa de título, unidade e eixo honesto.
4. Todo painel precisa de fonte e data de acesso.

## Perguntas

1. Quanto foi a inflação (IPCA) acumulada em cada ano completo de 2020 a 2025? O que mudou de um ano para outro?
2. Em um mesmo período, quais grupos mais subiram e quais menos? Como cada um se compara ao índice geral?
3. Em que momentos a inflação acelerou ou desacelerou? Compare dois períodos escolhidos por você.
4. O grupo que mais subiu é o que mais pesou no índice? Use o impacto (peso x variação) para responder.
5. Quais grupos são mais voláteis? A média da variação mensal conta a história toda ou a mediana conta melhor?

## Entregas

1. O CSV baixado e conferido com um número divulgado pelo IBGE.
2. As queries SQL que respondem as 5 perguntas.
3. Um painel no Power BI com gráficos, fonte e conclusão.
4. Um resumo executivo de 3 passos (contexto, descoberta, recomendação), começando pelo achado.
