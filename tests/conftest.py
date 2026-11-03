"""Fixtures compartilhadas: dado sintético pequeno + config apontando para ele."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import yaml


@pytest.fixture
def dataset_sintetico(tmp_path):
    """Gera um Parquet pequeno e separável, e devolve seu caminho."""
    rng = np.random.default_rng(42)
    n = 200
    x1 = rng.normal(0, 1, n)
    x2 = rng.normal(0, 1, n)
    x3 = rng.normal(0, 1, n)
    # Alvo com sinal claro, para as métricas serem estáveis no teste.
    y = (x1 + x2 > 0).astype(int)

    df = pd.DataFrame({"x1": x1, "x2": x2, "x3": x3, "y": y})
    caminho = tmp_path / "sintetico.parquet"
    df.to_parquet(caminho, index=False)
    return caminho


@pytest.fixture
def config_sintetico(tmp_path, dataset_sintetico):
    """Config YAML válido apontando para o dado sintético e tracking local isolado."""
    conteudo = {
        "name": "exemplo_modelo",
        "data_source": {"type": "parquet", "path": str(dataset_sintetico)},
        "tracking": {
            "experiment_name": "teste_exemplo_modelo",
            "databricks": False,
            # Tracking isolado no tmp_path: o teste não suja o backend do repo.
            "tracking_uri": f"sqlite:///{tmp_path / 'mlflow.db'}",
        },
        "output_dir": str(tmp_path / "processed"),
        "params": {
            "target": "y",
            "features": ["x1", "x2", "x3"],
            "split": "random",
            "test_size": 0.25,
            "random_state": 42,
            "n_estimators": 10,
            "max_depth": 3,
        },
    }
    caminho = tmp_path / "exemplo_modelo.yaml"
    with caminho.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(conteudo, fh)
    return caminho
