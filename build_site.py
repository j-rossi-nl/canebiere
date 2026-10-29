"""Exécute les notebooks et écrit le site statique dans site/."""
import shutil

from argparse import ArgumentParser
from pathlib import Path

import nbformat
import papermill

from nbconvert import HTMLExporter

from utils.accueil import render_index
from utils.articles import season_page_name, season_pages
from utils.season import render_season

ROOT = Path(__file__).parent

# Le template JupyterLab limite les svg à la largeur de la page: les graphes larges
# seraient écrasés, on préfère les faire défiler horizontalement.
CSS = """<style>
  .vega-embed { overflow-x: auto; }
  .vega-embed svg { max-width: none; }
</style>
"""

# notebook -> page
PAGES = {
    "generate_academies.ipynb": "academies",
    "generate_notes.ipynb": "notes",
    "generate_opponents.ipynb": "opponents",
    "generate_words.ipynb": "words",
}


def render(notebook: Path, page: str, out_dir: Path, parameters: dict | None = None, title: str | None = None):
    print(f"{notebook.name} -> {page}.html", flush=True)
    executed = papermill.execute_notebook(
        str(notebook), None, parameters=parameters or {}, cwd=str(ROOT), progress_bar=False
    )
    nb = nbformat.from_dict(executed)
    if title is not None:
        nb.metadata["title"] = title
    body, _ = HTMLExporter(exclude_input=True, exclude_output_prompt=True).from_notebook_node(nb)
    body = body.replace("</head>", CSS + "</head>", 1)
    (out_dir / f"{page}.html").write_text(body, encoding="utf-8")


def main():
    parser = ArgumentParser("build-site")
    parser.add_argument("--out", type=Path, default=ROOT / "site")
    parser.add_argument("--only", nargs="*", help="pages à générer (ex: index 2024_2025), toutes par défaut")
    args = parser.parse_args()

    if args.only is None and args.out.exists():
        shutil.rmtree(args.out)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / ".nojekyll").touch()

    wanted = lambda page: args.only is None or page in args.only

    for notebook, page in PAGES.items():
        if wanted(page):
            render(ROOT / notebook, page, args.out)

    if wanted("index"):
        print("accueil -> index.html", flush=True)
        render_index(args.out)

    for season in season_pages():
        page = season_page_name(season)
        if wanted(page):
            print(f"saison {season} -> {page}.html", flush=True)
            render_season(season, args.out)


if __name__ == "__main__":
    main()
