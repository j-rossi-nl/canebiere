"""Les mots de la saison: les gimmicks, les surnoms et le concours zoologique.

Tout part du texte des académies (colonne full_text des articles).
"""
import json
import re

from collections import Counter
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SURNOMS = ROOT / "data" / "surnoms.json"

# Les gimmicks qu'on compte, match par match
GIMMICKS = {
    "honte": re.compile(r"honte à nous"),
    "slip": re.compile(r"slipom", re.IGNORECASE),
    "raie": re.compile(r"\bRAIE"),
}

# "Les réseaux : ton dromadaire blatère sur Facebook et BlueSky. Rémy B. remporte le concours zoologique."
_RESEAUX = re.compile(r"(?:Twitter|Bluesky|BlueSky|Facebook|Instagram|compte\))[^.]*?\.\s*")
_GAGNANT = re.compile(
    r"^(?P<nom>[A-ZÀ-Ý][^,;:()«»]{1,30}?)\s+(?:est\s+(?:de nouveau\s+|à nouveau\s+)?)?"
    r"(?:remporte|gagne|Gagne|vainqueur|réussit|survole|revient en tête|s’échappe en tête|"
    r"marque un nouveau point|entre au palmarès)"
)
_PAS_UN_NOM = {"Je", "Il", "Elle", "On", "Nul"}
# Les lecteurs dont le nom s'écrit de plusieurs façons
LECTEURS = {"Johny Kreuz": "Johnny Kreuz"}


def gagnant_concours(texte: str) -> str | None:
    """Le lecteur qui remporte le concours zoologique de cette académie, s'il y en a un."""
    for ligne in texte.split("\n"):
        i = ligne.find("concours zoologique")
        if i < 0:
            continue
        m = _GAGNANT.match(_RESEAUX.split(ligne[:i])[-1].strip())
        if m and m.group("nom").strip() not in _PAS_UN_NOM:
            nom = m.group("nom").strip()
            return LECTEURS.get(nom, nom)
    return None


def palmares_concours(textes: pd.Series, top: int = 5) -> list[dict]:
    gagnants = Counter(g for g in map(gagnant_concours, textes) if g)
    return [{"Lecteur": nom, "Victoires": n} for nom, n in gagnants.most_common(top)]


def gimmicks(matchs: pd.DataFrame) -> pd.DataFrame:
    """Une colonne par gimmick: le nombre d'occurrences dans chaque académie."""
    return pd.DataFrame({nom: matchs["full_text"].str.count(rx) for nom, rx in GIMMICKS.items()}, index=matchs.index)


def load_surnoms() -> list[dict]:
    """[{"surnom": "Jean-Bite", "joueur": "Aubameyang", "variantes": [...], "saisons": [...], "note": "..."}, ...]

    "variantes", "saisons" et "note" sont optionnels: sans "saisons", le surnom vaut pour toutes.
    """
    if not SURNOMS.exists():
        return []
    return [s for s in json.loads(SURNOMS.read_text(encoding="utf-8")) if s.get("joueur")]


def surnoms(textes: pd.Series, season: str) -> list[dict]:
    """Les surnoms employés cette saison, du plus fréquent au moins fréquent."""
    texte = "\n".join(textes)
    out = []
    for s in load_surnoms():
        if s.get("saisons") and season not in s["saisons"]:
            continue
        formes = [s["surnom"], *s.get("variantes", [])]
        rx = re.compile(r"(?<![\w-])(?:" + "|".join(map(re.escape, formes)) + r")(?![\w-])")
        n = len(rx.findall(texte))
        if n:
            out.append({"Surnom": s["surnom"], "Joueur": s["joueur"], "Note": s.get("note"), "Fois": n})
    return sorted(out, key=lambda s: -s["Fois"])
