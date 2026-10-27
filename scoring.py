"""Plain-Python ICPC scoring for pre-judged workshop submissions."""
CONTEST_MINUTES = 120

def standings(contest, elapsed_minutes):
    """Rank by solves, then penalty. Use only results revealed by the clock."""
    cutoff = min(max(elapsed_minutes, 0), CONTEST_MINUTES)
    problem_ids = [p["id"] for p in contest["problems"]]
    rows = {
        t["id"]: {
            "team_id": t["id"], "team_name": t["name"], "solved": 0, "penalty": 0,
            "problems": {
                p: {"solved": False, "attempts": 0, "wrong_before_solve": 0, "accepted_minute": None}
                for p in problem_ids
            }
        }
        for t in contest["teams"]
    }
    # Chronological ordering makes first Accepted decisive.
    for submission in sorted(contest["submissions"], key=lambda s: s["minute"]):
        if submission["minute"] > cutoff:
            break
        problem = rows[submission["team_id"]]["problems"][submission["problem_id"]]
        if problem["solved"]:
            continue
        verdict = submission["verdict"]
        problem["attempts"] += 1
        if verdict == "Accepted":
            problem["solved"] = True
            problem["accepted_minute"] = submission["minute"]
            row = rows[submission["team_id"]]
            row["solved"] += 1
            row["penalty"] += submission["minute"] + 20 * problem["wrong_before_solve"]
        elif verdict != "Compilation Error":
            problem["wrong_before_solve"] += 1
    ranked = sorted(rows.values(), key=lambda r: (-r["solved"], r["penalty"], r["team_name"].casefold()))
    for rank, row in enumerate(ranked, 1):
        row["rank"] = rank
    return ranked
