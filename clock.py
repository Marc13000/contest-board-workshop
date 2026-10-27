"""Persistent two-hour clock for a single-process local workshop."""
import json
from datetime import datetime
from pathlib import Path
from threading import Lock

_start_lock = Lock()

def read_start(path):
    path = Path(path)
    if not path.exists():
        return None
    return datetime.fromisoformat(json.loads(path.read_text(encoding="utf-8"))["started_at"])

def start_once(path, now):
    """Save the start time on first click only; never reset the contest."""
    path = Path(path)
    with _start_lock:
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"started_at": now.isoformat()}), encoding="utf-8")
    return read_start(path)

def elapsed_seconds(start, now, duration_seconds=7200):
    """Clamp time before start to zero and time after deadline to duration."""
    if start is None:
        return 0
    return min(max((now - start).total_seconds(), 0), duration_seconds)
