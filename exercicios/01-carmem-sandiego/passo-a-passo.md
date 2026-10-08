# Passo a passo - Exercicio 01

## Etapa A - Excel (limpeza)

1. Abra o Excel. Menu Dados > Obter Dados > De Texto/CSV e escolha `dados/suspeitos_sujo.csv`.
2. Na janela de visualizacao, confira Origem do arquivo = 65001 UTF-8 e Delimitador = Ponto e virgula.
3. Em Deteccao de Tipo de Dados, escolha "Nao Detectar Tipos de Dados". Isso mantem tudo como texto e evita que o Excel converta "True" ou "1" sozinho. Clique em Carregar.
4. Salve o arquivo como `suspeitos.xlsx` em `exercicios/01-carmem-sandiego/dados/`.
5. Duplicatas: selecione a tabela, Dados > Remover Duplicatas, deixe todas as colunas marcadas. Devem sair 40 linhas (2040 para 2000). Anote o numero.
6. Acentos: selecione as colunas nome, profissao, cor_cabelo e ultima_cidade. Pagina Inicial > Localizar e Selecionar > Substituir. Troque cada letra acentuada pela versao sem acento: a, a, a, a (de á, à, â, ã), e (é, ê), i (í), o (ó, ô, õ), u (ú), c (ç). Decisao documentada: o padrao final nao tem acento, porque acentos perdidos nao podem ser recuperados com certeza.
7. Crie colunas auxiliares (a tabela tem as colunas A a I na ordem do enunciado). Na linha 2, escreva e arraste ate o fim:

   - nome limpo: `=NOME.PRÓPRIO(ARRUMAR(B2))`
   - profissao limpa: `=SE(ARRUMAR(C2)="";"";NOME.PRÓPRIO(ARRUMAR(C2)))`
   - cor do cabelo limpa: `=SE(ARRUMAR(E2)="";"";NOME.PRÓPRIO(ARRUMAR(E2)))`
   - cidade limpa: `=NOME.PRÓPRIO(ARRUMAR(H2))`
   - altura limpa: `=SE(DIREITA(ARRUMAR(D2);2)="cm";VALOR(SUBSTITUIR(ARRUMAR(D2);" cm";""));SE(DIREITA(ARRUMAR(D2);1)="m";ARRED(VALOR(SUBSTITUIR(ARRUMAR(D2);" m";""))*100;0);VALOR(ARRUMAR(D2))))`
   - valor limpo: `=VALOR(SUBSTITUIR(SUBSTITUIR(SUBSTITUIR(I2;"R$";"");".";"");" ";""))`
   - data limpa: `=SE(EXT.TEXTO(G2;5;1)="-";DATA(ESQUERDA(G2;4);EXT.TEXTO(G2;6;2);EXT.TEXTO(G2;9;2));DATA(DIREITA(G2;4);EXT.TEXTO(G2;4;2);ESQUERDA(G2;2)))` e formate a coluna como Personalizado `aaaa-mm-dd`
   - tatuagem limpa: crie uma aba `mapa` com a coluna A (sim, s, 1, true, verdadeiro, yes, nao, n, 0, false, falso, no) e coluna B (1 nas seis primeiras, 0 nas seis ultimas); depois `=PROCV(MINÚSCULA(ARRUMAR(F2));mapa!A:B;2;FALSO)`
8. Crie uma aba `limpo` com colunas na ordem: id, nome, profissao, altura_cm, cor_cabelo, tem_tatuagem, data_nascimento, ultima_cidade, valor_gasto_viagens. Cole os resultados das fórmulas com Colar Especial > Valores. Celulas de profissao e cor do cabelo que estavam vazias continuam vazias.
9. Com a aba `limpo` ativa, Arquivo > Salvar como > "CSV UTF-8 (delimitado por virgulas)". Nome: `suspeitos_limpo.csv`. No Excel brasileiro o separador sera `;`.
10. Confira: 2000 linhas, sem duplicatas, e compare algumas linhas com `gabarito/suspeitos_limpo_referencia.csv`.
11. Tabela Dinamica (Pilar 1): na aba limpa, Inserir > Tabela Dinamica. Linhas = profissao, Valores = contagem de id e media do valor. Anote o que chamou atencao.

