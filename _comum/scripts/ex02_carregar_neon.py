"""Carrega o CSV do exercicio 02 (IPCA) nas tabelas dim_grupo e ipca_mensal
(PostgreSQL/Neon). Modelo normalizado: os nomes dos grupos ficam em uma tabela
so deles e a tabela de fatos guarda apenas o numero do grupo.

Antes de gravar, valida o arquivo. Se achar problema estrutural, NAO grava nada.

Uso (na raiz do repositorio):
    py _comum/scripts/ex02_carregar_neon.py
    py _comum/scripts/ex02_carregar_neon.py caminho/outro_arquivo.csv
"""
import os
import sys
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[2]
ARQUIVO_PADRAO = (RAIZ / "exercicios" / "02-painel-inflacao-ipca" / "dados"
                  / "ipca_grupos.csv")

CRIAR_TABELAS = """
CREATE TABLE IF NOT EXISTS dim_grupo (
  id_grupo     INTEGER PRIMARY KEY,
  codigo_sidra INTEGER NOT NULL UNIQUE,
  nome         TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ipca_mensal (
  mes         DATE NOT NULL,
  id_grupo    INTEGER NOT NULL REFERENCES dim_grupo (id_grupo),
  var_mensal  NUMERIC(8, 2),
  var_ano     NUMERIC(8, 2),
  var_12m     NUMERIC(8, 2),
  peso_mensal NUMERIC(8, 4),
  PRIMARY KEY (mes, id_grupo)
);
"""


def ler(caminho):
    df = pd.read_csv(caminho, sep=";", decimal=",", encoding="utf-8-sig")
    df["mes"] = pd.to_datetime(df["mes"])
    return df


def validar(df):
    problemas, avisos = [], []
    colunas = {"mes", "codigo_sidra", "grupo", "var_mensal", "var_ano",
               "var_12m", "peso_mensal"}
    if not colunas <= set(df.columns):
        return [f"faltam colunas: {sorted(colunas - set(df.columns))}"], avisos
    if df.duplicated(["mes", "codigo_sidra"]).any():
        problemas.append("ha linhas repetidas para o mesmo mes e grupo")
    if df["grupo"].nunique() != 10:
        problemas.append(f"esperava 10 grupos (geral + 9) e achei {df['grupo'].nunique()}")
    if df.groupby("mes").size().nunique() != 1:
        problemas.append("ha meses com numero diferente de grupos")
    if df["var_mensal"].abs().max() > 20:
        problemas.append("variacao mensal acima de 20%: confira se a virgula decimal foi lida certo")
    for coluna in ("var_mensal", "var_ano", "var_12m"):
        n = int(df[coluna].isna().sum())
        if n:
            avisos.append(f"{coluna}: {n} valores vazios (ficam NULL no banco)")
    if df["peso_mensal"].isna().all():
        avisos.append("peso_mensal esta todo vazio: a analise de impacto nao vai funcionar")
    return problemas, avisos


def nulo(valor):
    return None if pd.isna(valor) else float(valor)


def montar(df):
    grupos = (df[["codigo_sidra", "grupo"]].drop_duplicates()
              .sort_values("codigo_sidra").reset_index(drop=True))
    if grupos.loc[0, "grupo"] != "Índice geral":
        sys.exit("O Indice geral deveria ter o menor codigo. Confira o CSV.")
    grupos["id_grupo"] = grupos.index          # 0 = Indice geral, 1 a 9 = grupos
    ids = dict(zip(grupos["codigo_sidra"], grupos["id_grupo"]))
    linhas_grupo = [(int(r.id_grupo), int(r.codigo_sidra), r.grupo)
                    for r in grupos.itertuples()]
    linhas_fato = [(r.mes.date(), int(ids[r.codigo_sidra]), nulo(r.var_mensal),
                    nulo(r.var_ano), nulo(r.var_12m), nulo(r.peso_mensal))
                   for r in df.itertuples()]
    return linhas_grupo, linhas_fato


def gravar(url, linhas_grupo, linhas_fato):
    with psycopg.connect(url, connect_timeout=20) as conn:
        with conn.cursor() as cur:
            cur.execute(CRIAR_TABELAS)
            cur.execute("TRUNCATE ipca_mensal, dim_grupo")
            with cur.copy("COPY dim_grupo (id_grupo, codigo_sidra, nome) FROM STDIN") as copia:
                for linha in linhas_grupo:
                    copia.write_row(linha)
            with cur.copy("COPY ipca_mensal (mes, id_grupo, var_mensal, var_ano, var_12m, "
                          "peso_mensal) FROM STDIN") as copia:
                for linha in linhas_fato:
                    copia.write_row(linha)
            cur.execute("SELECT COUNT(*) FROM ipca_mensal")
            return cur.fetchone()[0]


def main():
    load_dotenv(RAIZ / ".env")
    # Tenta primeiro o endereco do pooler (o que ja funcionou neste projeto)
    candidatas = [os.getenv("DATABASE_URL"), os.getenv("DATABASE_URL_UNPOOLED")]
    urls = [u for u in candidatas if u]
    if not urls:
        sys.exit("Nao achei DATABASE_URL no arquivo .env da raiz do projeto.")

    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else ARQUIVO_PADRAO
    if not caminho.exists():
        sys.exit(f"Arquivo nao encontrado: {caminho}. Rode antes o ex02_baixar_ipca.py")
    df = ler(caminho)
    print(f"Lidas {len(df)} linhas de {caminho.name}")

    problemas, avisos = validar(df)
    for aviso in avisos:
        print(f"AVISO: {aviso}")
    if problemas:
        print("\nO arquivo tem problemas. Nada foi gravado:")
        for p in problemas:
            print(f"  - {p}")
        sys.exit(1)

    linhas_grupo, linhas_fato = montar(df)
    ultimo_erro = None
    for numero, url in enumerate(urls, start=1):
        try:
            print(f"Conectando ao banco (tentativa {numero} de {len(urls)})...")
            total = gravar(url, linhas_grupo, linhas_fato)
            print(f"Pronto: {len(linhas_grupo)} grupos e {total} linhas em ipca_mensal.")
            return
        except psycopg.OperationalError as erro:
            ultimo_erro = erro
            print(f"Nao consegui conectar: {str(erro).strip()[:200]}")
    sys.exit(f"Nenhuma conexao funcionou. Ultimo erro: {str(ultimo_erro).strip()[:200]}")


if __name__ == "__main__":
    main()