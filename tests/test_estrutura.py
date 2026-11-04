from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def test_pastas_do_projeto_existem():
    for pasta in ["ETL", "notebooks", "modelos", "documentos-de-apoio"]:
        assert (RAIZ / pasta).is_dir(), f"a pasta {pasta}/ sumiu do repositório"
