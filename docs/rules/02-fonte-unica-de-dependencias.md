# Rule 02 — Fonte única de dependências

`pyproject.toml` é a única fonte de dependências. `uv.lock` é versionado.

**Faça:** adicionar/remover dependência apenas no `pyproject.toml` (via `uv`).
**Não faça:** editar `platform/conda.yaml` ou qualquer `requirements.txt` à mão. Esses
artefatos são **gerados** a partir do `pyproject.toml`. Escrever à mão recria o bug de
divergência que essa regra existe para matar.
