# Source cells of generate_academies.ipynb
# --- cell 0 (code) ---
import pickle

import altair as alt
import pandas as pd

# --- cell 1 (code) ---
pd.options.display.max_colwidth = 200
DEFAULT_WIDTH = 800

_ = alt.data_transformers.disable_max_rows()

# --- cell 2 (code) ---
with open("canebiere.pickle", "rb") as src:
    df: pd.DataFrame = pickle.load(src)

# --- cell 3 (markdown) ---
# # La Canebière Académie, des origines à aujourd'hui

# --- cell 4 (markdown) ---
# ## Publications par auteur

# --- cell 5 (code) ---
df = df.reset_index()

# --- cell 6 (code) ---
alt.Chart(df[["Auteur", "Publications"]]).mark_bar().encode(
    x=alt.X(
        "Auteur:N",
        axis=alt.Axis(labelAngle=0)
    ),
    y=alt.Y(
        "count(Publications):Q",
        axis=alt.Axis(title="Académies")
    ),
    color="Auteur:N",
    tooltip=["Auteur", alt.Tooltip("count(Publications):Q", title="Académies")]
).properties(
    width=DEFAULT_WIDTH
)

# --- cell 7 (code) ---
alt.Chart(df[["Auteur", "Publications"]]).mark_arc(innerRadius=50, outerRadius=300).encode(
    theta=alt.Theta(
        "count(Publications):Q",
        title="Académies"
    ),
    color="Auteur:N",
    tooltip=["Auteur", alt.Tooltip("count(Publications):Q", title="Académies")]
).properties(
    width=DEFAULT_WIDTH
)

# --- cell 8 (markdown) ---
# ## Publications par Saison et Auteur

# --- cell 9 (code) ---
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

# --- cell 10 (code) ---
raw_counts = alt.Chart(df[["Saison", "Auteur", "Publications"]]).mark_bar().encode(
    x=alt.X("Saison:N", title=None, axis=alt.Axis(ticks=False, labels=False)),
    y=alt.Y("count():Q", title="Académies"),
    color="Auteur:N",
    tooltip=[alt.Tooltip("Saison", title="Saison"), "Auteur", alt.Tooltip("count()", title="Académies")]
).properties(
    width=DEFAULT_WIDTH
)

pct_counts = alt.Chart(df[["Saison", "Auteur", "Publications"]]).mark_bar().encode(
    x=alt.X("Saison:N", title="Saison", axis=alt.Axis(ticks=False, labelAngle=-45)),
    y=alt.Y("count():Q", title="Académies", stack="normalize", axis=alt.Axis(format="%")),
    color="Auteur:N",
    tooltip=[alt.Tooltip("Saison", title="Saison"), "Auteur", alt.Tooltip("count()", title="Académies")]
).properties(
    width=DEFAULT_WIDTH
)

raw_counts & pct_counts

# --- cell 11 (markdown) ---
# ## Longueur du texte par auteur

# --- cell 12 (code) ---
alt.Chart(df[["Auteur", "nb_tokens"]]).transform_density(
    'nb_tokens',
    as_=['Nombre de Mots', 'density'],
    extent=[0, 6000],
    groupby=['Auteur']
).mark_area(orient='horizontal').encode(
    y='Nombre de Mots:Q',
    color='Auteur:N',
    x=alt.X(
        'density:Q',
        stack='center',
        impute=None,
        title=None,
        axis=alt.Axis(labels=False, values=[0],grid=False, ticks=True),
    ),
    column=alt.Column(
        'Auteur:N',
        header=alt.Header(
            titleOrient='bottom',
            labelOrient='bottom',
            labelPadding=0,
            labelFontWeight="bold",
            labelBaseline="bottom"
        ),
    )
).properties(
    width=200
).configure_facet(
    spacing=0
).configure_view(
    stroke=None
)

# --- cell 13 (code) ---


# --- cell 14 (code) ---

