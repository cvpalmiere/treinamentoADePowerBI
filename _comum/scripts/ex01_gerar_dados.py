"""Exercicio 01 - Carmem Sandiego.

Gera o CSV SUJO com 2000 suspeitos (mais 40 linhas duplicadas) e um gabarito
escondido: exatamente 1 suspeita satisfaz TODAS as pistas do enunciado.

Uso (na raiz do repositorio, com o ambiente virtual ativo):
    python _comum/scripts/ex01_gerar_dados.py
"""
import json
import random
import unicodedata
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

SEMENTE = 42
N_SUSPEITOS = 2000
N_DUPLICADOS = 40

random.seed(SEMENTE)
rng = np.random.default_rng(SEMENTE)

RAIZ = Path(__file__).resolve().parents[2]
PASTA_EX = RAIZ / "exercicios" / "01-carmem-sandiego"
PASTA_COMUM = RAIZ / "_comum" / "dados"

NOMES = ["João", "Maria", "José", "Ana", "Pedro", "Luíza", "Carlos", "Fernanda",
         "Lucas", "Beatriz", "Rafael", "Camila", "Gustavo", "Juliana", "André",
         "Patrícia", "Marcelo", "Aline", "Rodrigo", "Tatiane", "Felipe", "Larissa",
         "Thiago", "Renata", "Bruno", "Vanessa", "Diego", "Sônia", "Eduardo", "Mônica"]
SOBRENOMES = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves",
              "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho",
              "Araújo", "Gonçalves", "Barbosa", "Monteiro", "Montes", "Rocha", "Dias",
              "Teixeira", "Cardoso", "Nunes", "Moreira", "Lopes", "Vieira", "Fernandes",
              "Mendes", "Pinto"]
PROFISSOES = ["Piloto", "Guia Turístico", "Fotógrafo", "Engenheiro", "Médico", "Professor",
              "Chef de Cozinha", "Advogado", "Músico", "Jornalista", "Designer", "Contador"]
CABELOS = ["castanho", "preto", "loiro", "ruivo", "grisalho"]
CIDADES = ["Lisboa", "Madrid", "Roma", "Paris", "Berlim", "Praga", "Viena", "Atenas",
           "Cairo", "Istambul", "Tóquio", "Bogotá", "Nova York", "Cidade do México",
           "Buenos Aires"]

# A culpada. Satisfaz todas as pistas do enunciado.
CULPADA = {
    "nome": "Helena Montenegro Teixeira",
    "profissao": "Guia Turístico",
    "altura_cm": 171,
    "cor_cabelo": "castanho",
    "tem_tatuagem": True,
    "data_nascimento": date(1989, 3, 14),
    "ultima_cidade": "Lisboa",
    "valor_gasto_viagens": 31500,
}


def sem_acento(texto):
    decomposto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


def casa_pistas(r):
    """True se a linha satisfaz TODAS as pistas (compara em forma limpa)."""
    return (
        168 <= r["altura_cm"] <= 174
        and r["cor_cabelo"] in ("castanho", "preto")
        and bool(r["tem_tatuagem"])
        and sem_acento(r["profissao"]) in ("Piloto", "Guia Turistico", "Fotografo")
        and "Mont" in sem_acento(r["nome"])
        and sem_acento(r["ultima_cidade"]) in ("Lisboa", "Madrid", "Roma")
        and date(1985, 1, 1) <= r["data_nascimento"] <= date(1992, 12, 31)
        and 20000 <= r["valor_gasto_viagens"] <= 40000
    )


def gerar_base():
    """Dados corretos (ainda sem sujeira). Garante UMA unica culpada."""
    linhas = []
    for _ in range(N_SUSPEITOS - 1):
        nasc = date(1950, 1, 1) + timedelta(days=int(rng.integers(0, 365 * 55)))
        linhas.append({
            "nome": " ".join([random.choice(NOMES), random.choice(SOBRENOMES),
                              random.choice(SOBRENOMES)]),
            "profissao": random.choice(PROFISSOES),
            "altura_cm": int(rng.normal(171, 9)),
            "cor_cabelo": random.choice(CABELOS),
            "tem_tatuagem": bool(rng.random() < 0.3),
            "data_nascimento": nasc,
            "ultima_cidade": random.choice(CIDADES),
            "valor_gasto_viagens": int(np.clip(rng.lognormal(9.5, 0.9), 300, 500000)),
        })
    linhas.append(dict(CULPADA))
    random.shuffle(linhas)
    for i, linha in enumerate(linhas, start=1):
        linha["id"] = i
    df = pd.DataFrame(linhas)[["id", "nome", "profissao", "altura_cm", "cor_cabelo",
                               "tem_tatuagem", "data_nascimento", "ultima_cidade",
                               "valor_gasto_viagens"]]

    # Qualquer outra pessoa que case com todas as pistas perde a tatuagem.
    for idx, r in df.iterrows():
        if r["nome"] != CULPADA["nome"] and casa_pistas(r):
            df.at[idx, "tem_tatuagem"] = False
    return df


