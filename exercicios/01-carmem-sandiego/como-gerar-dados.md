# Como os dados sao gerados - Exercicio 01

## Script

`_comum/scripts/ex01_gerar_dados.py`

## Como rodar

    python _comum/scripts/ex01_gerar_dados.py

(No Windows, use `py` no lugar de `python`.)

## Saida

| Arquivo | Conteudo |
|---------|----------|
| `exercicios/01-carmem-sandiego/dados/suspeitos_sujo.csv` | CSV sujo (entregue ao aluno) |
| `_comum/dados/ex01_suspeitos_sujo.csv` | copia |
| `exercicios/01-carmem-sandiego/gabarito/suspeitos_limpo_referencia.csv` | resultado de uma limpeza perfeita |
| `exercicios/01-carmem-sandiego/gabarito/gabarito_oculto.json` | id e nome da culpada |

## Tamanho

2040 linhas: 2000 suspeitos unicos mais 40 linhas duplicadas exatas. 9 colunas. Semente fixa 42.

## Erros inseridos

| Coluna | Erro | Como limpar |
|--------|------|-------------|
| nome, profissao, cor_cabelo, ultima_cidade | acentos removidos, MAIUSCULAS, minusculas, espacos extras no inicio, fim e meio | trocar acentos, ARRUMAR, NOME.PROPRIO |
| profissao, cor_cabelo | ~2% vazios | manter vazio, nunca adivinhar |
| altura_cm | `172`, `172 cm`, `1,72 m` | converter tudo para cm inteiro |
| tem_tatuagem | Sim, sim, SIM, S, 1, True, verdadeiro, yes (e os opostos) | PROCV com tabela de mapeamento para 1 ou 0 |
| data_nascimento | 4 formatos: `AAAA-MM-DD`, `DD/MM/AAAA`, `DD-MM-AAAA`, `DD.MM.AAAA` (dia sempre antes do mes nos tres ultimos) | converter para `AAAA-MM-DD` |
| valor_gasto_viagens | `31500`, `R$ 31.500`, `31.500`, `R$31500` (ponto e milhar, nao decimal) | extrair so o numero inteiro |
| linhas | 40 duplicatas exatas | Remover Duplicatas |

## Gabarito escondido

Exatamente uma pessoa satisfaz as 8 pistas. O script confere isso com um `assert` antes de gravar. A culpada nunca recebe nulo nem duplicata, entao ela e sempre recuperavel depois da limpeza. O gabarito fica em `gabarito/gabarito_oculto.json`.