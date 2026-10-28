# Source cells of generate_opponents.ipynb
# --- cell 0 (code) ---
import pickle
import string

from babel.dates import format_date

import altair as alt
import numpy as np
import pandas as pd
import re
import spacy

from bs4 import BeautifulSoup
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
from gensim.corpora.dictionary import Dictionary

from utils.data import notes, resultats

# --- cell 1 (code) ---
pd.options.display.max_colwidth = 200
DEFAULT_WIDTH = 800

_ = alt.data_transformers.disable_max_rows()

# --- cell 2 (code) ---
with open("canebiere.pickle", "rb") as src:
    df: pd.DataFrame = pickle.load(src)

blaah = df[df['Auteur'] == 'Blaah'].reset_index()
matchs = resultats(blaah)

# --- cell 3 (markdown) ---
# # L'OM de Blaah

# --- cell 4 (markdown) ---
# ## Nombre de buts dans les matches

# --- cell 5 (code) ---
matchs["Nb Buts"] = matchs["Buts_R"] + matchs["Buts_V"]

# --- cell 6 (code) ---
alt.Chart(matchs[["Nb Buts"]]).mark_bar().encode(
    x=alt.X("Nb Buts:O", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("count():Q", title="Matchs"),
    color=alt.Color("Nb Buts:O", scale=alt.Scale(scheme="greens")),
    tooltip=["Nb Buts:O", alt.Tooltip("count():Q", title="Nb Matches")]
).properties(
    width=DEFAULT_WIDTH
)

# --- cell 7 (markdown) ---
# ## Nombre de buts de l'OM

# --- cell 8 (code) ---
alt.Chart(matchs[["Buts_OM"]]).mark_bar().encode(
    x=alt.X("Buts_OM:O", title="Buts de l'OM", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("count():Q", title='Matchs'),
    color="Buts_OM:O",
    tooltip=[alt.Tooltip("Buts_OM:O", title="Buts de l'OM"), alt.Tooltip("count():Q", title="Nb Matches")]
).properties(
    width=DEFAULT_WIDTH
)

# --- cell 9 (markdown) ---
# ## Nombre de buts de l'adversaire

# --- cell 10 (code) ---
alt.Chart(matchs[["Buts_Adversaire"]]).mark_bar().encode(
    x=alt.X("Buts_Adversaire:O", title="Buts de l'adversaire", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("count():Q", title="Matchs"),
    color=alt.Color("Buts_Adversaire:O", scale=alt.Scale(scheme="reds")),
    tooltip=[alt.Tooltip("Buts_Adversaire:O", title="Buts de l'OM"), alt.Tooltip("count():Q", title="Nb Matches")]
).properties(
    width=DEFAULT_WIDTH
)

# --- cell 11 (markdown) ---
# ## Des saisons et des buts marqués

# --- cell 12 (code) ---
matchs["Victoire"] = matchs["Buts_OM"] > matchs["Buts_Adversaire"]
matchs["Défaite"] =  matchs["Buts_OM"] < matchs["Buts_Adversaire"]
matchs["Nul"] =  matchs["Buts_OM"] == matchs["Buts_Adversaire"]

# --- cell 13 (code) ---
def date_to_season(date: pd.Timestamp) -> str:
    # La saison N/N+1 dure du 1er Juillet N au 30 Juin N+1
    month = date.month
    year = date.year

    if month <=6:
        season = f'{year-1}-{year}'
    else:
        season = f'{year}-{year+1}'

    return season
    
matchs['Saison'] = matchs['Date'].apply(date_to_season)

# --- cell 14 (code) ---
games_total = alt.Chart(matchs).mark_bar().encode(
    x=alt.X('Saison:N', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('count(Date)', title='Matchs'),
    color=alt.Color('Saison'),
    tooltip=['Saison', alt.Tooltip('count(Date)', title='Matchs')]
).properties(
    width=800
)

goals_total = alt.Chart(matchs).mark_bar().encode(
    x=alt.X('Saison:N', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('sum(Buts_OM)', title='Buts de l\'OM'),
    color=alt.Color('Saison'),
    tooltip=['Saison', alt.Tooltip('sum(Buts_OM)', title='Buts de l\'OM')]
).properties(
    width=800
)

goals_per_game = alt.Chart(matchs).mark_bar().encode(
    x=alt.X('Saison:N', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('mean(Buts_OM)', title='Buts de l\'OM par Match'),
    color=alt.Color('Saison'),
    tooltip=['Saison', alt.Tooltip('mean(Buts_OM)', title='Buts de l\'OM par Match', format='.2f')]
).properties(
    width=800
)

games_total & goals_total & goals_per_game

# --- cell 15 (markdown) ---
# ## Des saisons et des buts encaissés

# --- cell 16 (code) ---
games_total = alt.Chart(matchs).mark_bar().encode(
    x=alt.X('Saison:N', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('count(Date)', title='Matchs'),
    color=alt.Color('Saison'),
    tooltip=['Saison', alt.Tooltip('count(Date)', title='Matchs')]
).properties(
    width=800
)

goals_total = alt.Chart(matchs).mark_bar().encode(
    x=alt.X('Saison:N', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('sum(Buts_Adversaire)', title='Buts contre l\'OM'),
    color=alt.Color('Saison'),
    tooltip=['Saison', alt.Tooltip('sum(Buts_Adversaire)', title='Buts contre l\'OM')]
).properties(
    width=800
)

goals_per_game = alt.Chart(matchs).mark_bar().encode(
    x=alt.X('Saison:N', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('mean(Buts_Adversaire)', title='Buts contre l\'OM par Match'),
    color=alt.Color('Saison'),
    tooltip=['Saison', alt.Tooltip('mean(Buts_Adversaire)', title='Buts contre l\'OM par Match', format='.2f')]
).properties(
    width=800
)

games_total & goals_total & goals_per_game

# --- cell 17 (markdown) ---
# ## Des saisons et des victoires, des défaites et des nuls

# --- cell 18 (code) ---
vnd = matchs.groupby('Saison').agg({'Victoire': 'sum', 'Défaite': 'sum', 'Nul': 'sum'}).reset_index().melt(id_vars='Saison', value_vars=['Victoire', 'Nul', 'Défaite'])

# --- cell 19 (code) ---
counts = alt.Chart(vnd).mark_bar().encode(
    x=alt.X("Saison:N", title=None, axis=alt.Axis(ticks=False, labels=False)),
    y=alt.Y('value:Q', title=''),
    color=alt.Color('variable', scale=alt.Scale(domain=['Victoire', 'Nul', 'Défaite'], range=['#54a24b', '#d8b5a5', '#e45756'])),
    tooltip=[alt.Tooltip("Saison", title="Saison"), "variable", alt.Tooltip("value", title="Académies")]
).properties(
    width=800
)

pcts = alt.Chart(vnd).mark_bar().encode(
    x=alt.X("Saison:N", title=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y("value:Q", title="", stack="normalize", axis=alt.Axis(format="%")),
    color='variable',
    tooltip=[alt.Tooltip("Saison", title="Saison"), "variable", alt.Tooltip("value", title="Académies")]
).properties(
    width=800
)

counts & pcts

# --- cell 20 (markdown) ---
# ## Différence de But par Adversaire

# --- cell 21 (code) ---
by_adv = matchs.groupby("Adversaire").size()

# --- cell 22 (code) ---
# Il va falloir traiter les doublons...

# * ASSE / Saint-Etienne / Saint-Étienne
# * TFC / Toulouse
# * MHSC / Montpellier
# * Gazélec / Gazéléc
# * Konyaspot / Konyasport
# * Salzbourg / Salzburg
# * Athletic / Bilbao

# --- cell 23 (code) ---
normalize = [
    {"dups": ["ASSE", "Saint-Etienne", "Saint-Étienne"], "norm": "Saint-Étienne"},
    {"dups": ["TFC", "Toulouse"], "norm": "Toulouse"},
    {"dups": ["MHSC", "Montpellier"], "norm": "Montpellier"},
    {"dups": ["Gazélec", "Gazéléc"], "norm": "Gazélec Ajaccio"},
    {"dups": ["Konyaspor", "Konyasport"], "norm": "Konyaspor"},
    {"dups": ["Salzbourg", "Salzburg"], "norm": "Salzburg"},
    {"dups": ["Athletic", "Bilbao"], "norm": "Athletic Bilbao"},
    {"dups": ["Atlético"], "norm": "Atletico Madrid"},
    {"dups": ["PAOK", 'PAOK Salonique'], "norm": "PAOK"}
]

# --- cell 24 (code) ---
matchs["Publications"] = 1

# --- cell 25 (code) ---
for dedup in normalize:
    matchs.loc[matchs["Adversaire"].isin(dedup["dups"]), "Adversaire"] = dedup["norm"]

# --- cell 26 (code) ---
by_adv = matchs.groupby("Adversaire").agg({"Publications": "sum", "Buts_OM": "sum", "Buts_Adversaire": "sum"})
by_adv.reset_index(inplace=True)

# --- cell 27 (code) ---
by_adv["Différence de Buts"] = by_adv["Buts_OM"] - by_adv["Buts_Adversaire"]

# --- cell 28 (code) ---
slider = alt.binding_range(min=by_adv["Publications"].min(), max=by_adv["Publications"].max(), step=1, name="Nombre Minimum de Matchs: ")
select_nb_matches = alt.selection_single(name="matches", fields=["Publications"], bind=slider, init={"Publications": 1})

alt.Chart(by_adv).mark_bar().encode(
    y="Différence de Buts",
    x=alt.X(
        "Adversaire:O", 
        sort=alt.EncodingSortField(field="Différence de Buts", order="ascending"),
        axis=alt.Axis(labelAngle=-45)
    ),
    color=alt.Color("Différence de Buts", scale=alt.Scale(scheme="redyellowgreen")),
    tooltip=["Adversaire", "Différence de Buts", alt.Tooltip("Publications", title="Nb Matches")]
).add_selection(
    select_nb_matches
).transform_filter(
    "datum.Publications >= matches_Publications"
). properties(height=600,width=1200)

# --- cell 29 (markdown) ---
# ## Différentiel Victoire / Défaite par Adversaire

# --- cell 30 (code) ---
by_adv = matchs.groupby("Adversaire").agg({"Publications": "sum", "Victoire": "sum", "Défaite": "sum", "Nul": "sum"})
by_adv.reset_index(inplace=True)
by_adv["Différence Victoire / Défaite"] = by_adv["Victoire"].astype(int) - by_adv["Défaite"].astype(int)

# --- cell 31 (code) ---
chart = alt.Chart(by_adv).mark_bar().encode(
    y="Différence Victoire / Défaite",
    x=alt.X(
        "Adversaire:O", 
        sort=alt.EncodingSortField(field="Différence Victoire / Défaite"),
        axis=alt.Axis(labelAngle=-45)
    ),
    color=alt.Color("Différence Victoire / Défaite", scale=alt.Scale(domain=[-10, 10], scheme="redyellowgreen")),
    tooltip=["Adversaire", "Victoire", "Nul", "Défaite", alt.Tooltip("Publications", title="Nb Matches")]
).add_selection(
    select_nb_matches
).transform_filter(
    "datum.Publications >= matches_Publications"
). properties(height=600,width=1200)

chart
