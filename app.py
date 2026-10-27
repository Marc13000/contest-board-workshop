"""Small Flask app for a pre-judged contest workshop."""

import json
from pathlib import Path

from flask import Flask, render_template

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)


def load_contest():
    """Load deterministic sample data; no judge or database required."""
    return json.loads((BASE_DIR / "data" / "submissions.json").read_text(encoding="utf-8"))


@app.get("/")
def home():
    contest = load_contest()
    teams = {team["id"]: team["name"] for team in contest["teams"]}
    submissions = sorted(contest["submissions"], key=lambda row: row["minute"])
    for submission in submissions:
        submission["team_name"] = teams[submission["team_id"]]
    return render_template("index.html", contest=contest, submissions=submissions)


if __name__ == "__main__":
    app.run(debug=True)
