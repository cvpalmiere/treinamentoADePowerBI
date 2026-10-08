# Gabarito - Exercicio 01

Nao abra antes de tentar.

- `investigacao.sql`: CREATE TABLE, funil e query final
- `dashboard.md`: layout do dashboard e medidas DAX
- `schema.prisma`: modelo Prisma (opcional)
- `suspeitos_limpo_referencia.csv`: limpeza perfeita (gerada pelo script)
- `gabarito_oculto.json`: id e nome da culpada (gerado pelo script)

## Resposta

A culpada e Helena Montenegro Teixeira, guia turistico, 171 cm, cabelo castanho, tatuada, nascida em 14/03/1989, ultima cidade Lisboa, gasto de R$ 31.500.

## Decisoes de limpeza esperadas

1. 40 duplicatas exatas removidas (2040 para 2000).
2. Texto sem acento e em Title Case.
3. Altura em cm inteiro; valor em reais inteiro; data em AAAA-MM-DD; tatuagem em 1 ou 0.
4. Nulos de profissao e cor do cabelo (~2%) mantidos como nulos.