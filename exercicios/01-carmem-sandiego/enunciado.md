# Enunciado 01 - Carmem Sandiego

## Contexto

Um museu em Lisboa foi roubado. A policia internacional reuniu 2000 suspeitos a partir de varias fontes, cada uma com seu proprio jeito de digitar. Voce e o analista de dados da investigacao e precisa descobrir quem e a ladra.

## O que voce recebe

- `dados/suspeitos_sujo.csv` (separador `;`, UTF-8)
- Colunas: `id`, `nome`, `profissao`, `altura_cm`, `cor_cabelo`, `tem_tatuagem`, `data_nascimento`, `ultima_cidade`, `valor_gasto_viagens`

## Pistas

1. A altura esta entre 168 e 174 cm.
2. O cabelo e castanho ou preto.
3. Ela tem tatuagem.
4. A profissao e piloto, guia turistico ou fotografo.
5. O nome contem "Mont".
6. A ultima cidade visitada foi Lisboa, Madrid ou Roma.
7. Nasceu entre 01/01/1985 e 31/12/1992.
8. Gastou entre R$ 20.000 e R$ 40.000 em viagens.

## Entregas

1. CSV limpo, com as decisoes de limpeza anotadas.
2. Query SQL que isola a suspeita.
3. Dashboard no Power BI sobre a populacao de suspeitos e o funil de pistas.
4. Resumo executivo em 3 passos (contexto, descoberta, recomendacao).