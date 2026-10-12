"""Carrega o arquivo LIMPO do exercicio 01 na tabela suspeitos (PostgreSQL/Neon).

Antes de gravar, valida a limpeza: se achar espaco sobrando, acento, tatuagem
fora de 0/1 ou ids repetidos, mostra o problema e NAO grava nada.

Uso (na raiz do repositorio):
    py _comum/scripts/ex01_carregar_neon.py
    py _comum/scripts/ex01_carregar_neon.py caminho/outro_arquivo.xlsx
"""
import os
import sys
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[2]
ARQUIVO_PADRAO = (RAIZ / "exercicios" / "01-carmem-sandiego" / "dados"
                  / "suspeitos_limpo_csv.xlsx")

COLUNAS = ["id", "nome", "profissao", "altura_cm", "cor_cabelo", "tem_tatuagem",
           "data_nascimento", "ultima_cidade", "valor_gasto_viagens"]
TEXTO = ["nome", "profissao", "cor_cabelo", "ultima_cidade"]

CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS suspeitos (
  id                  INTEGER PRIMARY KEY,
  nome                TEXT NOT NULL,
  profissao           TEXT,
  altura_cm           INTEGER,
  cor_cabelo          TEXT,
  tem_tatuagem        BOOLEAN,
  data_nascimento     DATE,
  ultima_cidade       TEXT,
  valor_gasto_viagens INTEGER
)
"""


def ler(caminho):
    if caminho.suffix.lower() == ".xlsx":
        df = pd.read_excel(caminho, sheet_name="limpo", dtype=object)
    else:
        df = pd.read_csv(caminho, sep=";", dtype=object, encoding="utf-8-sig")
    df = df.iloc[:, :9]          # as 9 primeiras colunas, na ordem do enunciado
    df.columns = COLUNAS         # ignora os nomes de cabecalho que voce escolheu
    return df


def validar(df):
    problemas = []
    if df["id"].duplicated().any():
        problemas.append(f"ids repetidos: {int(df['id'].duplicated().sum())}")
    for col in TEXTO:
        s = df[col].dropna().astype(str)
        pontas = int((s != s.str.strip().str.replace(r"\s+", " ", regex=True)).sum())
        acento = int(s.str.contains(r"[^\x00-\x7f]").sum())
        if pontas:
            problemas.append(f"{col}: {pontas} valores com espaco sobrando")
        if acento:
            problemas.append(f"{col}: {acento} valores com acento")
    if not set(df["tem_tatuagem"].astype(str)) <= {"0", "1"}:
        problemas.append("tem_tatuagem tem valores diferentes de 0 e 1")
    datas = pd.to_datetime(df["data_nascimento"], errors="coerce")
    if datas.isna().any():
        problemas.append(f"data_nascimento: {int(datas.isna().sum())} datas invalidas")
    elif datas.dt.year.min() < 1940 or datas.dt.year.max() > 2010:
        problemas.append("data_nascimento fora do intervalo esperado (1940 a 2010)")
    for col in ("altura_cm", "valor_gasto_viagens"):
        if pd.to_numeric(df[col], errors="coerce").isna().any():
            problemas.append(f"{col}: ha valores que nao sao numeros")
    return problemas


def nulo(v):
    return None if pd.isna(v) else v


def montar_linhas(df):
    linhas = []
    for r in df.itertuples(index=False):
        linhas.append((
            int(r.id),
            nulo(r.nome),
            nulo(r.profissao),
            int(r.altura_cm),
            nulo(r.cor_cabelo),
            bool(int(r.tem_tatuagem)),
            pd.to_datetime(r.data_nascimento).date(),
            nulo(r.ultima_cidade),
            int(r.valor_gasto_viagens),
        ))
    return linhas


def main():
    load_dotenv(RAIZ / ".env")
    url = os.getenv("DATABASE_URL_UNPOOLED") or os.getenv("DATABASE_URL")
    if not url:
        sys.exit("Nao achei DATABASE_URL no arquivo .env da raiz do projeto.")

    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else ARQUIVO_PADRAO
    df = ler(caminho)
    print(f"Lidas {len(df)} linhas de {caminho.name}")

    problemas = validar(df)
    if problemas:
        print("\nA limpeza ainda tem problemas. Nada foi gravado:")
        for p in problemas:
            print(f"  - {p}")
        sys.exit(1)

    linhas = montar_linhas(df)
    with psycopg.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(CRIAR_TABELA)
            cur.execute("TRUNCATE suspeitos")
            with cur.copy(
                "COPY suspeitos (id, nome, profissao, altura_cm, cor_cabelo, "
                "tem_tatuagem, data_nascimento, ultima_cidade, valor_gasto_viagens) "
                "FROM STDIN"
            ) as copia:
                for linha in linhas:
                    copia.write_row(linha)
            cur.execute("SELECT COUNT(*) FROM suspeitos")
            total = cur.fetchone()[0]
    print(f"Pronto: {total} linhas na tabela suspeitos.")


if __name__ == "__main__":
    main()