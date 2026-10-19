"""Exercicio 02 - Painel de inflacao (IPCA / IBGE).

Baixa o IPCA por grupo da API do SIDRA/IBGE (tabela 7060) e grava um CSV
organizado: uma linha por mes e por grupo (mais o Indice geral).

Uso (na raiz do repositorio):
    py _comum/scripts/ex02_baixar_ipca.py

Precisa de internet. So usa pandas e a biblioteca padrao do Python.
"""
import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

BASE_API = "https://apisidra.ibge.gov.br/values"
TABELA = 7060                      # IPCA, a partir de janeiro/2020
VARIAVEIS = {                      # codigo SIDRA -> nome da coluna no CSV
    "63": "var_mensal",            # variacao no mes (%)
    "69": "var_ano",               # acumulada no ano (%)
    "2265": "var_12m",             # acumulada em 12 meses (%)
}
VARIAVEL_PESO = "66"               # peso mensal do grupo no indice (%)
NOME_GERAL = "Índice geral"

RAIZ = Path(__file__).resolve().parents[2]
PASTA_EX = RAIZ / "exercicios" / "02-painel-inflacao-ipca"
PASTA_COMUM = RAIZ / "_comum" / "dados"


def buscar(caminho):
    pedido = Request(f"{BASE_API}/{caminho}",
                     headers={"User-Agent": "exercicios-dados/1.0"})
    with urlopen(pedido, timeout=90) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def validar_resposta(dados, o_que):
    if not isinstance(dados, list) or len(dados) < 2:
        sys.exit(f"A API nao devolveu dados para {o_que}: {str(dados)[:300]}")


def dimensao(cabecalho, trecho):
    """A 1a linha da API descreve cada coluna (D1N = 'Brasil', D2N = 'Variável'...).
    Procura qual coluna Dn contem o trecho e devolve 'Dn'."""
    for chave, texto in cabecalho.items():
        if re.fullmatch(r"D\d+N", chave) and trecho.lower() in str(texto).lower():
            return chave[:-1]
    sys.exit(f"Nao achei a dimensao '{trecho}' no cabecalho da API: {cabecalho}")


def descobrir_grupos():
    """Pergunta a API pelas 365 categorias do IPCA (so no ultimo mes) e fica com
    o Indice geral e os 9 grupos (nomes que comecam com 1 digito e ponto)."""
    dados = buscar(f"t/{TABELA}/n1/all/v/63/p/last/c315/all")
    validar_resposta(dados, "a lista de grupos")
    coluna = dimensao(dados[0], "Geral")
    grupos = {}
    for linha in dados[1:]:
        codigo = int(linha[coluna + "C"])
        nome = linha[coluna + "N"].strip()
        if re.match(r"^\d\.", nome):
            grupos[codigo] = re.sub(r"^\d\.\s*", "", nome)
        elif nome.lower().replace("í", "i").startswith("indice geral"):
            grupos[codigo] = NOME_GERAL
    if len(grupos) != 10:
        sys.exit(f"Esperava 10 categorias (geral + 9 grupos) e achei {len(grupos)}: {grupos}")
    return grupos


def para_df(dados):
    """Transforma a resposta da API em tabela: mes, categoria, variavel, valor."""
    cabecalho, linhas = dados[0], pd.DataFrame(dados[1:])
    c_var = dimensao(cabecalho, "Variável")
    c_mes = dimensao(cabecalho, "Mês")
    c_cat = dimensao(cabecalho, "Geral")
    return pd.DataFrame({
        "mes": pd.to_datetime(linhas[c_mes + "C"], format="%Y%m"),
        "codigo_sidra": linhas[c_cat + "C"].astype(int),
        "variavel": linhas[c_var + "C"].astype(str),
        "variavel_nome": linhas[c_var + "N"],
        # a API usa '...', '-', 'X' para "sem dado": viram vazio (NaN), nunca zero
        "valor": pd.to_numeric(linhas["V"], errors="coerce"),
    })


