"""Page d'une saison: les données et les graphes, sans spaCy ni notebook.

Les pages de saison n'ont besoin que des titres et du html des académies:
on part directement des articles versionnés (data/articles) au lieu du pickle.
"""
import json

from dataclasses import dataclass
from pathlib import Path

import altair as alt
import pandas as pd

from jinja2 import Environment, FileSystemLoader, select_autoescape

from utils.articles import date_to_season, load_articles, season_page_name, season_pages
from utils.data import notes, resultats

ROOT = Path(__file__).resolve().parents[1]

ACADEMIE_URL = "https://horsjeu.net/category/france/lelite/la-canebiere-academie/"

# Les couleurs du maillot: blanc, bleu ciel, marine, et l'étoile de 93
BLEU = "#2FAEE0"
MARINE = "#0B2341"
OR = "#C9A227"
SABLE = "#C8BBA6"
ROUGE = "#D64541"

RESULTATS = ["Victoire", "Nul", "Défaite"]
RESULTATS_COULEURS = [BLEU, SABLE, ROUGE]

# Notes de 0 à 5: du rouge au bleu ciel en passant par le sable
NOTES_SCALE = alt.Scale(domain=[0, 2.5, 5], range=[ROUGE, "#EFE6D6", "#1B75BC"], interpolate="rgb")

FONT = "Source Sans 3, Helvetica, Arial, sans-serif"


def _style(chart: alt.TopLevelMixin) -> alt.TopLevelMixin:
    return (
        chart.configure(font=FONT, background="transparent")
        .configure_axis(labelColor=MARINE, titleColor=MARINE, gridColor="#E3EAF0", domainColor="#9FB3C8", tickColor="#9FB3C8")
        .configure_legend(labelColor=MARINE, titleColor=MARINE)
        .configure_view(stroke=None)
    )


