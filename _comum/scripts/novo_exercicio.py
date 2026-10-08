"""Cria a estrutura de um novo exercicio a partir dos templates.

Uso:
    python _comum/scripts/novo_exercicio.py 02 vendas-fantasma
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
TEMPLATES = RAIZ / "_comum" / "templates"
ARQUIVOS = {
    "README.md": "README.template.md",
    "enunciado.md": "enunciado.template.md",
    "como-gerar-dados.md": "como-gerar-dados.template.md",
    "passo-a-passo.md": "passo-a-passo.template.md",
}


def main():
    if len(sys.argv) < 3:
        print("Uso: python _comum/scripts/novo_exercicio.py 02 nome-do-exercicio")
        sys.exit(1)

    numero, slug = sys.argv[1], sys.argv[2]
    destino = RAIZ / "exercicios" / f"{numero}-{slug}"
    if destino.exists():
        print(f"A pasta {destino} ja existe. Nada foi alterado.")
        sys.exit(1)

    for sub in ("gabarito", "dados", "powerbi"):
        (destino / sub).mkdir(parents=True)
        (destino / sub / ".gitkeep").touch()

    for nome, modelo in ARQUIVOS.items():
        texto = (TEMPLATES / modelo).read_text(encoding="utf-8")
        texto = texto.replace("{{NUMERO}}", numero).replace("{{SLUG}}", slug)
        (destino / nome).write_text(texto, encoding="utf-8")

    print(f"Exercicio criado em {destino}")
    print(f"Proximo passo: criar _comum/scripts/ex{numero}_gerar_dados.py")


if __name__ == "__main__":
    main()