import altair as alt


def plot_match_notes(static_url: str):
    graph = alt.Chart(static_url + '/notes.csv').mark_circle().transform_filter(
        alt.datum.match_rank <= 5
    ).transform_calculate(
        team_labels="split(datum.Match_Teams, ' ')"
    ).transform_aggregate(
        Note_num_count="count()",
        ranker="max(match_rank)",
        groupby=["Match_Teams", "Note_num"]
    ).encode(
        x=alt.X(
            'Match_Teams:N',
            title=None,
            axis=alt.Axis(ticks=False, grid=False, labelFontSize=16, labelAngle=0, orient='top', labelExpr="split(datum.label, ' ')"),
            sort=alt.EncodingSortField("ranker", order="ascending"),
        ),
        y=alt.Y(
            'Note_num:Q',
            title=None,
            axis=None, #alt.Axis(grid=False, tickMinStep=1.0, labelFontSize=16),
            scale=alt.Scale(domain=[0.0, 5.0])
        ),
        color=alt.Color(
            'Note_num:Q', 
            legend=None, 
            scale=alt.Scale(domain=[0.0,5.0], scheme="redyellowgreen")
        ),
        size=alt.Size(
            "Note_num_count:Q",
            legend=None,
            scale=alt.Scale(domain=[0.0, 5.0], range=[0.0, 5000.0])
        ),
        tooltip=["Match_Teams:N",  alt.Tooltip("Note_num:Q", title="Note"), alt.Tooltip("Note_num_count:N", title="# Joueurs")]
    ).properties(
            width="container",
            height="container",
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ) 

    return graph.to_json()


def plot_player_notes(static_url: str):
    graph = alt.Chart(static_url + '/notes.csv').mark_bar().transform_filter(
        alt.datum.match_rank <= 5
    ).encode(
        x=alt.X(
            'Joueur:N',
            title=None,
            axis=alt.Axis(labelFontSize=16, labelAngle=-45, orient='top'),
        ),
        y=alt.Y(
            'count(Note_num):Q', 
            title="",
            stack='normalize',
            axis=alt.Axis(labels=False, ticks=False)
        ),
        order=alt.Order("Note_num:Q", sort="ascending"),
        color=alt.Color('Note_num:Q', scale=alt.Scale(scheme="redyellowgreen", domain=[0.0, 5.0]), legend=None),
        tooltip=["Joueur:N", alt.Tooltip("Note_num:Q", title="Note"), alt.Tooltip("count(Note_num):Q", title="Nombre de fois")]
    ).properties(
            width="container",
            height="container",
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    )

    return graph.to_json()


def plot_player_matchs(static_url: str):
    graph = alt.Chart(static_url + '/notes.csv').mark_bar().transform_filter(
        alt.datum.match_rank <= 5
    ).transform_aggregate(
        num_apparitions='count()',
        groupby=['Joueur']
    ).encode(
        x=alt.X(
            'Joueur:N',
            title=None,
            axis=alt.Axis(labelFontSize=16, labelAngle=-45, orient='top'),
            sort=alt.EncodingSortField('num_apparitions', order='descending')
        ),
        y=alt.Y(
            'num_apparitions:Q', 
            title="",
            axis=alt.Axis(labels=False, ticks=False)
        ),
        color=alt.Color('num_apparitions:Q', scale=alt.Scale(scheme="redyellowgreen", domain=[0.0, 5.0]), legend=None),
        tooltip=["Joueur:N", alt.Tooltip("num_apparitions:Q", title="Nombre de Notes")]
    ).properties(
            width="container",
            height="container",
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    )

    return graph.to_json()
