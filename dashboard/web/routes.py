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
        "plot_notes_match": notes_match,
        "plot_notes_player": notes_player,
        "plot_player_matchs": player_matchs
    }

    return render_template("recent.html", context=context)
