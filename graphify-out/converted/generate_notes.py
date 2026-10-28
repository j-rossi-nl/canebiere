# Source cells of generate_notes.ipynb
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

# --- cell 3 (code) ---
def date_to_season(date: pd.Timestamp) -> str:
    # La saison N/N+1 dure du 1er Juillet N au 30 Juin N+1
    month = date.month
    year = date.year

    if month <=6:
        season = f'{year-1}-{year}'
    else:
        season = f'{year}-{year+1}'

    return season
    
df['Saison'] = df['Date'].apply(date_to_season)

# --- cell 4 (code) ---
blaah = df[df['Auteur'] == 'Blaah'].reset_index()

matchs = resultats(blaah)
notation = notes(blaah)

# --- cell 5 (markdown) ---
# # Des Joueurs, des Notes

# --- cell 6 (code) ---
stats = pd.DataFrame({"Académie": ["Académie", "Académie"], "Notes": ["Récupérées", "Non Récupérées"], "Nombre": [notation["Date"].nunique(), blaah.shape[0] - notation["Date"].nunique()]})

alt.Chart(stats).mark_bar().encode(
    x=alt.X("Académie:N", axis=alt.Axis(labels=False)),
    y=alt.Y("Nombre:Q", stack="zero"),
    color=alt.Color("Notes:N", legend=alt.Legend(title="Récupération Automatique"), scale=alt.Scale(domain=["Récupérées", "Non Récupérées"], range=["green", "red"])),
    tooltip="Nombre:Q"
)

# --- cell 7 (code) ---
by_joueur = notation.groupby("Joueur").agg({"Note_num": ["count", "mean"]})
by_joueur.columns = by_joueur.columns.droplevel()
by_joueur.reset_index(inplace=True)

# --- cell 8 (code) ---
chart = alt.Chart(by_joueur).mark_bar().encode(
    x=alt.X(
        field="Joueur", 
        type="ordinal", 
        sort=alt.EncodingSortField(field="count", order="descending"),
        axis=alt.Axis(labelAngle=-45, labelFontSize=14)
    ),
    y=alt.Y("count:Q", title="Nombre de Notes"),
    color=alt.Color("count:Q", scale=alt.Scale(scheme="greenblue")),
    tooltip=["Joueur", alt.Tooltip("count:Q", title="# Notes")]
)

chart.configure_header(
    titleColor='green',
    titleFontSize=14,
    labelColor='red',
    labelFontSize=14
)

chart

# --- cell 9 (markdown) ---
# ## Les notes de l'OM par match

# --- cell 10 (code) ---
notation['Saison'] = notation['Date'].apply(date_to_season)

# --- cell 11 (code) ---
by_match_by_note = notation.groupby(["Saison", "Match", "Note_num"]).agg({"Joueur": "count", "sort": "max"}).reset_index()

base_circles = alt.Chart(by_match_by_note).mark_circle().encode(
    y=alt.Y(
        'Match:N',
        title=None,
        axis=alt.Axis(ticks=False, grid=False, labelPadding=20, labelFontSize=14),
        sort=alt.EncodingSortField("sort", op="max", order="descending")
    ),
    x=alt.X(
        'Note_num:Q',
        title='Note',
        axis=alt.Axis(grid=False)
    ),
    color=alt.Color(
        'Note_num:Q', 
        legend=None, 
        scale=alt.Scale(domain=[0.0,5.0], scheme="redyellowgreen")
    ),
    size=alt.Size(
        "Joueur:Q",
        legend=None,
        scale=alt.Scale(domain=[0.0, by_match_by_note["Joueur"].max()], range=[0.0, 4000.0])
    ),
    tooltip=["Match:N", alt.Tooltip("Note_num:Q", title="Note"), alt.Tooltip("Joueur:N", title="# Joueurs")]
)

chart = alt.hconcat()

for season in sorted(notation['Saison'].unique(), reverse=True):
    chart |= base_circles.transform_filter(alt.datum.Saison == season).properties(title=season)

chart

# --- cell 12 (markdown) ---
# ## Les moyennes

# --- cell 13 (code) ---
by_joueur_by_note = notation.groupby(["Joueur", "Note_num"]).agg({"Date": "count"})
by_joueur_by_note = by_joueur_by_note.reset_index()
by_joueur_by_note.columns = ["Joueur", "Note", "count"]

# --- cell 14 (code) ---
slider = alt.binding_range(min=by_joueur["count"].min(), max=by_joueur["count"].max(), step=1, name="Nombre Minimum de Notes: ")
select_nb_matches = alt.selection_single(name="matches", fields=["count"], bind=slider, init={"count": 1})

classement_moyenne = alt.Chart(notation).mark_bar().transform_aggregate(
    count="count(Note_num)",
    moyenne="mean(Note_num)",
    groupby=["Joueur"]
).encode(
    x=alt.X(
        field="Joueur", 
        type="ordinal", 
        sort="-y",
        axis=alt.Axis(labelAngle=-45, labelFontSize=14)
    ),
    y=alt.Y("moyenne:Q", title="Moyenne"),
    color=alt.Color("moyenne:Q", scale=alt.Scale(scheme="redyellowgreen", domain=[0.0, 5.0])),
    tooltip=["Joueur", alt.Tooltip("count:Q", title="# Notes"), alt.Tooltip("moyenne:Q", title="Moyenne", format='.2f')]
).add_selection(
    select_nb_matches
).transform_filter(
    'datum.count >= matches_count'
)

classement_moyenne.configure_header(
    titleColor='green',
    titleFontSize=14,
    labelColor='red',
    labelFontSize=14
)

classement_moyenne

# --- cell 15 (markdown) ---
# ## Le détail par joueur

# --- cell 16 (code) ---
notes_joueurs = alt.Chart(notation).mark_bar().encode(
    y=alt.Y(
        'Joueur:N',
        title=None,
        axis=alt.Axis(labelFontSize=16),
    ),
    x=alt.X(
        'count(Note_num):Q', 
        title="",
        stack='normalize',
        axis=alt.Axis(labels=False, ticks=False)
    ),
    order=alt.Order("Note_num:Q", sort="ascending"),
    color=alt.Color('Note_num:Q', scale=alt.Scale(scheme="redyellowgreen", domain=[0.0, 5.0])),
    tooltip=["Joueur", alt.Tooltip("Note_num:Q", title="Note"), alt.Tooltip("count(Note_num):Q", title="Nombre de fois")]
)

moyennes = alt.Chart(notation).mark_bar().transform_aggregate(
    count="count(Note_num)",
    moyenne="mean(Note_num)",
    groupby=["Joueur"]
).encode(
    y=alt.Y(
        field="Joueur", 
        type="ordinal", 
        title="",
        axis=alt.Axis(labels=False, ticks=False)
    ),
    x=alt.X(
        "moyenne:Q", 
        title="Moyenne",
        axis=alt.Axis(grid=False)
    ),
    color=alt.Color("moyenne:Q", scale=alt.Scale(scheme="redyellowgreen", domain=[0.0, 5.0])),
    tooltip=["Joueur", alt.Tooltip("count:Q", title="# Notes"), alt.Tooltip("moyenne:Q", title="Moyenne", format='.2f')]
)

notes_joueurs | moyennes
