-- Exercicio 02 - Painel de inflacao (IPCA / IBGE)
-- Rode no SQL Editor do Neon. Troque as datas pelo periodo que VOCE escolheu.

-- 0) Conferencias
SELECT COUNT(*) AS grupos FROM dim_grupo;                      -- esperado: 10

SELECT COUNT(*) AS linhas, MIN(mes) AS primeiro_mes, MAX(mes) AS ultimo_mes
FROM ipca_mensal;

-- Dezembro de 2021 deve mostrar 10,06 no indice geral
SELECT m.mes, m.var_12m
FROM ipca_mensal m
JOIN dim_grupo g USING (id_grupo)
WHERE g.nome = 'Índice geral' AND m.mes = DATE '2021-12-01';

-- 1) Pergunta 1: IPCA acumulado em cada ano completo (composicao dos 12 meses)
SELECT EXTRACT(YEAR FROM m.mes)::int AS ano,
       ROUND((EXP(SUM(LN(1 + m.var_mensal / 100.0))) - 1) * 100, 2) AS acumulado_composto,
       ROUND(SUM(m.var_mensal), 2) AS soma_simples_errada
FROM ipca_mensal m
JOIN dim_grupo g USING (id_grupo)
WHERE g.nome = 'Índice geral'
  AND m.mes < DATE '2026-01-01'
GROUP BY 1
ORDER BY 1;

-- O mesmo numero como o IBGE divulga (acumulado em 12 meses de dezembro)
SELECT EXTRACT(YEAR FROM m.mes)::int AS ano, m.var_12m AS divulgado_ibge
FROM ipca_mensal m
JOIN dim_grupo g USING (id_grupo)
WHERE g.nome = 'Índice geral' AND EXTRACT(MONTH FROM m.mes) = 12
ORDER BY ano;

-- 2) Pergunta 2: acumulado por grupo em um periodo, comparado ao indice geral
WITH acumulado AS (
  SELECT g.nome,
         ROUND((EXP(SUM(LN(1 + m.var_mensal / 100.0))) - 1) * 100, 2) AS acumulado_pct
  FROM ipca_mensal m
  JOIN dim_grupo g USING (id_grupo)
  WHERE m.mes BETWEEN DATE '2021-01-01' AND DATE '2021-12-01'
  GROUP BY g.nome
)
SELECT nome,
       acumulado_pct,
       ROUND(acumulado_pct - (SELECT acumulado_pct FROM acumulado WHERE nome = 'Índice geral'), 2)
         AS diferenca_vs_geral_pp
FROM acumulado
ORDER BY acumulado_pct DESC;

-- 3) Pergunta 3a: dois periodos lado a lado (12 meses acumulados em dezembro de cada ano)
SELECT g.nome,
       MAX(CASE WHEN m.mes = DATE '2024-12-01' THEN m.var_12m END) AS dez_2024,
       MAX(CASE WHEN m.mes = DATE '2025-12-01' THEN m.var_12m END) AS dez_2025,
       MAX(CASE WHEN m.mes = DATE '2025-12-01' THEN m.var_12m END)
       - MAX(CASE WHEN m.mes = DATE '2024-12-01' THEN m.var_12m END) AS mudanca_pp
FROM ipca_mensal m
JOIN dim_grupo g USING (id_grupo)
WHERE m.mes IN (DATE '2024-12-01', DATE '2025-12-01')
GROUP BY g.nome
ORDER BY mudanca_pp DESC;

-- 3) Pergunta 3b: aceleracao e desaceleracao do indice geral (12 meses vs mes anterior)
SELECT m.mes,
       m.var_12m,
       ROUND(m.var_12m - LAG(m.var_12m) OVER (ORDER BY m.mes), 2) AS mudanca_vs_mes_anterior_pp
FROM ipca_mensal m
JOIN dim_grupo g USING (id_grupo)
WHERE g.nome = 'Índice geral'
ORDER BY m.mes;

-- 4) Pergunta 4: impacto (peso x variacao / 100) de cada grupo no ultimo mes
WITH ultimo AS (SELECT MAX(mes) AS mes FROM ipca_mensal)
SELECT g.nome,
       m.peso_mensal,
       m.var_mensal,
       ROUND(m.peso_mensal * m.var_mensal / 100.0, 3) AS impacto_pp
FROM ipca_mensal m
JOIN dim_grupo g USING (id_grupo)
JOIN ultimo u ON u.mes = m.mes
WHERE g.nome <> 'Índice geral'
ORDER BY impacto_pp DESC;

-- Conferencia: a soma dos impactos deve ficar perto da variacao mensal do indice geral
WITH ultimo AS (SELECT MAX(mes) AS mes FROM ipca_mensal)
SELECT ROUND(SUM(m.peso_mensal * m.var_mensal / 100.0), 3) AS soma_impactos,
       (SELECT m2.var_mensal
        FROM ipca_mensal m2
        JOIN dim_grupo g2 USING (id_grupo)
        WHERE g2.nome = 'Índice geral' AND m2.mes = (SELECT mes FROM ultimo)) AS var_mensal_geral
FROM ipca_mensal m
JOIN dim_grupo g USING (id_grupo)
WHERE g.nome <> 'Índice geral' AND m.mes = (SELECT mes FROM ultimo);

-- 5) Pergunta 5a: media x mediana x desvio padrao da variacao mensal de cada grupo
SELECT g.nome,
       ROUND(AVG(m.var_mensal), 2) AS media,
       ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY m.var_mensal)::numeric, 2) AS mediana,
       ROUND(STDDEV_SAMP(m.var_mensal), 2) AS desvio_padrao,
       MIN(m.var_mensal) AS minimo,
       MAX(m.var_mensal) AS maximo
FROM ipca_mensal m
JOIN dim_grupo g USING (id_grupo)
WHERE g.nome <> 'Índice geral'
GROUP BY g.nome
ORDER BY desvio_padrao DESC;

-- 5) Pergunta 5b: quantos meses cada grupo foi o que mais subiu
WITH ranking AS (
  SELECT m.mes,
         g.nome,
         RANK() OVER (PARTITION BY m.mes ORDER BY m.var_mensal DESC) AS posicao
  FROM ipca_mensal m
  JOIN dim_grupo g USING (id_grupo)
  WHERE g.nome <> 'Índice geral' AND m.var_mensal IS NOT NULL
)
SELECT nome, COUNT(*) AS meses_em_primeiro
FROM ranking
WHERE posicao = 1
GROUP BY nome
ORDER BY meses_em_primeiro DESC;
