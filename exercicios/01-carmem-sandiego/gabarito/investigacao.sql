-- Exercicio 01 - Carmem Sandiego
-- Rode no SQL Editor do Supabase/Neon ou no psql.

-- 1) Tabela (para quem nao usa Prisma)
CREATE TABLE suspeitos (
  id                  INTEGER PRIMARY KEY,
  nome                TEXT NOT NULL,
  profissao           TEXT,
  altura_cm           INTEGER,
  cor_cabelo          TEXT,
  tem_tatuagem        BOOLEAN,
  data_nascimento     DATE,
  ultima_cidade       TEXT,
  valor_gasto_viagens INTEGER
);

-- 2) Importacao (psql). Ajuste o caminho do arquivo.
-- \copy suspeitos FROM 'suspeitos_limpo.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';')

-- 3) Conferencia
SELECT COUNT(*) AS total FROM suspeitos;            -- esperado: 2000

-- 4) Funil: cada pista sobre a anterior (execute uma a uma e anote)
SELECT COUNT(*) FROM suspeitos
WHERE altura_cm BETWEEN 168 AND 174;

SELECT COUNT(*) FROM suspeitos
WHERE altura_cm BETWEEN 168 AND 174
  AND cor_cabelo IN ('Castanho', 'Preto');

SELECT COUNT(*) FROM suspeitos
WHERE altura_cm BETWEEN 168 AND 174
  AND cor_cabelo IN ('Castanho', 'Preto')
  AND tem_tatuagem = TRUE;

SELECT COUNT(*) FROM suspeitos
WHERE altura_cm BETWEEN 168 AND 174
  AND cor_cabelo IN ('Castanho', 'Preto')
  AND tem_tatuagem = TRUE
  AND profissao IN ('Piloto', 'Guia Turistico', 'Fotografo');

-- 5) Query final: todas as pistas
SELECT id, nome, profissao, altura_cm, ultima_cidade, valor_gasto_viagens
FROM suspeitos
WHERE altura_cm BETWEEN 168 AND 174
  AND cor_cabelo IN ('Castanho', 'Preto')
  AND tem_tatuagem = TRUE
  AND profissao IN ('Piloto', 'Guia Turistico', 'Fotografo')
  AND nome LIKE '%Mont%'
  AND ultima_cidade IN ('Lisboa', 'Madrid', 'Roma')
  AND data_nascimento BETWEEN '1985-01-01' AND '1992-12-31'
  AND valor_gasto_viagens BETWEEN 20000 AND 40000;
-- Resultado esperado: 1 linha (Helena Montenegro Teixeira)

-- 6) Exemplo de OR com parenteses: quem escapou por pouco?
SELECT id, nome, ultima_cidade
FROM suspeitos
WHERE (profissao = 'Piloto' OR profissao = 'Fotografo')
  AND tem_tatuagem = TRUE
  AND ultima_cidade = 'Lisboa';

-- 7) Bussola: media x mediana
SELECT
  ROUND(AVG(valor_gasto_viagens)) AS media,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY valor_gasto_viagens) AS mediana
FROM suspeitos;