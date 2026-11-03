"""Teste de fumaça: garante que o pacote e as dependências base importam."""


def test_pacote_common_importa():
    import common

    assert common.__version__


def test_dependencias_base_importam():
    # Núcleo instala sozinho, sem extras de plataforma (Rule 06).
    import pandas  # noqa: F401
    import pydantic  # noqa: F401
    import sklearn  # noqa: F401
    import yaml  # noqa: F401
