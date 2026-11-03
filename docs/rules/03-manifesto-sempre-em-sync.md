# Rule 03 — Manifesto sempre em sync

Os artefatos de plataforma gerados a partir do `pyproject.toml` (ex.: `conda.yaml`)
têm que refletir o `pyproject.toml` atual.

**Faça:** ao mudar o `pyproject.toml`, regerar os artefatos de plataforma no mesmo
commit. O CI checa se estão em sync.
**Não faça:** commitar um `pyproject.toml` alterado deixando `conda.yaml`/requirements
defasados. Manifesto fora de sync é falha de CI.
