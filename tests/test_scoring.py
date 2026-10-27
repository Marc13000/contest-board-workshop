"""ICPC scoring regression tests."""
import json
from pathlib import Path
from scoring import standings

def contest(submissions):
    return {"teams":[{"id":"a","name":"Alpha"},{"id":"b","name":"Bravo"}],
            "problems":[{"id":"A","name":"Warm-up"},{"id":"B","name":"Graphs"}],
            "submissions":submissions}

def s(team, problem, minute, verdict):
    return {"team_id":team,"problem_id":problem,"minute":minute,"verdict":verdict}

def test_ties_rank_by_penalty_then_name():
    rows = standings(contest([s("a","A",45,"Accepted"),s("b","A",25,"Accepted")]),120)
    assert [r["team_id"] for r in rows] == ["b","a"]
    tied = standings(contest([s("a","A",25,"Accepted"),s("b","A",25,"Accepted")]),120)
    assert [r["team_id"] for r in tied] == ["a","b"]

def test_unsolved_problem_no_penalty():
    rows = standings(contest([s("a","A",15,"Wrong Answer"),s("a","A",25,"Time Limit Exceeded")]),120)
    alpha = next(r for r in rows if r["team_id"]=="a")
    assert (alpha["solved"],alpha["penalty"],alpha["problems"]["A"]["wrong_before_solve"]) == (0,0,2)

def test_only_first_accepted_counts():
    rows = standings(contest([s("a","A",65,"Wrong Answer"),s("a","A",30,"Accepted"),s("a","A",55,"Accepted"),s("a","A",40,"Wrong Answer")]),120)
    alpha = next(r for r in rows if r["team_id"]=="a")
    assert (alpha["solved"],alpha["penalty"]) == (1,30)

def test_compilation_errors_excluded():
    rows = standings(contest([s("a","A",5,"Wrong Answer"),s("a","A",9,"Compilation Error"),s("a","A",18,"Accepted")]),120)
    alpha = next(r for r in rows if r["team_id"]=="a")
    assert (alpha["solved"],alpha["penalty"]) == (1,38)

def test_deadline():
    rows = standings(contest([s("a","A",120,"Accepted"),s("a","B",121,"Accepted"),s("b","A",121,"Accepted")]),160)
    assert (rows[0]["solved"],rows[0]["penalty"],rows[1]["solved"]) == (1,120,0)

def test_results_revealed_by_clock():
    c=contest([s("a","A",8,"Wrong Answer"),s("a","A",18,"Accepted")])
    alpha=lambda t: next(r for r in standings(c,t) if r["team_id"]=="a")
    assert alpha(17.99)["solved"]==0
    assert (alpha(18)["solved"],alpha(18)["penalty"]) == (1,38)

def test_no_precontest_scoring():
    assert all(r["solved"]==0 for r in standings(contest([s("a","A",10,"Accepted")]),-20))

def test_worked_fixture():
    c=json.loads((Path(__file__).resolve().parents[1]/"data"/"submissions.json").read_text(encoding="utf-8"))
    rows=standings(c,120)
    assert (rows[0]["team_name"],rows[0]["solved"],rows[0]["penalty"]) == ("Pixel Pioneers",3,171)
    assert (next(r for r in rows if r["team_name"]=="Byte Benders")["penalty"]) == 201
