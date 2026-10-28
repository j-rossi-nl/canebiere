# Source cells of generate_2021_2022.ipynb
# --- cell 0 (code) ---
import pickle

import altair as alt
import pandas as pd

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

# --- cell 5 (code) ---
matchs['Saison'] = matchs['Date'].apply(date_to_season)
notation['Saison'] = notation['Date'].apply(date_to_season)

matchs["Nb Buts"] = matchs["Buts_R"] + matchs["Buts_V"]

matchs["Victoire"] = matchs["Buts_OM"] > matchs["Buts_Adversaire"]
matchs["Défaite"] =  matchs["Buts_OM"] < matchs["Buts_Adversaire"]
matchs["Nul"] =  matchs["Buts_OM"] == matchs["Buts_Adversaire"]
matchs['Ecart'] = matchs['Buts_OM'] - matchs['Buts_Adversaire']

# --- cell 6 (code) ---
matchs_saison = matchs[matchs['Saison'] == '2021-2022']
notation_saison = notation[notation['Saison'] == '2021-2022']

# --- cell 7 (markdown) ---
# # Saison 2021-2022

# --- cell 8 (markdown) ---
# # Des matchs, des résultats

# --- cell 9 (code) ---
vnd = matchs_saison.groupby('Saison').agg({'Victoire': 'sum', 'Défaite': 'sum', 'Nul': 'sum'}).reset_index().melt(id_vars='Saison', value_vars=['Victoire', 'Nul', 'Défaite'])

alt.Chart(vnd).mark_bar().encode(
    x=alt.X(
        'value:Q', 
        title='',
    ),
    color=alt.Color(
        'variable', 
        title='Résultat', 
        scale=alt.Scale(
            domain=['Victoire', 'Nul', 'Défaite'], 
            range=['#54a24b', '#d8b5a5', '#e45756']
        )
    ),
    tooltip=[alt.Tooltip("Saison", title="Saison"), alt.Tooltip("variable", title='Résultat'), alt.Tooltip("value", title="Académies")],
    order=alt.Order(
        'variable',
        sort='descending'
    )
).properties(
    width=800
).configure_axisY(
    labelPadding=20, 
    labelFontSize=18,
    grid=False,
)

# --- cell 10 (markdown) ---
# # Des matchs, des buts

# --- cell 11 (code) ---
alt.Chart(matchs_saison[['Nb Buts']]).mark_bar().encode(
    x=alt.X("Nb Buts:O", axis=alt.Axis(labelAngle=0), title="Nombre de buts dans un match"),
    y=alt.Y("count():Q", title="Matchs"),
    color=alt.Color("Nb Buts:O", scale=alt.Scale(scheme="greens")),
    tooltip=["Nb Buts:O", alt.Tooltip("count():Q", title="Nb Matches")]
).properties(
    width=DEFAULT_WIDTH
)

