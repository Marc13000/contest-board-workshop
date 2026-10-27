"""Local Flask workshop app with a persistent shared contest clock."""
import json
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template
from scoring import CONTEST_MINUTES, standings
from clock import read_start, start_once, elapsed_seconds

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
app.config["STATE_PATH"] = BASE_DIR / "contest_state.json"

def load_contest():
    return json.loads((BASE_DIR / "data" / "submissions.json").read_text(encoding="utf-8"))

def utc_now():
    return datetime.now(timezone.utc)

def contest_snapshot(now=None):
    """One server-side source of truth for the clock and standings."""
    now = now or utc_now()
    contest = load_contest()
    start = read_start(app.config["STATE_PATH"])
    seconds = elapsed_seconds(start, now, CONTEST_MINUTES * 60)
    visible_minutes = seconds / 60
    if start is None:
        visible_submissions = contest["submissions"]
        status = "ready"
    else:
        visible_submissions = [s for s in contest["submissions"] if s["minute"] <= visible_minutes]
        status = "finished" if seconds >= CONTEST_MINUTES * 60 else "running"

    teams = {t["id"]: t["name"] for t in contest["teams"]}
    submissions = [dict(s, team_name=teams[s["team_id"]])
                   for s in sorted(visible_submissions, key=lambda s: s["minute"], reverse=True)]
    return {
        "status": status, "started_at": start.isoformat() if start else None,
        "server_now": now.isoformat(), "duration_seconds": CONTEST_MINUTES * 60,
        "elapsed_seconds": seconds, "standings": standings(contest, visible_minutes),
        "submissions": submissions, "problems": contest["problems"],
    }

@app.get("/")
def home():
    return render_template("index.html", contest=load_contest())

@app.get("/api/contest")
def contest_api():
    return jsonify(contest_snapshot())

@app.post("/api/start")
def start_api():
    start_once(app.config["STATE_PATH"], utc_now())
    return jsonify(contest_snapshot())

if __name__ == "__main__":
    app.run(debug=True)
