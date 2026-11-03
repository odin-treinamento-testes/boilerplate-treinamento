#!/usr/bin/env python3
"""Cancela: convenções de nomenclatura ODIN.

Lint dos nomes de repos/artefatos do núcleo em toda a documentação .md.
Stdlib only. Uso: python3 tools/check_convencoes.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORG = "ODIN-NDados-Poli-Junior"
PROIBIDOS = {
    r"core-plugins\b": "use 'core-plugin' (singular) — nome de repo confirmado",
    r"\bretrospective\.md\b": "use 'retrospectiva.md' — padrão da KB",
    r"core-biblioteca\b": "use 'core-manual' — repo renomeado",
}

erros: list[str] = []
for p in RAIZ.rglob("*.md"):
    if ".git" in p.parts:
        continue
    texto = p.read_text(encoding="utf-8", errors="ignore")
    rel = p.relative_to(RAIZ)
    for padrao, motivo in PROIBIDOS.items():
        for m in re.finditer(padrao, texto):
            linha = texto[: m.start()].count("\n") + 1
            erros.append(f"{rel}:{linha} — '{m.group()}' proibido: {motivo}")
    for m in re.finditer(r"marketplace add\s+(\S+)/", texto):
        if m.group(1) != ORG:
            linha = texto[: m.start()].count("\n") + 1
            erros.append(f"{rel}:{linha} — org handle '{m.group(1)}' ≠ '{ORG}'")

if erros:
    print("AVISO (não barra o merge): convenções de nomenclatura ODIN\n")
    for e in erros:
        print(f"  - {e}")
    sys.exit(1)
print("OK: convenções ODIN respeitadas.")
sys.exit(0)