# --- cell 12 (code) ---
alt.Chart(matchs_saison[["Buts_OM"]]).mark_bar().encode(
    x=alt.X("Buts_OM:O", title="Buts de l'OM", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("count():Q", title='Matchs'),
    color=alt.Color("Buts_OM:O", scale=alt.Scale(scheme='blues'), title='Buts de l\'OM'),
    tooltip=[alt.Tooltip("Buts_OM:O", title="Buts de l'OM"), alt.Tooltip("count():Q", title="Nb Matches")]
).properties(
    width=DEFAULT_WIDTH
)

# --- cell 13 (code) ---
alt.Chart(matchs_saison[["Buts_Adversaire"]]).mark_bar().encode(
    x=alt.X("Buts_Adversaire:O", title="Buts de l'adversaire", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("count():Q", title="Matchs"),
    color=alt.Color("Buts_Adversaire:O", scale=alt.Scale(scheme="reds"), title='But de l\'Adversaire'),
    tooltip=[alt.Tooltip("Buts_Adversaire:O", title="Buts de l'Adversaire"), alt.Tooltip("count():Q", title="Nb Matches")]
).properties(
    width=DEFAULT_WIDTH
)

# --- cell 14 (code) ---
alt.Chart(matchs_saison[["Ecart"]]).mark_bar().encode(
    x=alt.X("Ecart:O", title="Écart au score", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("count():Q", title="Matchs"),
    color=alt.Color("Ecart:O", scale=alt.Scale(scheme="redyellowgreen"), title='Écart'),
    tooltip=[alt.Tooltip("Ecart:O", title="Écart au score"), alt.Tooltip("count():Q", title="Nb Matches")]
).properties(
    width=DEFAULT_WIDTH
)

# --- cell 15 (markdown) ---
# # Des notes

# --- cell 16 (code) ---
overall = notation_saison.groupby(['Note_num', 'Note_txt']).agg({"Joueur": "count", "sort": "max"}).reset_index()

alt.Chart(overall).mark_circle().encode(
    x=alt.X(
        'Note_num:Q',
        title='Note',
        axis=None
    ),
    y=alt.datum("Toutes les notes"),
    color=alt.Color(
        'Note_num:Q', 
        legend=None, 
        scale=alt.Scale(domain=[0.0,5.0], scheme="redyellowgreen")
    ),
    size=alt.Size(
        "Joueur:Q",
        legend=None,
        scale=alt.Scale(domain=[0.0, overall["Joueur"].max()], range=[0.0, 4000.0])
    ),
    tooltip=[alt.Tooltip("Note_txt:N", title="Note"), alt.Tooltip("Joueur:N", title="# Attributions")]
).properties(
    title='2021-2022',
    width=800
).configure_axis(
    grid=False
).configure_view(
    strokeWidth=0,
).configure_axisY(
    labelPadding=20, 
    labelFontSize=18,
    grid=False,
)

# --- cell 17 (code) ---
by_joueur = notation_saison.groupby("Joueur").agg({"Note_num": ["count", "mean"]})
by_joueur.columns = by_joueur.columns.droplevel()
by_joueur.reset_index(inplace=True)

alt.Chart(by_joueur).mark_bar().encode(
    x=alt.X("count:Q", title="Nombre de Notes"),
    y=alt.Y(
        field="Joueur", 
        type="ordinal", 
        sort="-x",
        axis=alt.Axis(labelFontSize=14)
    ),
    color=alt.Color("count:Q", title="Nombre de Notes", scale=alt.Scale(scheme="blues")),
    tooltip=["Joueur", alt.Tooltip("count:Q", title="# Notes")]
).configure_header(
    titleColor='green',
    titleFontSize=14,
    labelColor='red',
    labelFontSize=14
).configure_view(
    width=800
)

# --- cell 18 (markdown) ---
# # Des notes, des moyennes

# --- cell 19 (code) ---
alt.Chart(notation_saison).mark_bar().transform_aggregate(
    count="count(Note_num)",
    moyenne="mean(Note_num)",
    groupby=["Joueur"]
).encode(
    x=alt.X("moyenne:Q", title="Moyenne"),
    y=alt.Y(
        field="Joueur", 
        type="ordinal", 
        sort="-x",
        axis=alt.Axis(labelFontSize=14)
    ),
    color=alt.Color("moyenne:Q", title="Moyenne", scale=alt.Scale(scheme="redyellowgreen", domain=[1.0, 3.5])),
    tooltip=["Joueur", alt.Tooltip("count:Q", title="# Notes"), alt.Tooltip("moyenne:Q", title="Moyenne", format='.2f')]
).configure_header(
    titleColor='green',
    titleFontSize=14,
    labelColor='red',
    labelFontSize=14
).configure_view(
    width=800
)

# --- cell 20 (markdown) ---
# # Des joueurs, des notes

# --- cell 21 (code) ---
by_match_by_note = notation_saison.groupby(["Saison", "Match", "Match_Teams", "Note_num", "Note_txt"]).agg({"Joueur": "count", "sort": "max"}).reset_index()
fuse = notation_saison.set_index('Date').join(matchs_saison.set_index('Date'), how='inner', lsuffix='_notes', rsuffix='_matchs')

# --- cell 22 (code) ---
step = 30
overlap = 0.5

alt.Chart(fuse[['Joueur', 'Note_num']], height=step, width=800).transform_joinaggregate(
    mean_note='mean(Note_num)', groupby=['Joueur']
).transform_bin(
    ['bin_max', 'bin_min'], 'Note_num'
).transform_aggregate(
    value='count()', groupby=['Joueur', 'mean_note', 'bin_min', 'bin_max']
).transform_impute(
    impute='value', groupby=['Joueur', 'mean_note'], key='bin_min', value=0
).mark_area(
    interpolate='monotone',
    fillOpacity=0.8,
    stroke='lightgray',
    strokeWidth=0.5
).encode(
    x=alt.X('bin_min:Q', bin='binned', title='Note / 5'),
    y=alt.Y(
        'value:Q',
        scale=alt.Scale(range=[step, -step * overlap]),
        axis=None
    ),
    fill=alt.Fill(
        'mean_note:Q',
        legend=alt.Legend(title='Moyenne'),
        scale=alt.Scale(domain=[1.0, 3.5], scheme='redyellowgreen')
    ),
    tooltip=['Joueur:N', alt.Tooltip('mean_note:Q', title='Moyenne', format='.1f')]
).facet(
    row=alt.Row(
        'Joueur:N',
        title=None,
        header=alt.Header(labelAngle=0, labelAlign='left', labelFontSize=14, labelBaseline='top'),
    )
).properties(
    title='OM 2021-2022',
    bounds='flush',
).configure_facet(
    spacing=0,
).configure_view(
    stroke=None
).configure_title(
    anchor='end'
)

# --- cell 23 (markdown) ---
# # Des matchs, des notes

# --- cell 24 (code) ---
base_circles = alt.Chart(by_match_by_note).mark_circle().encode(
    x=alt.X(
        'Note_num:Q',
        title='Note',
        axis=alt.Axis(grid=False, ticks=False, labels=False, domain=False)
    ),
    y=alt.Y(
        'Match_Teams:N',
        title=None,
        axis=alt.Axis(ticks=False, grid=False, labelPadding=180, labelFontSize=14, labelAlign='left', domain=False),
        sort=alt.EncodingSortField("sort", op="max", order="ascending")
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
    tooltip=[alt.Tooltip("Match_Teams:N", title="Match"), alt.Tooltip("Note_txt:N", title="Note"), alt.Tooltip("Joueur:N", title="# Joueurs")]
).properties(
    title='2021-2022',
    width=800
)

dots = alt.Chart(fuse).mark_circle(size=200).encode(
    y=alt.Y(
        'Match_Teams:N',
        axis=alt.Axis(ticks=False, labels=False, title="", domain=False), 
        sort=alt.EncodingSortField("sort", op="max", order="ascending")
    ),
    color=alt.Color('Résultat', legend=None, scale=alt.Scale(domain=['Victoire', 'Nul', 'Défaite'], range=['#54a24b', '#d8b5a5', '#e45756'])),
    tooltip=[alt.Tooltip('Match_Teams:N', title="Match"), 'Résultat:N']
)

line = alt.Chart(fuse).mark_line().encode(
    y=alt.Y('Match_Teams:N', sort=alt.EncodingSortField("sort", op="max", order="ascending")),
)


# --- cell 25 (code) ---
(line + dots | base_circles).configure_view(strokeWidth=0)

# --- cell 26 (code) ---
# from sklearn.ensemble import HistGradientBoostingClassifier
# from sklearn.metrics import classification_report
# from sklearn.metrics import ConfusionMatrixDisplay
# from sklearn.inspection import permutation_importance

# pivot = fuse[['Joueur', 'Note_num']].pivot(columns='Joueur', values='Note_num')
# pivot['Resultat'] = matchs_saison.set_index('Date')['Résultat']

# X = pivot[[x for x in pivot.columns if x != 'Resultat']]
# y = pivot['Resultat']

# clf: HistGradientBoostingClassifier = HistGradientBoostingClassifier()
# _ = clf.fit(X, y)

# print(classification_report(y_true=y, y_pred=clf.predict(X)))

# _ = ConfusionMatrixDisplay.from_estimator(clf, X, y, normalize='pred', values_format='.2f', cmap='Blues')


# result = permutation_importance(
#     clf, X, y, n_repeats=10, random_state=42, n_jobs=2
# )

# sorted_importances_idx = result.importances_mean.argsort()[::-1]
# importances = pd.DataFrame(
#     result.importances[sorted_importances_idx].T,
#     columns=X.columns[sorted_importances_idx],
# )

# _ = alt.Chart(importances.melt()).mark_boxplot().encode(
#     x='value',
#     y=alt.X('Joueur', sort=alt.EncodingSortField('mean(value)'), axis=alt.Axis(labelFontSize=14)),
#     color=alt.Color('mean(value)', scale=alt.Scale(domain=[0, 0.16], scheme='redyellowgreen'))
# )

# --- cell 27 (code) ---

