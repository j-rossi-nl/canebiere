from flask import (
    render_template,
)

from web import app
from web.utils.altair_plot import plot_match_notes
from web.utils.altair_plot import plot_player_notes
from web.utils.altair_plot import plot_player_matchs


@app.route("/")
@app.route("/recent")
def build_recent():
    # ploting
    notes_match = plot_match_notes(app.static_url_path)
    notes_player = plot_player_notes(app.static_url_path)
    player_matchs = plot_player_matchs(app.static_url_path)

    context = {
        "total_all_confirmed": 10,
        "total_all_recovered": 10,
        "total_all_deaths": 10,
        "plot_notes_match": notes_match,
        "plot_notes_player": notes_player,
        "plot_player_matchs": player_matchs
    }

    return render_template("recent.html", context=context)


@app.route("/history")
def build_history():
    # total confirmed cases globally
    total_all_confirmed = total_confirmed[total_confirmed.columns[-1]].sum()
    total_all_recovered = total_recovered[total_recovered.columns[-1]].sum()
    total_all_deaths = total_death[total_death.columns[-1]].sum()

    # ploting
    plot_global_cases_per_country = altair_plot.altair_global_cases_per_country(
        final_df
    )
    context = {
        "total_all_confirmed": total_all_confirmed,
        "total_all_recovered": total_all_recovered,
        "total_all_deaths": total_all_deaths,
        "plot_global_cases_per_country": plot_global_cases_per_country,
    }
    return render_template("history.html", context=context)