def gerar_referencia_limpa(df):
    """O que uma limpeza perfeita produz (gabarito da etapa Excel)."""
    ref = df.copy()
    for col in ("nome", "profissao", "cor_cabelo", "ultima_cidade"):
        ref[col] = ref[col].map(lambda t: sem_acento(t).title())
    ref["tem_tatuagem"] = ref["tem_tatuagem"].astype(int)
    ref["data_nascimento"] = ref["data_nascimento"].map(lambda d: d.isoformat())
    return ref


# ---------- Sujeira ----------
SIM = ["Sim", "sim", "SIM", "S", "1", "True", "verdadeiro", "yes"]
NAO = ["Não", "nao", "NÃO", "N", "0", "False", "falso", "no"]
FORMATOS_DATA = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y"]


def sujar_texto(t):
    r = rng.random()
    if r < 0.25:
        t = sem_acento(t)
    elif r < 0.40:
        t = t.upper()
    elif r < 0.55:
        t = t.lower()
    elif r < 0.65:
        t = sem_acento(t).upper()
    r = rng.random()
    if r < 0.10:
        t = " " + t
    elif r < 0.20:
        t = t + "  "
    elif r < 0.25:
        t = t.replace(" ", "  ", 1)
    return t


def sujar_altura(cm):
    f = random.random()
    if f < 0.6:
        return str(cm)
    if f < 0.8:
        return f"{cm} cm"
    return f"{cm / 100:.2f}".replace(".", ",") + " m"


def sujar_valor(v):
    f = random.random()
    if f < 0.4:
        return str(v)
    if f < 0.7:
        return "R$ " + f"{v:,}".replace(",", ".")
    if f < 0.85:
        return f"{v:,}".replace(",", ".")
    return f"R${v}"


def sujar(df):
    eh_culpada = (df["nome"] == CULPADA["nome"]).values
    sujo = pd.DataFrame({
        "id": df["id"],
        "nome": df["nome"].map(sujar_texto),
        "profissao": df["profissao"].map(sujar_texto),
        "altura_cm": df["altura_cm"].map(sujar_altura),
        "cor_cabelo": df["cor_cabelo"].map(sujar_texto),
        "tem_tatuagem": df["tem_tatuagem"].map(lambda v: random.choice(SIM if v else NAO)),
        "data_nascimento": df["data_nascimento"].map(
            lambda d: d.strftime(random.choice(FORMATOS_DATA))),
        "ultima_cidade": df["ultima_cidade"].map(sujar_texto),
        "valor_gasto_viagens": df["valor_gasto_viagens"].map(sujar_valor),
    })

    # Nulos (~2%). A culpada nunca recebe nulo.
    for col in ("profissao", "cor_cabelo"):
        mascara = (rng.random(len(sujo)) < 0.02) & ~eh_culpada
        sujo.loc[mascara, col] = ""

    # Duplicatas exatas (a culpada nao e duplicada).
    duplicadas = sujo[~eh_culpada].sample(N_DUPLICADOS, random_state=SEMENTE)
    sujo = pd.concat([sujo, duplicadas]).sample(frac=1, random_state=SEMENTE)
    return sujo.reset_index(drop=True)


def main():
    base = gerar_base()
    referencia = gerar_referencia_limpa(base)
    sujo = sujar(base)

    total_que_casam = int(sum(casa_pistas(r) for _, r in base.iterrows()))
    assert total_que_casam == 1, f"Esperado 1 suspeito, achei {total_que_casam}"

    for pasta in (PASTA_EX / "dados", PASTA_EX / "gabarito", PASTA_COMUM):
        pasta.mkdir(parents=True, exist_ok=True)

    sujo.to_csv(PASTA_EX / "dados" / "suspeitos_sujo.csv",
                sep=";", index=False, encoding="utf-8-sig")
    sujo.to_csv(PASTA_COMUM / "ex01_suspeitos_sujo.csv",
                sep=";", index=False, encoding="utf-8-sig")
    referencia.to_csv(PASTA_EX / "gabarito" / "suspeitos_limpo_referencia.csv",
                      sep=";", index=False, encoding="utf-8-sig")

    culpada_id = int(base.loc[base["nome"] == CULPADA["nome"], "id"].iloc[0])
    (PASTA_EX / "gabarito" / "gabarito_oculto.json").write_text(
        json.dumps({"id": culpada_id, "nome": CULPADA["nome"], "semente": SEMENTE},
                   ensure_ascii=False, indent=2),
        encoding="utf-8")

    print(f"Linhas no CSV sujo: {len(sujo)} (2000 suspeitos + {N_DUPLICADOS} duplicadas)")
    print(f"Suspeitos que casam com todas as pistas: {total_que_casam}")
    print("Arquivos gerados em exercicios/01-carmem-sandiego e _comum/dados")


if __name__ == "__main__":
    main()