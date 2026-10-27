# Contest Board Workshop

A small **Flask + plain HTML/CSS/JavaScript** programming-contest dashboard for students. It reads **sample, pre-judged submissions** from `data/submissions.json`. It never accepts or judges code, and is **not a production contest platform**.

## Run in PyCharm

Open this folder as a project, set a Python 3.10+ interpreter, and run:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. Click **Start contest** to begin a shared two-hour clock. Refreshing the page keeps the original start time, saved in `contest_state.json` (ignored by Git). To restart the demo, stop the app and delete that file. Run in a trusted local environment: the start button has no login.

## ICPC scoring

- Rank by **problems solved**, then **lowest penalty**, then team name.
- For each solved problem, count the first Accepted minute plus **20 minutes for each earlier rejected submission**, excluding Compilation Error.
- Unsolved problems contribute no penalty. Later Accepted results do not count.
- The contest ends at minute 120. Submissions after that are ignored.
- The shared timer counts down every second; results and standings refresh every two seconds.

**Worked example:** Byte Benders solve A at minute 18 after one Wrong Answer and a Compilation Error: `18 + 20 = 38`. They solve B at minute 52 after one Wrong Answer: `52 + 20 = 72`. They solve C at minute 91 on the first try: `91`. Total: **3 solved and 201 penalty**. Pixel Pioneers also solve 3 with `24 + 44 + (83 + 20) = 171` penalty, so Pixel Pioneers rank ahead.

## Test

```bash
python -m pytest -q
```

Scoring is independent of Flask in `scoring.py`. Integration tests use Flask's built-in test client. This is a workshop demo, not a live programming judge.
