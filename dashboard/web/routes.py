from flask import (
    render_template,
)

from web import app
from web.utils.altair_plot import plot_recent_match_notes
from web.utils.altair_plot import plot_recent_player_notes
from web.utils.altair_plot import plot_recent_player_matchs
from web.utils.altair_plot import plot_all_player_notes
from web.utils.altair_plot import plot_all_players_means


@app.route("/")
@app.route("/recent")
def build_recent():
    # ploting
    recent_match_notes = plot_recent_match_notes(app.static_url_path)
    recent_player_notes = plot_recent_player_notes(app.static_url_path)
    recent_player_matchs = plot_recent_player_matchs(app.static_url_path)
    all_player_notes = plot_all_player_notes(app.static_url_path)
    all_player_means = plot_all_players_means(app.static_url_path)

    context = {
        "plot_recent_match_notes": recent_match_notes,
        "plot_recent_player_notes": recent_player_notes,
        "plot_recent_player_matchs": recent_player_matchs,
        "plot_all_player_notes": all_player_notes,
        "plot_all_player_means": all_player_means
    }

    return render_template("recent.html", context=context)
