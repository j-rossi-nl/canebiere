# La Canebière Académie

Des statistiques parfaitement inutiles sur [La Canebière Académie](https://horsjeu.net/category/france/lelite/la-canebiere-academie/),
publiées sur <https://j-rossi-nl.github.io/canebiere/>.

## Le pipeline

1. **Scraper** (`scraper/`): récupère les nouvelles académies via l'API REST WordPress de horsjeu.net,
   du plus récent au plus ancien, et s'arrête dès qu'il retrouve une académie déjà connue.
   Les articles sont stockés dans `data/articles/<saison>.jsonl` (versionnés dans git).
2. **Préparation** (`data_creation.py`): passe les textes dans spaCy et écrit `canebiere.pickle` (non versionné).
3. **Site** (`generate_website.sh`): exécute les notebooks et écrit les pages HTML dans `site/`.
   L'accueil et les pages de saison ne passent pas par un notebook: `utils/accueil.py` et `utils/season.py`
   calculent les chiffres et les graphes Altair, les gabarits Jinja de `templates/` (qui partagent `base.html.j2`)
   font la mise en page (`uv run python -m utils.accueil`, `uv run python -m utils.season 2025-2026`).

Le workflow GitHub Actions `update.yml` enchaîne les trois étapes chaque jour, commite les nouvelles
académies sur `main` et publie `site/` sur GitHub Pages.

## En local

```bash
uv sync
(cd scraper && uv run scrapy crawl canebiere_spider)
uv run python data_creation.py
./generate_website.sh
```
