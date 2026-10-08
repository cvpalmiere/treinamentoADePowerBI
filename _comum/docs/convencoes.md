# Convencoes do repositorio

## Nomes

- Pastas e arquivos: minusculas, sem acento, sem espaco, palavras separadas por hifen.
- Pasta de exercicio: `NN-slug` (exemplo: `01-carmem-sandiego`, `02-vendas-fantasma`).
- Scripts geradores: `_comum/scripts/exNN_gerar_dados.py`.
- CSV sujo: `<tema>_sujo.csv`. CSV limpo: `<tema>_limpo.csv`.
- Colunas dos CSVs: minusculas, `snake_case`, sem acento (`data_nascimento`).
- Tabelas SQL: plural, minusculas (`suspeitos`).

## O que TODA questao deve ter

| Item | Funcao |
|------|--------|
| `README.md` | visao geral, links, pilares treinados |
| `enunciado.md` | o problema, sem solucao |
| `como-gerar-dados.md` | script, erros inseridos, linhas, gabarito escondido |
| `passo-a-passo.md` | tutorial Excel, SQL, Power BI e "Pilares treinados neste exercicio" |
| `gabarito/` | solucao comentada das 3 etapas |
| `dados/` | o CSV sujo da questao |
| `powerbi/` | prints ou arquivo .pbix |

## Regras de dados

- Todo script gerador usa semente fixa (reproducivel).
- Todo erro inserido e listado no `como-gerar-dados.md`.
- A limpeza e honesta: decisoes (padronizar, descartar, deixar nulo) ficam documentadas. Nunca ajustar dados para confirmar uma conclusao desejada.
- CSV com `;` como separador e UTF-8 com BOM, para abrir certo no Excel brasileiro.

## Commits

Mensagens curtas no imperativo: `adiciona exercicio 02`, `corrige gabarito do 01`.