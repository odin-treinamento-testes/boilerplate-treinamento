#!/usr/bin/env python3
"""Roda o CI inteiro de uma vez: o portão local antes do commit.

É o mesmo conjunto de verificações que o `.github/workflows/ci.yml` roda, separado do
mesmo jeito:

- CONTRATO (barra o merge): estrutura essencial e plugin, erros de Python que quebram,
  pytest e manifesto em sync. Se algo aqui falha, o script sai com erro.
- CONSELHO (só avisa): estrutura recomendada, estilo (ruff), raiz mínima, MLflow
  centralizado, plataforma isolada e convenções. Aparece no resumo como AVISO e não
  muda o resultado.

Quem decide flexibilizar o escopo é o coordenador, ao aprovar o PR. Ao contrário do CI
(que mostra cada job separado), este script roda TODAS as etapas até o fim e imprime
um resumo: você vê tudo de uma vez.

Stdlib only: delega a `uv run` (ruff/pytest) e ao próprio Python (os scripts de
tools/), sem importar nada além da biblioteca padrão.

Uso:
    python3 tools/check.py            # roda tudo em modo verificação (igual ao CI)
    python3 tools/check.py --fix      # aplica ruff format + ruff check --fix antes
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PY = sys.executable


# Cada etapa é (rótulo, comando). A ordem e a divisão espelham o ci.yml.
def contrato() -> list[tuple[str, list[str]]]:
    return [
        ("estrutura essencial e plugin", [PY, "tools/check_estrutura.py"]),
        (
            "erros de Python que quebram",
            ["uv", "run", "ruff", "check", "--select", "E9,F63,F7,F82", "."],
        ),
        ("pytest", ["uv", "run", "pytest"]),
        ("manifesto em sync (Rules 02/03)", [PY, "tools/check_manifest.py"]),
    ]


def conselho(fix: bool) -> list[tuple[str, list[str]]]:
    ruff = (
        [
            ("ruff format", ["uv", "run", "ruff", "format", "."]),
            ("ruff check --fix", ["uv", "run", "ruff", "check", "--fix", "."]),
        ]
        if fix
        else [
            ("ruff check", ["uv", "run", "ruff", "check", "."]),
            ("ruff format --check", ["uv", "run", "ruff", "format", "--check", "."]),
        ]
    )
    return [
        ("estrutura recomendada", [PY, "tools/check_estrutura.py", "--conselho"]),
        *ruff,
        ("raiz mínima (Rule 04)", [PY, "tools/check_root.py"]),
        ("mlflow centralizado (Rule 01)", [PY, "tools/check_mlflow.py"]),
        ("plataforma isolada (Rule 06)", [PY, "tools/check_platform.py"]),
        ("convenções ODIN", [PY, "tools/check_convencoes.py"]),
    ]


def rodar(rotulo: str, comando: list[str]) -> bool:
    print(f"\n{'=' * 70}\n▶ {rotulo}\n{'=' * 70}")
    try:
        resultado = subprocess.run(comando, cwd=RAIZ)
    except FileNotFoundError:
        print(f"ERRO: comando não encontrado: {comando[0]!r}.")
        if comando[0] == "uv":
            print("Instale o uv (https://docs.astral.sh/uv/) — o repo depende dele.")
        return False
    return resultado.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Roda todas as cancelas (portão local pré-commit)."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Aplica ruff format e ruff check --fix antes de verificar.",
    )
    args = parser.parse_args()

    barra = [(rotulo, rodar(rotulo, cmd)) for rotulo, cmd in contrato()]
    avisa = [(rotulo, rodar(rotulo, cmd)) for rotulo, cmd in conselho(args.fix)]

    print(f"\n{'=' * 70}\nRESUMO\n{'=' * 70}")
    print("  CONTRATO (barra o merge)")
    for rotulo, ok in barra:
        print(f"    {'OK    ' if ok else 'FALHOU'}  {rotulo}")
    print("  CONSELHO (só avisa)")
    for rotulo, ok in avisa:
        print(f"    {'OK    ' if ok else 'AVISO '}  {rotulo}")

    falharam = [rotulo for rotulo, ok in barra if not ok]
    avisos = [rotulo for rotulo, ok in avisa if not ok]
    if avisos:
        print(
            f"\n{len(avisos)} aviso(s) de conselho. Não barram o merge; o coordenador decide no PR."
        )
        if not args.fix:
            print("Dica: `python3 tools/check.py --fix` resolve estilo automaticamente.")
    if falharam:
        print(f"\n{len(falharam)} item(ns) do contrato reprovaram. Corrija antes de commitar.")
        return 1

    print("\nContrato verde. Pode commitar com segurança.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
