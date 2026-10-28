# Source cells of generate_words.ipynb
# --- cell 0 (code) ---
import pickle
import string

import altair as alt
import numpy as np
import pandas as pd
import spacy

from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
from gensim.corpora.dictionary import Dictionary

# --- cell 1 (code) ---
pd.options.display.max_colwidth = 200
DEFAULT_WIDTH = 800

_ = alt.data_transformers.disable_max_rows()

# --- cell 2 (code) ---
with open("canebiere.pickle", "rb") as src:
    df: pd.DataFrame = pickle.load(src)

blaah = df[df['Auteur'] == 'Blaah'].reset_index()

# --- cell 3 (markdown) ---
# # Blaah l'académicien

# --- cell 4 (code) ---
lemmatizer = FrenchLefffLemmatizer()

def lemmatize(x: spacy.tokens.Token) -> str:
    pos_2_leff = {
        "VERB": "v",
        "NOUN": "n",
        "ADJ": "a"
    }
    leff_pos = pos_2_leff.get(x.pos_, "n")
    return lemmatizer.lemmatize(word=x.lemma_, pos=leff_pos)

corpus = [[lemmatize(t) for t in doc if not t.is_stop and not t.is_space and len(t) > 2] for doc in blaah["docs"]]
dic = Dictionary(documents=corpus)

# --- cell 5 (markdown) ---
# ## Mots utilisés dans le plus d'académies

# --- cell 6 (code) ---
dfs = pd.DataFrame([{"word": dic[k], "dfs": v} for k, v in dic.dfs.items()])
dfs['first_letter'] = dfs['word'].str[0].str.upper()

dropdown_letter = alt.binding_select(options=list(string.ascii_uppercase), name="Première lettre: ")
select_first_letter = alt.selection_single(name="firstletter", fields=["first_letter"], bind=dropdown_letter, init={"first_letter": 'A'})

slider_docfreq = alt.binding_range(min=dfs['dfs'].min(), max=dfs['dfs'].max(), step=1, name="Nombre Minimum d'Académies: ")
select_nb_acad = alt.selection_single(name="nbacads", fields=["dfs"], bind=slider_docfreq, init={"dfs": 20})

alt.Chart(dfs.sort_values('word')).mark_bar().encode(
    y=alt.Y(
        "dfs:Q", 
        title="Nombre d'académies utilisant le mot",
        scale=alt.Scale(domain=[0, dfs['dfs'].max()])
    ),
    x=alt.X(
        "word:O", 
        axis=alt.Axis(labelAngle=-45),
        title="Mot"
    ),
    color=alt.Color("dfs", scale=alt.Scale(scheme="redyellowgreen", domain=[0, dfs['dfs'].max()])),
    tooltip=[alt.Tooltip(field="word", title="Mot"), alt.Tooltip(field="dfs", title="# Académies")]
).add_selection(
    select_first_letter,
    select_nb_acad
).transform_filter(
    select_first_letter
).transform_filter(
    "datum.dfs >= nbacads_dfs"
).properties(
    height=400
)

# --- cell 7 (markdown) ---
# ## Mots les plus fréquents

# --- cell 8 (code) ---
cfs = pd.DataFrame([{"word": dic[k], "cfs": v} for k, v in dic.cfs.items()])
cfs['first_letter'] = cfs['word'].str[0].str.upper()

dropdown_letter = alt.binding_select(options=list(string.ascii_uppercase), name="Première lettre: ")
select_first_letter = alt.selection_single(name="firstletter", fields=["first_letter"], bind=dropdown_letter, init={"first_letter": 'A'})

slider_docfreq = alt.binding_range(min=cfs['cfs'].min(), max=cfs['cfs'].max(), step=10, name="Nombre Minimum d'utilisations: ")
select_nb_appears = alt.selection_single(name="nbappears", fields=["cfs"], bind=slider_docfreq, init={"cfs": 101})

alt.Chart(cfs.sort_values('word')).mark_bar().encode(
    y=alt.Y(
        "cfs:Q", 
        title="Nombre d'utilisations du mot",
        scale=alt.Scale(domain=[0, cfs['cfs'].max()])
    ),
    x=alt.X(
        "word:O", 
        axis=alt.Axis(labelAngle=-45),
        title="Mot"
    ),
    color=alt.Color("cfs", scale=alt.Scale(scheme="redyellowgreen", domain=[cfs['cfs'].min(), cfs['cfs'].max()])),
    tooltip=[alt.Tooltip(field="word", title="Mot"), alt.Tooltip(field="cfs", title="# Utilisations")]
).add_selection(
    select_first_letter,
    select_nb_appears
).transform_filter(
    select_first_letter
).transform_filter(
    "datum.cfs >= nbappears_cfs"
).properties(
    height=400
)

# --- cell 9 (markdown) ---
# # Les Verbes dans les Titres

# --- cell 10 (code) ---
titres = pd.DataFrame(blaah["Titre"].copy())
titres["Titre_Part2"] = titres["Titre"].str.lower().str.extract(r"^.+(la\s+canebière\s+académiq?u?e[\w\s]+)")

# --- cell 11 (code) ---
titres.dropna(subset=["Titre_Part2"], inplace=True)

# --- cell 12 (code) ---
titres["Titre_Part2"] = titres["Titre_Part2"].str.replace(r"la\s+canebière\s+académiq?u?e", "elle", regex=True)

# --- cell 13 (code) ---
fr = spacy.load('fr_core_news_sm')

# --- cell 14 (code) ---
titres["Titre_Part2_doc"] = titres["Titre_Part2"].apply(fr)

# --- cell 15 (code) ---
def extract_verb(x):
    v = [t.lemma_ for t in x if t.pos_ == "VERB"]
    if len(v) == 0:
        return np.nan
    return lemmatizer.lemmatize(v[0], "v")

titres["Verbe"] = titres["Titre_Part2_doc"].apply(extract_verb)
titres["Publications"] = 1

# --- cell 16 (code) ---
def group_verb(x: str) -> int:
    if x.endswith("er"):
        return 1

    if x.endswith("oir"):
        return 3

    if x.endswith("ir"):
        return 2

    return 3

verbes = pd.DataFrame(titres["Verbe"].dropna().unique(), columns=["Verbe"])
verbes["groupe"] = verbes["Verbe"].apply(group_verb)

# --- cell 17 (code) ---
chart = alt.Chart(titres[["Verbe", "Publications"]].dropna().sort_values(["Publications", "Verbe"], ascending=[False, True])).mark_bar().encode(
    x=alt.X(
        field="Verbe", 
        type="ordinal", 
        sort=alt.EncodingSortField(field="Occurences", order="descending"),
        axis=alt.Axis(labelAngle=-45, labelFontSize=14)
    ),
    y="Occurences:Q",
    color=alt.Color("Occurences:Q", scale=alt.Scale(scheme="greenblue")),
    tooltip=["Verbe", "Occurences:Q"]
).transform_aggregate(
    groupby=["Verbe"],
    Occurences="sum(Publications)"
).transform_filter(
    alt.datum.Occurences >= 1
)

chart.configure_header(
    titleColor='green',
    titleFontSize=14,
    labelColor='red',
    labelFontSize=14
)

chart

# --- cell 18 (code) ---

