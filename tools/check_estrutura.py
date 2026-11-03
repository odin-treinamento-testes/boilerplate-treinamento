#!/usr/bin/env python3
"""CI do projeto: CONTRATO (barra o merge) e CONSELHO (só avisa).

- CONTRATO: o que, se quebrar, quebra o projeto sem ninguém perceber. É o job
  `contrato` do CI, o único que a regra de CI da organização deve exigir para o merge.
- CONSELHO: estrutura recomendada e convenções. Aparece como aviso no PR e não
  impede o merge.

Quem decide flexibilizar o escopo é o coordenador, ao aprovar o PR. Se o projeto não
precisa mais de um item do contrato, tire-o da lista abaixo no mesmo PR e explique o
motivo na descrição: o CI não barra uma decisão que o coordenador pode tomar.

Stdlib only: roda sem instalar nada.

Uso:
    python3 tools/check_estrutura.py              # contrato (o que o CI exige)
    python3 tools/check_estrutura.py --conselho   # conselho (só avisa; sai sempre com 0)
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SCRIPT = "tools/check_estrutura.py"
ORG = "ODIN-NDados-Poli-Junior"
MARKETPLACE = "core-plugin"
PLUGIN = "ndados@core-plugin"
COMO_DECLARAR = "https://github.com/ODIN-NDados-Poli-Junior/core-plugin#instalar"
NO_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"

# ==== Configuração deste boilerplate =============================================
# Um item com "|" aceita qualquer uma das alternativas.
# CONTRATO: sem estes, o projeto quebra sem ninguém perceber.
CONTRATO = {
    "CLAUDE.md": "é o contexto-mestre que o Claude Code lê em toda sessão",
    ".claude/settings.json": "declara o plugin do núcleo e as permissões do projeto",
    ".github/CODEOWNERS": "sem ele, a aprovação do coordenador deixa de ser obrigatória",
    "context/README.md": "é o índice do context/, por onde a equipe acha as decisões",
    "context/99_conclusoes": "é dali que sai o cadastro do projeto na KB, no encerramento",
    "pyproject.toml": "é a fonte única das dependências: sem ele o uv não instala nada",
}
# CONSELHO: estrutura recomendada. Faltar gera só aviso.
CONSELHO = {
    ".claude/README.md": "explica a camada .claude/ para quem chega",
    "context/glossario.md": "guarda os termos do cliente",
    "context/project-context.md": "resumo vivo do projeto, que as skills de registro atualizam",
    ".claude/rules": "regras do projeto que o Claude Code carrega",
    ".claude/skills": "skills específicas do projeto",
}
# Pastas de dados do cliente: nada versionado nelas além de .gitkeep e README.md.
PASTAS_DE_DADOS = [
    "pipeline/data/raw",
    "pipeline/data/interim",
    "pipeline/data/processed",
    "pipeline/data/external",
]
# Extensões tratadas como dado do cliente, com os arquivos que são exceção.
DADOS_POR_EXTENSAO: dict[str, set[str]] = {}
# Entradas que o .gitignore deveria ter (conselho: o contrato confere o que foi commitado).
GITIGNORE_RECOMENDADO = [".env", "pipeline/data/raw/", "CLAUDE.local.md"]
# Limite dos .md de context/, em bytes. Acima dele, o arquivo é dividido em <nome>_pt2.md,
# <nome>_pt3.md... (conselho: só avisa). O project-context.md é o resumo vivo e fica fora.
LIMITE_CONTEXTO = 8192
SEM_LIMITE_CONTEXTO = {"project-context.md"}
# Lint dos nomes do núcleo nos .md: no CD fica com tools/check_convencoes.py.
LINT_DE_NOMES = False
# ================================================================================

NOMES_PROIBIDOS = {
    r"core-plugins\b": "use 'core-plugin' (singular)",
    r"\bretrospective\.md\b": "use 'retrospectiva.md', o padrão da KB",
    r"core-biblioteca\b": "use 'core-manual', o repositório foi renomeado",
}
NOME_DE_SKILL = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
PERMITIDOS_EM_DADOS = {".gitkeep", "README.md"}
IGNORAR_DIRS = {".git", ".venv", "node_modules"}


class Relatorio:
    """Junta os achados e, no GitHub Actions, os anota no PR (erro ou aviso)."""

    def __init__(self, nivel: str) -> None:
        self.nivel = nivel  # "error" no contrato, "warning" no conselho
        self.itens: list[str] = []

    def add(self, msg: str, arquivo: str | None = None, linha: int | None = None) -> None:
        local = f"{arquivo}:{linha}" if arquivo and linha else (arquivo or "")
        self.itens.append(f"{local} — {msg}" if local else msg)
        if NO_ACTIONS:
            titulo = "Contrato (barra o merge)" if self.nivel == "error" else "Conselho (só avisa)"
            props = [f"title={titulo}"]
            if arquivo:
                props.append(f"file={arquivo}")
            if linha:
                props.append(f"line={linha}")
            print(f"::{self.nivel} {','.join(props)}::{msg}")


def existe(item: str) -> bool:
    return any((RAIZ / alternativa).exists() for alternativa in item.split("|"))


def versionados() -> list[str]:
    """O que está commitado: é isso que importa, não o que existe só no disco."""
    try:
        saida = subprocess.run(
            ["git", "ls-files", "-z"], cwd=RAIZ, capture_output=True, text=True, check=True
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [
            str(p.relative_to(RAIZ))
            for p in RAIZ.rglob("*")
            if p.is_file() and not IGNORAR_DIRS & set(p.relative_to(RAIZ).parts)
        ]
    return [caminho for caminho in saida.split("\0") if caminho]


def linhas_do_gitignore() -> set[str] | None:
    gitignore = RAIZ / ".gitignore"
    if not gitignore.is_file():
        return None
    return {linha.strip() for linha in gitignore.read_text(encoding="utf-8").splitlines()}


def pastas_de_skill() -> list[Path]:
    pasta = RAIZ / ".claude" / "skills"
    return sorted(p for p in pasta.iterdir() if p.is_dir()) if pasta.is_dir() else []


def frontmatter(texto: str) -> str | None:
    achado = re.match(r"^---\s*\n(.*?)\n---\s*\n", texto, re.DOTALL)
    return achado.group(1) if achado else None


def campo(bloco: str, nome: str) -> str | None:
    achado = re.search(rf"(?m)^{nome}:\s*(.+)$", bloco)
    return achado.group(1).strip().strip("\"'") if achado else None


def checar_contrato(r: Relatorio) -> None:
    dica = (
        f"Se o projeto não precisa mais dele, tire-o de CONTRATO em {SCRIPT} no mesmo PR; "
        "quem decide é o coordenador, ao aprovar."
    )
    for item, motivo in CONTRATO.items():
        if not existe(item):
            r.add(f"falta {item.replace('|', ' ou ')}: {motivo}. {dica}")

    settings = RAIZ / ".claude" / "settings.json"
    if settings.is_file():
        try:
            config = json.loads(settings.read_text(encoding="utf-8"))
        except json.JSONDecodeError as erro:
            r.add(
                f"não é JSON válido ({erro}). Com o arquivo quebrado, o Claude Code ignora as "
                "configurações do projeto, inclusive o plugin do núcleo.",
                ".claude/settings.json",
            )
        else:
            config = config if isinstance(config, dict) else {}
            marketplaces = config.get("extraKnownMarketplaces") or {}
            plugins = config.get("enabledPlugins") or {}
            if MARKETPLACE not in marketplaces or plugins.get(PLUGIN) is not True:
                r.add(
                    f"não declara o plugin do núcleo (extraKnownMarketplaces.{MARKETPLACE} e "
                    f"enabledPlugins.{PLUGIN}). Sem isso, as skills e os agentes do núcleo "
                    f"somem do projeto. Recoloque as duas chaves: {COMO_DECLARAR}",
                    ".claude/settings.json",
                )

    for caminho in versionados():
        nome = Path(caminho).name
        if nome == "CLAUDE.local.md":
            r.add(
                "está versionado. É um arquivo pessoal e pode ter segredos: rode "
                "git rm --cached no arquivo e mantenha-o no .gitignore.",
                caminho,
            )
        if nome == ".env" or (nome.startswith(".env.") and nome != ".env.example"):
            r.add(
                "segredo versionado. Tire do git (git rm --cached) e troque as credenciais "
                "que estavam nele: o histórico do git guarda o arquivo.",
                caminho,
            )
        for pasta in PASTAS_DE_DADOS:
            if caminho.startswith(f"{pasta}/") and nome not in PERMITIDOS_EM_DADOS:
                r.add(
                    f"arquivo versionado em {pasta}/, que é pasta de dados do cliente. Tire do "
                    "git (git rm --cached) e confira se o .gitignore cobre a pasta.",
                    caminho,
                )
        excecoes = DADOS_POR_EXTENSAO.get(Path(caminho).suffix.lower())
        if excecoes is not None and caminho not in excecoes:
            r.add(
                f"arquivo {Path(caminho).suffix} versionado: este boilerplate trata esse tipo "
                "como dado do cliente. Tire do git (git rm --cached) ou, se não é dado do "
                f"cliente, acrescente-o às exceções em DADOS_POR_EXTENSAO, em {SCRIPT}; o "
                "coordenador decide no PR.",
                caminho,
            )

    for pasta in pastas_de_skill():
        rel = f".claude/skills/{pasta.name}"
        skill = pasta / "SKILL.md"
        if not skill.is_file():
            r.add(
                "pasta sem SKILL.md. O Claude Code só encontra skill em "
                ".claude/skills/<nome>/SKILL.md, um nível abaixo: pasta de agrupamento não "
                "funciona. Mova cada skill para .claude/skills/<nome>/, ou crie o SKILL.md se "
                "a pasta é uma skill.",
                rel,
            )
            continue
        bloco = frontmatter(skill.read_text(encoding="utf-8", errors="ignore"))
        nome = campo(bloco, "name") if bloco else None
        if nome and not NOME_DE_SKILL.fullmatch(nome):
            r.add(
                f"name '{nome}' fora do formato que o Claude Code aceita (minúsculas, números "
                "e hífens, como minha-skill); a skill pode não carregar.",
                f"{rel}/SKILL.md",
            )


def checar_conselho(r: Relatorio) -> None:
    dica = (
        "É a estrutura recomendada do boilerplate. Se o projeto não precisa, tire o item "
        f"de CONSELHO em {SCRIPT}."
    )
    for item, motivo in CONSELHO.items():
        if not existe(item):
            r.add(f"falta {item.replace('|', ' ou ')}: {motivo}. {dica}")

    gitignore = linhas_do_gitignore()
    faltando = [e for e in GITIGNORE_RECOMENDADO if gitignore is None or e not in gitignore]
    if gitignore is None and faltando:
        r.add(
            f"o projeto não tem .gitignore. Crie um com {', '.join(faltando)}, para dados do "
            "cliente e segredos não irem para o git por engano."
        )
    elif faltando:
        r.add(
            f"o .gitignore não tem {', '.join(faltando)}. Essas entradas evitam que dados do "
            "cliente e segredos sejam commitados por engano.",
            ".gitignore",
        )

    for pasta in pastas_de_skill():
        skill = pasta / "SKILL.md"
        if not skill.is_file():
            continue
        rel = f".claude/skills/{pasta.name}/SKILL.md"
        bloco = frontmatter(skill.read_text(encoding="utf-8", errors="ignore"))
        if bloco is None:
            r.add(
                "sem frontmatter (--- no topo). O Claude Code usa o nome da pasta, mas é a "
                "description que faz a skill ser usada na hora certa.",
                rel,
            )
            continue
        nome = campo(bloco, "name")
        if not campo(bloco, "description"):
            r.add("sem description. É por ela que o Claude Code decide quando usar a skill.", rel)
        if nome and NOME_DE_SKILL.fullmatch(nome) and nome != pasta.name:
            r.add(
                f"name '{nome}' diferente do nome da pasta ({pasta.name}). Funciona, mas "
                "confunde quem procura a skill.",
                rel,
            )

    pasta_contexto = RAIZ / "context"
    if pasta_contexto.is_dir():
        for caminho in sorted(pasta_contexto.rglob("*.md")):
            if caminho.name in SEM_LIMITE_CONTEXTO or "checkpoints" in caminho.parts:
                continue
            tamanho = caminho.stat().st_size
            if tamanho > LIMITE_CONTEXTO:
                r.add(
                    f"tem {tamanho} bytes, acima do limite de {LIMITE_CONTEXTO} dos arquivos de "
                    "context/. Divida entre seções: a parte 1 mantém o nome, as seguintes viram "
                    "<nome>_pt2.md, <nome>_pt3.md..., cada uma com o frontmatter, o H1 com "
                    "(parte N) e o link para a próxima, e todas entram no README.md da pasta.",
                    str(caminho.relative_to(RAIZ)),
                )

    if LINT_DE_NOMES:
        for caminho in RAIZ.rglob("*.md"):
            if IGNORAR_DIRS & set(caminho.relative_to(RAIZ).parts):
                continue
            texto = caminho.read_text(encoding="utf-8", errors="ignore")
            rel = str(caminho.relative_to(RAIZ))
            for padrao, motivo in NOMES_PROIBIDOS.items():
                for achado in re.finditer(padrao, texto):
                    linha = texto[: achado.start()].count("\n") + 1
                    r.add(f"'{achado.group()}': {motivo}.", rel, linha)
            for achado in re.finditer(r"marketplace add\s+(\S+)/", texto):
                if achado.group(1) != ORG:
                    linha = texto[: achado.start()].count("\n") + 1
                    r.add(f"org '{achado.group(1)}' no lugar de '{ORG}'.", rel, linha)


def main() -> int:
    conselho = "--conselho" in sys.argv[1:]
    r = Relatorio("warning" if conselho else "error")
    if conselho:
        checar_conselho(r)
        if r.itens:
            print(f"\nCONSELHO: {len(r.itens)} aviso(s). Não barram o merge.\n")
            for item in r.itens:
                print(f"  - {item}")
            print("\nQuem decide se vale corrigir agora é o coordenador, no PR.")
        else:
            print("OK: nenhum aviso de estrutura ou convenção.")
        return 0

    checar_contrato(r)
    if r.itens:
        print(f"\nCONTRATO: {len(r.itens)} item(ns) barram o merge. Cada um diz como resolver.\n")
        for item in r.itens:
            print(f"  - {item}")
        print(
            "\nSe a mudança foi intencional, quem decide é o coordenador: ajuste a lista em "
            f"{SCRIPT} no mesmo PR."
        )
        return 1
    print("OK: contrato respeitado (estrutura essencial, plugin, dados e segredos fora do git).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
