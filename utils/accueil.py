"""La page d'accueil: le bilan de toutes les académies et une carte par saison."""
from datetime import date
from pathlib import Path

from utils.articles import date_to_season, load_articles, season_page_name, season_pages
from utils.data import notes, resultats
from utils.season import ACADEMIE_URL, ROOT, bilan, templates

# Les pages encore générées par les notebooks
AUTRES = [
    ("words", "Des textes, des mots", "Le vocabulaire des académies, saison après saison."),
    ("opponents", "Des buts, des scores, des adversaires", "Les adversaires préférés et les bêtes noires."),
    ("notes", "Des joueurs, des notes", "Toutes les notes de tous les joueurs."),
    ("academies", "Des auteurs, des académies", "Qui écrit, quand, et combien."),
]


def render_index(out_dir: Path) -> Path:
    articles = load_articles()
    blaah = articles[articles["Auteur"] == "Blaah"]
    matchs = resultats(blaah).sort_values("Date")
    matchs["Saison"] = matchs["Date"].map(date_to_season)

    en_cours = date_to_season(date.today())
    saisons = []
    for season in reversed(season_pages()):
        m = matchs[matchs["Saison"] == season]
        saisons.append({
            "season": season,
            "page": season_page_name(season),
            "en_cours": season == en_cours,
            "bilan": bilan(m),
            "serie": m["Résultat"].tolist(),
        })

    derniere = blaah.sort_values("Date").iloc[-1]
    page = templates().get_template("index.html.j2").render(
        total={
            **bilan(matchs),
            "academies": len(blaah),
            "notes": len(notes(blaah)),
            "depuis": matchs["Date"].min().year,
        },
        saisons=saisons,
        derniere={"Titre": derniere["Titre"], "url": derniere["url"], "Jour": derniere["Date"].strftime("%d/%m/%Y")},
        autres=AUTRES,
        academie_url=ACADEMIE_URL,
    )
    out = out_dir / "index.html"
    out.write_text(page, encoding="utf-8")
    return out


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser("index-page")
    parser.add_argument("--out", type=Path, default=ROOT / "site")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    print(render_index(args.out))