## Etapa B - Banco e SQL

1. Crie um projeto gratuito no Supabase (ou Neon). Copie a string de conexao.
2. No terminal: `npm init -y` e depois `npm install prisma --save-dev` (opcional, so se for usar Prisma).
3. Crie o arquivo `.env` na raiz com `DATABASE_URL="sua-string-de-conexao"`. Ele ja esta no `.gitignore`.
4. Crie a tabela. Caminho mais simples: abra o SQL Editor do Supabase (ou o console SQL do Neon) e rode o `CREATE TABLE` que esta em `gabarito/investigacao.sql`. Caminho Prisma: use `gabarito/schema.prisma` e `npx prisma db push` (se a sua versao do Prisma pedir outro arquivo de configuracao, siga a mensagem do terminal).
5. Importe o CSV limpo:
   - Supabase: Table Editor > tabela `suspeitos` > Import data from CSV (confira o delimitador).
   - Qualquer banco, via psql: `\copy suspeitos FROM 'caminho/suspeitos_limpo.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';')`
6. Confira: `SELECT COUNT(*) FROM suspeitos;` deve retornar 2000.
7. Faca o funil: adicione uma pista por vez e veja o COUNT cair. Depois monte a query final. Tudo isso esta em `gabarito/investigacao.sql`, mas tente antes de olhar.

## Etapa C - Power BI

1. Power BI Desktop > Obter dados > PostgreSQL (informe servidor e banco) ou, mais simples, Texto/CSV com `suspeitos_limpo.csv`.
2. No Power Query, confira tipos: id e inteiros, data_nascimento como Data, tem_tatuagem como Verdadeiro/Falso (converta 1 e 0).
3. Crie medidas (Modelagem > Nova medida): total de suspeitos, percentual com tatuagem, media e mediana de gasto.
4. Monte o dashboard descrito em `gabarito/dashboard.md`.
5. Salve em `exercicios/01-carmem-sandiego/powerbi/carmem-sandiego.pbix` e exporte prints (Arquivo > Exportar > PDF).

## Pilares treinados neste exercicio

- Pilar 1 - Alicerce: ARRUMAR, NOME.PROPRIO, SUBSTITUIR, PROCV e Tabela Dinamica fazem o trabalho de formatacao e resumo antes do codigo.
- Pilar 2 - Trabalho Sujo: voce remove 40 duplicatas, trata formatos de data, valor, altura e booleano, e mantem os nulos como nulos. Anote cada decisao. Se uma celula vazia pudesse "ajudar" a confirmar uma suspeita, deixa-la vazia continua sendo a decisao honesta.
- Pilar 3 - Linguagem: WHERE, IN, BETWEEN, LIKE e AND/OR repetem em SQL, em escala, o que o filtro do Excel faria.
- Pilar 4 - Bussola: compare media e mediana de `valor_gasto_viagens`. A distribuicao tem cauda longa, entao a media deve ser maior que a mediana. Qual descreve melhor o suspeito tipico?
- Pilar 5 - Filtro Critico: se a Tabela Dinamica mostrar mais tatuados em uma profissao, lembre que os dados sao aleatorios: qualquer diferenca e acaso, nao causa. Mantenha o eixo dos graficos de barra comecando em zero.
- Pilar 6 - Traducao: "quem e suspeito?" vira um funil de contagens, uma por pista. Contrapeso: a pista que mais reduz o numero nao e necessariamente a mais confiavel.
- Pilar 7 - Vitrine: poucos visuais, hierarquia clara (cartoes no topo), segmentacoes e o grafico certo para cada pergunta.
- Pilar 8 - Fator Ouro: escreva o resumo executivo em 3 frases (contexto, descoberta, recomendacao), comecando pelo achado.