"""Testes do gerador de conda.yaml (Decisão 2 / Rules 02 e 03).

Garantem que o artefato é derivado do pyproject, determinístico, e que o repo não
consegue commitar um manifesto fora de sync sem o CI perceber.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from tools.gen_conda import DESTINO, gerar, versao_python

PYPROJECT_FALSO = """\
[project]
name = "projeto-teste"
requires-python = "==3.11.*"
dependencies = ["zlib-wrapper>=1.0", "abc-lib>=2.0"]
"""


def test_versao_python_extrai_de_specifiers():
    assert versao_python("==3.11.*") == "3.11"
    assert versao_python(">=3.11,<3.12") == "3.11"
    assert versao_python("~=3.12.0") == "3.12"


def test_versao_python_rejeita_specifier_invalido():
    with pytest.raises(ValueError):
        versao_python("")


def test_gerar_e_deterministico(tmp_path):
    p = tmp_path / "pyproject.toml"
    p.write_text(PYPROJECT_FALSO, encoding="utf-8")
    assert gerar(p) == gerar(p)


def test_gerar_ordena_dependencias(tmp_path):
    """Ordem estável independe da ordem do pyproject (determinismo)."""
    p = tmp_path / "pyproject.toml"
    p.write_text(PYPROJECT_FALSO, encoding="utf-8")

    conteudo = gerar(p)
    pip_deps = yaml.safe_load(conteudo)["dependencies"][2]["pip"]
    assert pip_deps == ["abc-lib>=2.0", "zlib-wrapper>=1.0"]


def test_gerar_produz_yaml_valido_com_cabecalho(tmp_path):
    p = tmp_path / "pyproject.toml"
    p.write_text(PYPROJECT_FALSO, encoding="utf-8")

    conteudo = gerar(p)
    assert "ARQUIVO GERADO — NÃO EDITE" in conteudo

    dados = yaml.safe_load(conteudo)
    assert dados["name"] == "projeto-teste"
    assert dados["dependencies"][0] == "python=3.11"


def test_conda_yaml_versionado_esta_em_sync():
    """Rule 03: o artefato commitado reflete o pyproject atual."""
    assert DESTINO.exists(), "platform/conda.yaml não existe; rode tools/gen_conda.py"
    assert DESTINO.read_text(encoding="utf-8") == gerar()


def test_conda_yaml_nao_leva_extras_de_plataforma():
    """databricks-connect/pyspark não entram no ambiente do job (ver docstring)."""
    pip_deps = yaml.safe_load(DESTINO.read_text(encoding="utf-8"))["dependencies"][2]["pip"]
    nomes = " ".join(pip_deps)
    assert "databricks-connect" not in nomes
    assert "pyspark" not in nomes


def test_gerador_nao_importa_nada_do_nucleo():
    """O gerador é uma ferramenta de build: não depende do núcleo nem o contamina."""
    texto = Path("tools/gen_conda.py").read_text(encoding="utf-8")
    for proibido in ("from common", "import common", "from models", "import models"):
        assert proibido not in texto
