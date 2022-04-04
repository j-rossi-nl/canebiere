import pickle
import re

from operator import xor
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from bs4 import BeautifulSoup


def unpickle_blaah(from_: Path) -> pd.DataFrame:
    with from_.open("rb") as src:
        df: pd.DataFrame = pickle.load(src)

    blaah = df[df["Auteur"] == "Blaah"].copy()
    return blaah


def _resultats(blaah_: pd.DataFrame) -> pd.DataFrame:
    home = re.compile(r"^\s*OM\s*[\-–]\s*(?P<adversaire>[\w\- ]+)")
    away = re.compile(r"^\s*(?P<adversaire>[\w\- ]+)\s*[\-–]\s*OM")

    # ## Les exceptions à la règle
    # * Les académies de rétrospective
    test = [
        xor((home.match(txt) is not None), (away.match(txt) is not None))
        for txt in blaah_["Titre"]
    ]
    blaah = blaah_.iloc[[x[0] for x in filter(lambda t: t[1], enumerate(test))]][
        ["Titre", "Date", "url", "html"]
    ].copy()

    def extract_adversaire(x):
        m = home.match(x)
        if m is None:
            m = away.match(x)

        if m is None:
            raise ValueError(f"Can't process {x}")
        return m.group("adversaire").strip()

    blaah["Domicile"] = blaah["Titre"].apply(lambda x: home.match(x) is not None)
    blaah["Adversaire"] = blaah["Titre"].apply(extract_adversaire)

    score = re.compile(r"^\s*\((?P<receveuse>\d+)\s*-\s*(?P<visiteuse>\d+).*\)")

    def extract_buts(x):
        def apres_equipes(x_):
            m = home.match(x_)
            if m is None:
                m = away.match(x_)
            if m is None:
                raise ValueError(f"Can't process {x_}")

            return x_[m.end() :]

        txt = apres_equipes(x)
        m = score.match(txt)
        if m is None:
            return pd.Series(
                [np.nan, np.nan], index=["Buts_Receveuse", "Buts_Visiteuse"]
            )
        return pd.Series(
            [int(m.group("receveuse")), int(m.group("visiteuse"))],
            index=["Buts_Receveuse", "Buts_Visiteuse"],
        )

    buts = blaah["Titre"].apply(extract_buts)
    blaah[["Buts_R", "Buts_V"]] = buts
    blaah["Buts_OM"] = blaah.apply(
        lambda x: x["Buts_R"] if x["Domicile"] else x["Buts_V"], axis=1
    )
    blaah["Buts_Adversaire"] = blaah.apply(
        lambda x: x["Buts_V"] if x["Domicile"] else x["Buts_R"], axis=1
    )
    blaah.dropna(subset=["Buts_OM", "Buts_Adversaire"], inplace=True)
    for col in ["Buts_OM", "Buts_Adversaire", "Buts_V", "Buts_R"]:
        blaah[col] = blaah[col].astype(int)

    def resultat(x):
        om = x["Buts_OM"]
        adv = x["Buts_Adversaire"]

        if om > adv:
            return "Victoire"
        if om == adv:
            return "Nul"
        return "Défaite"

    blaah["Résultat"] = blaah.apply(resultat, axis=1)
    return blaah


def resultats(blaah_: pd.DataFrame, to_: Path = Optional[None]) -> pd.DataFrame:
    blaah = _resultats(blaah_)
    blaah.drop(columns=["html"], inplace=True)
    if to_ is not None:
        blaah.to_csv(to_, index=False)
    return blaah


def notes(blaah_: pd.DataFrame, to_: Optional[Path] = None) -> pd.DataFrame:
    blaah = _resultats(blaah_)

    notes_re = re.compile(r"^(?P<joueur>[\w\s]+) \(.*,?\w*(?P<note>\d[\+\-]?)/5.*")
    note_num = re.compile(r"^(?P<num>\d+)(?P<plus>[\+\-]?)$")

    def extract_notes(row: pd.Series) -> pd.DataFrame:
        
        adversaire = row["Adversaire"]
        if row['Domicile']:
            match_title = f'OM - {adversaire} {row["Buts_R"]}-{row["Buts_V"]}'
        else:
            match_title = f'{adversaire} - OM {row["Buts_R"]}-{row["Buts_V"]}'
        date = row["Date"]
        soup = BeautifulSoup(row["html"], features="lxml")
        data = []
        for st in soup.find_all(["strong", "b", "i", "em"]):
            m = notes_re.match(st.text)
            if m is None:
                continue

            m_num = note_num.match(m.group("note"))
            if m_num is None:
                continue

            plus_moins = m_num.group("plus")
            note_ = float(m_num.group("num"))
            if len(plus_moins) > 0:
                note_ += 0.4 if plus_moins == "+" else -0.4
            data.append(
                {
                    "Adversaire": adversaire,
                    "Date": date,
                    "Match_Teams": match_title,
                    "Joueur": m.group("joueur").replace("\n", " ").strip().title(),
                    "Note_txt": m.group("note"),
                    "Note_num": note_,
                }
            )
        return pd.DataFrame(data)

    notes = pd.concat(blaah.apply(extract_notes, axis=1).values)

    # Les noms d'un meme joueur varient d'une fois sur l'autre
    normalize = [
        {"dups": ["Amavi", "Amavier"], "norm": "Amavi"},
        {"dups": ["De Ceglie", "Détchéyé"], "norm": "De Ceglie"},
        {"dups": ["Leya Iseka", "Iseka Leya"], "norm": "Leya Iseka"},
        {"dups": ["Lopez", "Maxime Lopez"], "norm": "Lopez"},
        {"dups": ["Doria", "Diego Armando Maradoria"], "norm": "Doria"},
        {"dups": ["Njie", "Nvier"], "norm": "Njie"},
        {"dups": ["Batshuayi", "Michybre"], "norm": "Batshuayi"},
    ]

    for dedup in normalize:
        notes.loc[notes["Joueur"].isin(dedup["dups"]), "Joueur"] = dedup["norm"]

    # On a 2 Lopez (Maxime et Pau) heureusement ils n'ont jamais joué ensemble
    notes.loc[
        (notes["Date"].dt.year <= 2020) & (notes["Joueur"] == "Lopez"), "Joueur"
    ] = "Maxime Lopez"
    notes.loc[
        (notes["Date"].dt.year > 2020) & (notes["Joueur"] == "Lopez"), "Joueur"
    ] = "Pau Lopez"

    notes["Match"] = notes["Adversaire"] + " " + notes["Date"].dt.strftime("%d/%m/%Y")
    notes["sort"] = (notes["Date"].dt.strftime("%Y%m%d")).astype(int)
    notes["count"] = 1
    notes["match_rank"] = notes["sort"].rank(ascending=False, method="dense")

    if to_ is not None:
        notes.to_csv(to_, index=False)

    return notes


if __name__ == "__main__":
    blaah = unpickle_blaah(Path("./canebiere.pickle"))
    resultats(blaah, Path("./dashboard/web/static/resultats.csv"))
    notes(blaah, Path("./dashboard/web/static/notes.csv"))