def baixar_pesos(lista_codigos):
    """O peso e opcional: se algo falhar, o CSV sai sem ele e o script avisa."""
    try:
        dados = buscar(f"t/{TABELA}/n1/all/v/{VARIAVEL_PESO}/p/all/c315/{lista_codigos}")
        validar_resposta(dados, "os pesos")
        pesos = para_df(dados)
        if not pesos["variavel_nome"].str.contains("peso", case=False).all():
            print("AVISO: a variavel 66 nao parece ser o peso. Seguindo sem peso.")
            return None
        return pesos[["mes", "codigo_sidra", "valor"]].rename(columns={"valor": "peso_mensal"})
    except (Exception, SystemExit) as erro:
        print(f"AVISO: nao consegui baixar os pesos ({erro}). Seguindo sem peso.")
        return None


def conferir(tabela, grupos):
    """Confere com um numero que o IBGE divulgou: IPCA de 2021 = 10,06%."""
    codigo_geral = next(c for c, n in grupos.items() if n == NOME_GERAL)
    ref = tabela[(tabela["codigo_sidra"] == codigo_geral)
                 & (tabela["mes"] == pd.Timestamp("2021-12-01"))]
    if ref.empty:
        print("Conferencia: dez/2021 nao encontrada no resultado.")
        return
    valor = float(ref["var_12m"].iloc[0])
    situacao = "OK" if abs(valor - 10.06) < 0.05 else "ATENCAO, confira com o IBGE"
    print(f"Conferencia: IPCA em 12 meses de dez/2021 = {valor:.2f}% (IBGE: 10,06%) -> {situacao}")


def main():
    grupos = descobrir_grupos()
    print("Categorias encontradas:", ", ".join(grupos.values()))
    lista = ",".join(str(c) for c in grupos)

    dados = buscar(f"t/{TABELA}/n1/all/v/{','.join(VARIAVEIS)}/p/all/c315/{lista}")
    validar_resposta(dados, "os valores do IPCA")
    valores = para_df(dados)

    tabela = (valores.pivot(index=["mes", "codigo_sidra"], columns="variavel", values="valor")
              .rename(columns=VARIAVEIS).reset_index())
    faltando = set(VARIAVEIS.values()) - set(tabela.columns)
    if faltando:
        sys.exit(f"A API nao devolveu as variaveis: {faltando}")

    pesos = baixar_pesos(lista)
    if pesos is not None:
        tabela = tabela.merge(pesos, on=["mes", "codigo_sidra"], how="left")
    else:
        tabela["peso_mensal"] = float("nan")

    tabela["grupo"] = tabela["codigo_sidra"].map(grupos)
    tabela = (tabela[["mes", "codigo_sidra", "grupo", "var_mensal", "var_ano",
                      "var_12m", "peso_mensal"]]
              .sort_values(["mes", "codigo_sidra"]).reset_index(drop=True))
    assert not tabela.duplicated(["mes", "codigo_sidra"]).any(), "linhas repetidas"

    for pasta in (PASTA_EX / "dados", PASTA_COMUM):
        pasta.mkdir(parents=True, exist_ok=True)
    opcoes = dict(sep=";", decimal=",", index=False, encoding="utf-8-sig",
                  date_format="%Y-%m-%d")
    tabela.to_csv(PASTA_EX / "dados" / "ipca_grupos.csv", **opcoes)
    tabela.to_csv(PASTA_COMUM / "ex02_ipca_grupos.csv", **opcoes)

    print(f"\nLinhas: {len(tabela)} | grupos: {tabela['grupo'].nunique()} | "
          f"periodo: {tabela['mes'].min():%m/%Y} a {tabela['mes'].max():%m/%Y}")
    print("Valores vazios por coluna:")
    print(tabela.isna().sum().to_string())
    conferir(tabela, grupos)
    print("\nArquivo gerado: exercicios/02-painel-inflacao-ipca/dados/ipca_grupos.csv")


if __name__ == "__main__":
    main()
