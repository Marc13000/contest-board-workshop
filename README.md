# Contest Board Workshop

A beginner-friendly Flask app that shows **sample, pre-judged programming contest submissions**. It does not run or judge student code. Built for an issue-driven AI coding workshop and easy to open in PyCharm.

## Run

Use Python 3.10+; open this folder as a project in PyCharm, then open its terminal:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. All submissions are in `data/submissions.json`.

This is a **workshop demo**, not a live judge or production contest platform.
