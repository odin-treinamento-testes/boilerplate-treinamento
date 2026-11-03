#!/usr/bin/env python3
"""Cancela: MANIFESTO SEMPRE EM SYNC (Rules 02 e 03).

Regenera o `platform/conda.yaml` a partir do `pyproject.toml` (a FONTE ÚNICA) e
falha se o resultado diferir do que está versionado. É esta cancela que mata o bug
real de um projeto anterior, onde requirements e conda divergiram.

Delega a geração para `tools/gen_conda.py` de propósito: se este script tivesse a
sua própria cópia da lógica, ele mesmo poderia dessincronizar — que é justamente o
problema que existimos para evitar.

PLATAFORMA OPCIONAL (Rule 06): se o toggle foi Não, `platform/` não existe e não há
manifesto a checar. Nesse caso o script PASSA, informando que pulou — o CI do
esqueleto é o mesmo do projeto-cópia, com ou sem Databricks.

Stdlib only: roda sem `uv sync`.

Uso:
    python3 tools/check_manifest.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PLATAFORMA = RAIZ / "platform"
GERADOR = RAIZ / "tools" / "gen_conda.py"


def main() -> int:
    if not PLATAFORMA.exists():
        print("PULADO: platform/ não existe (toggle Databricks = Não). Nada a checar.")
        return 0

    if not GERADOR.exists():
        print("ERRO: platform/ existe, mas tools/gen_conda.py não.")
        print("O conda.yaml é um artefato GERADO (Rule 02) e ficou sem o seu gerador —")
        print("ninguém consegue mais regerá-lo de forma legítima. Restaure o gerador.")
        return 1

    sys.path.insert(0, str(RAIZ / "tools"))
    from gen_conda import DESTINO, gerar

    if not DESTINO.exists():
        print(f"ERRO: {DESTINO.relative_to(RAIZ)} não existe.")
        print("Rode: uv run python tools/gen_conda.py")
        return 1

    esperado = gerar()
    atual = DESTINO.read_text(encoding="utf-8")

    if atual == esperado:
        print(f"OK: {DESTINO.relative_to(RAIZ)} está em sync com o pyproject.toml (Rule 03).")
        return 0

    print("ERRO: MANIFESTO FORA DE SYNC (Rules 02 e 03)\n")
    print("O pyproject.toml é a FONTE ÚNICA de dependências. O platform/conda.yaml é")
    print("DERIVADO dele e está defasado — provavelmente o pyproject mudou e o artefato")
    print("não foi regerado, ou alguém editou o conda.yaml à mão (proibido).\n")
    print("Como corrigir:")
    print("  1. uv run python tools/gen_conda.py")
    print("  2. commite o pyproject.toml e o conda.yaml JUNTOS\n")
    print("Diferença (esperado vs. versionado):")

    import difflib

    diff = difflib.unified_diff(
        esperado.splitlines(),
        atual.splitlines(),
        fromfile="gerado a partir do pyproject.toml",
        tofile=str(DESTINO.relative_to(RAIZ)),
        lineterm="",
    )
    for linha in diff:
        print(f"  {linha}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