@dataclass
class Season:
    season: str
    matchs: pd.DataFrame
    notes: pd.DataFrame

    @classmethod
    def load(cls, season: str) -> "Season":
        articles = load_articles()
        blaah = articles[articles["Auteur"] == "Blaah"]
        matchs = resultats(blaah)
        notation = notes(blaah)

        matchs = matchs[matchs["Date"].map(date_to_season) == season].sort_values("Date").reset_index(drop=True)
        notation = notation[notation["Date"].map(date_to_season) == season]

        matchs["Match"] = matchs.apply(_affiche, axis=1)
        matchs["Score"] = matchs["Buts_OM"].astype(str) + "-" + matchs["Buts_Adversaire"].astype(str)
        matchs["Ecart"] = matchs["Buts_OM"] - matchs["Buts_Adversaire"]
        # "Rennes-OM (1-0) : La Canebière Académie marque mal" -> "marque mal"
        matchs["Sous_titre"] = matchs["Titre"].str.replace(r"^.*Canebière Académie\s*", "", regex=True)
        matchs["Jour"] = matchs["Date"].dt.strftime("%d/%m/%Y")
        matchs["Numero"] = range(1, len(matchs) + 1)
        return cls(season, matchs, notation)

    # -- les chiffres -----------------------------------------------------

    def bilan(self) -> dict:
        m = self.matchs
        counts = m["Résultat"].value_counts()
        return {
            "matchs": len(m),
            "victoires": int(counts.get("Victoire", 0)),
            "nuls": int(counts.get("Nul", 0)),
            "defaites": int(counts.get("Défaite", 0)),
            "buts_pour": int(m["Buts_OM"].sum()),
            "buts_contre": int(m["Buts_Adversaire"].sum()),
        }

    def records(self) -> dict:
        m = self.matchs
        if m.empty:
            return {}
        # à écart égal, on garde la plus récente
        victoire = m.sort_values(["Ecart", "Date"]).iloc[-1]
        defaite = m.sort_values(["Ecart", "Date"], ascending=[True, False]).iloc[0]
        return {
            "victoire": victoire.to_dict() if victoire["Ecart"] > 0 else None,
            "defaite": defaite.to_dict() if defaite["Ecart"] < 0 else None,
        }

    def joueurs(self) -> pd.DataFrame:
        by = self.notes.groupby("Joueur")["Note_num"].agg(["count", "mean"]).reset_index()
        return by.rename(columns={"count": "Notes", "mean": "Moyenne"})

    def podium(self) -> dict:
        by = self.joueurs()
        # Pour le palmarès, il faut avoir été noté sur au moins un quart des matchs
        regulars = by[by["Notes"] >= max(2, len(self.matchs) // 4)]
        if regulars.empty:
            return {}
        return {
            "chouchou": regulars.sort_values(["Moyenne", "Notes"]).iloc[-1].to_dict(),
            "souffre_douleur": regulars.sort_values(["Moyenne", "Notes"], ascending=[True, False]).iloc[0].to_dict(),
            "pilier": by.sort_values(["Notes", "Moyenne"]).iloc[-1].to_dict(),
            "cinq_sur_cinq": int((self.notes["Note_txt"] == "5").sum()),
        }

    # -- les graphes ------------------------------------------------------

    def chart_scores(self) -> alt.TopLevelMixin:
        """Chaque match: les buts de l'OM vers le haut, ceux de l'adversaire vers le bas."""
        m = self.matchs.assign(Buts_Contre=-self.matchs["Buts_Adversaire"])
        x = alt.X(
            "Numero:O",
            title=None,
            axis=alt.Axis(labels=False, ticks=False, domain=False),
            sort="ascending",
        )
        tooltip = [
            alt.Tooltip("Match:N", title="Match"),
            alt.Tooltip("Score:N", title="Score OM"),
            alt.Tooltip("Jour:N", title="Date"),
            alt.Tooltip("Sous_titre:N", title="L'Académie"),
        ]
        base = alt.Chart(m).encode(x=x, tooltip=tooltip, href="url:N")
        pour = base.mark_bar(color=BLEU, cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
            y=alt.Y("Buts_OM:Q", title="Buts", axis=alt.Axis(tickMinStep=1, labelExpr="abs(datum.value)")),
            opacity=alt.condition("datum.Résultat == 'Défaite'", alt.value(0.55), alt.value(1)),
        )
        contre = base.mark_bar(color=ROUGE, cornerRadiusBottomLeft=3, cornerRadiusBottomRight=3).encode(
            y="Buts_Contre:Q",
            opacity=alt.condition("datum.Résultat == 'Victoire'", alt.value(0.55), alt.value(1)),
        )
        zero = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color=MARINE).encode(y="y:Q")
        return _style((pour + contre + zero).properties(width="container", height=260))

    def chart_notes(self) -> alt.TopLevelMixin:
        """Le carnet de notes: un joueur par ligne, un match par colonne."""
        n = self.notes.merge(self.matchs[["Date", "Numero", "Match", "Score", "url"]], on="Date")
        ordre = self.joueurs().sort_values("Notes", ascending=False)["Joueur"].tolist()
        return _style(
            alt.Chart(n)
            .mark_rect(cornerRadius=2, stroke="white", strokeWidth=1)
            .encode(
                x=alt.X("Numero:O", title="Match n°", axis=alt.Axis(labelAngle=0, labelFontSize=10)),
                y=alt.Y("Joueur:N", title=None, sort=ordre, axis=alt.Axis(labelFontSize=12)),
                color=alt.Color("Note_num:Q", scale=NOTES_SCALE, title="Note /5"),
                href="url:N",
                tooltip=[
                    alt.Tooltip("Joueur:N"),
                    alt.Tooltip("Note_txt:N", title="Note"),
                    alt.Tooltip("Match:N"),
                    alt.Tooltip("Score:N", title="Score OM"),
                ],
            )
            .properties(width="container", height=alt.Step(16))
        )

    def chart_moyennes(self) -> alt.TopLevelMixin:
        by = self.joueurs()
        by = by[by["Notes"] > 1]
        base = alt.Chart(by).encode(
            y=alt.Y("Joueur:N", sort="-x", title=None, axis=alt.Axis(labelFontSize=12)),
            x=alt.X("Moyenne:Q", title="Moyenne /5", scale=alt.Scale(domain=[0, 5])),
            tooltip=["Joueur", alt.Tooltip("Notes:Q", title="Notes"), alt.Tooltip("Moyenne:Q", format=".2f")],
        )
        bars = base.mark_bar(cornerRadiusEnd=3, height=12).encode(color=alt.Color("Moyenne:Q", scale=NOTES_SCALE, legend=None))
        labels = base.mark_text(align="left", dx=4, fontSize=11, color=MARINE).encode(text=alt.Text("Moyenne:Q", format=".1f"))
        return _style((bars + labels).properties(width="container", height=alt.Step(18)))

    def chart_distribution(self) -> alt.TopLevelMixin:
        ordre = sorted(self.notes["Note_txt"].unique(), key=lambda t: self.notes.loc[self.notes["Note_txt"] == t, "Note_num"].iloc[0])
        return _style(
            alt.Chart(self.notes)
            .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
            .encode(
                x=alt.X("Note_txt:N", sort=ordre, title="Note", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("count():Q", title="Attributions"),
                color=alt.Color("Note_num:Q", scale=NOTES_SCALE, legend=None),
                tooltip=[alt.Tooltip("Note_txt:N", title="Note"), alt.Tooltip("count():Q", title="Attributions")],
            )
            .properties(width="container", height=220)
        )

    def charts(self) -> dict[str, str]:
        if self.matchs.empty:
            return {}
        charts = {"scores": self.chart_scores()}
        if not self.notes.empty:
            charts |= {
                "notes": self.chart_notes(),
                "moyennes": self.chart_moyennes(),
                "distribution": self.chart_distribution(),
            }
        return {name: chart.to_json(indent=None) for name, chart in charts.items()}


def _affiche(row: pd.Series) -> str:
    return f"OM - {row['Adversaire']}" if row["Domicile"] else f"{row['Adversaire']} - OM"


def render_season(season: str, out_dir: Path) -> Path:
    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape())
    env.filters["note"] = lambda x: f"{x:.2f}".replace(".", ",")

    s = Season.load(season)
    seasons = season_pages()
    i = seasons.index(season)
    page = env.get_template("season.html.j2").render(
        season=season,
        bilan=s.bilan(),
        records=s.records(),
        podium=s.podium(),
        matchs=s.matchs.to_dict("records"),
        # "</" fermerait la balise <script> qui contient les specs
        charts=json.dumps({k: json.loads(v) for k, v in s.charts().items()}, ensure_ascii=False).replace("</", "<\\/"),
        precedente=(seasons[i - 1], season_page_name(seasons[i - 1])) if i > 0 else None,
        suivante=(seasons[i + 1], season_page_name(seasons[i + 1])) if i + 1 < len(seasons) else None,
        academie_url=ACADEMIE_URL,
    )
    out = out_dir / f"{season_page_name(season)}.html"
    out.write_text(page, encoding="utf-8")
    return out


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser("season-page")
    parser.add_argument("seasons", nargs="*", help="ex: 2025-2026, toutes par défaut")
    parser.add_argument("--out", type=Path, default=ROOT / "site")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for season in args.seasons or season_pages():
        print(render_season(season, args.out))
