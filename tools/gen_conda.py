"""Gera `platform/conda.yaml` a partir do `pyproject.toml` (Decisão 2).

O `pyproject.toml` é a FONTE ÚNICA de dependências. O conda.yaml da plataforma é um
artefato DERIVADO — nunca escrito à mão (Rule 02). Este script é a única forma
legítima de produzi-lo, e o resultado é determinístico: mesma entrada, mesma saída,
byte a byte.

Uso:
    uv run python tools/gen_conda.py            # (re)gera platform/conda.yaml
    uv run python tools/gen_conda.py --check    # falha se estiver fora de sync (CI, Rule 03)

Nota sobre escopo: o conda.yaml leva as dependências BASE do núcleo. Os extras
`databricks` e `spark` ficam de fora de propósito — o runtime do Databricks já
fornece o Spark, e `databricks-connect` serve para conectar DE FORA, não para rodar
dentro do cluster. Instalá-los no job conflitaria com o runtime.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PYPROJECT = RAIZ / "pyproject.toml"
DESTINO = RAIZ / "platform" / "conda.yaml"

CABECALHO = """\
# =============================================================================
# ARQUIVO GERADO — NÃO EDITE
#
# Gerado por tools/gen_conda.py a partir do pyproject.toml, que é a FONTE ÚNICA
# de dependências (Decisão 2 / Rule 02). Qualquer edição manual será perdida na
# próxima geração e o CI acusa manifesto fora de sync (Rule 03).
#
# Para alterar dependências:
#   1. edite o pyproject.toml
#   2. rode: uv run python tools/gen_conda.py
#   3. commite os dois juntos
# =============================================================================
"""


def versao_python(requires_python: str) -> str:
    """Extrai 'X.Y' de um specifier como '==3.11.*' ou '>=3.11,<3.12'.

    O conda precisa de uma versão concreta; o specifier do pyproject é uma faixa.
    """
    achados = re.findall(r"(\d+\.\d+)", requires_python or "")
    if not achados:
        raise ValueError(
            f"Não consegui extrair a versão do Python de requires-python={requires_python!r}."
        )
    return achados[0]


def gerar(pyproject_path: Path = PYPROJECT) -> str:
    """Monta o conteúdo do conda.yaml a partir do pyproject. Determinístico."""
    with pyproject_path.open("rb") as fh:
        dados = tomllib.load(fh)

    projeto = dados["project"]
    nome = projeto["name"]
    py = versao_python(projeto.get("requires-python", ""))
    # sorted() garante a mesma ordem a cada geração, independente do pyproject.
    deps = sorted(projeto.get("dependencies", []))

    linhas = [
        CABECALHO,
        f"name: {nome}",
        "channels:",
        "  - conda-forge",
        "dependencies:",
        f"  - python={py}",
        "  - pip",
        "  - pip:",
    ]
    linhas.extend(f"      - {dep}" for dep in deps)
    return "\n".join(linhas) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera platform/conda.yaml a partir do pyproject.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Não escreve; sai com código 1 se o arquivo estiver fora de sync.",
    )
    args = parser.parse_args()

    conteudo = gerar()

    if args.check:
        if not DESTINO.exists():
            print(
                f"ERRO: {DESTINO.relative_to(RAIZ)} não existe.\n"
                "Rode: uv run python tools/gen_conda.py"
            )
            return 1
        atual = DESTINO.read_text(encoding="utf-8")
        if atual != conteudo:
            print(
                f"ERRO: {DESTINO.relative_to(RAIZ)} está FORA DE SYNC com o pyproject.toml "
                "(Rule 03).\nRode: uv run python tools/gen_conda.py"
            )
            return 1
        print(f"OK: {DESTINO.relative_to(RAIZ)} está em sync com o pyproject.toml.")
        return 0

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(conteudo, encoding="utf-8")
    print(f"Gerado: {DESTINO.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
