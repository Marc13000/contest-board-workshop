"""Flask test-client integration checks."""
from datetime import datetime,timedelta,timezone
import json
import pytest
pytest.importorskip("flask")
from app import app

@pytest.fixture
def client(tmp_path):
    app.config.update(TESTING=True,STATE_PATH=tmp_path/"contest_state.json")
    with app.test_client() as c:
        yield c

def test_home(client):
    response=client.get("/")
    assert response.status_code==200
    assert b"STUDENT WORKSHOP" in response.data

def test_start_persists_between_requests(client):
    first=client.post("/api/start").get_json()
    second=client.post("/api/start").get_json()
    refreshed=client.get("/api/contest").get_json()
    assert first["status"]=="running"
    assert first["started_at"]==second["started_at"]==refreshed["started_at"]
    assert len(refreshed["standings"])==5

def test_start_saved_in_file(client):
    client.post("/api/start")
    saved=json.loads(app.config["STATE_PATH"].read_text(encoding="utf-8"))
    assert datetime.fromisoformat(saved["started_at"]).tzinfo is not None

def test_deadline_freezes_feed(client):
    started=datetime.now(timezone.utc)-timedelta(minutes=125)
    app.config["STATE_PATH"].write_text(json.dumps({"started_at":started.isoformat()}))
    data=client.get("/api/contest").get_json()
    assert data["status"]=="finished"
    assert data["elapsed_seconds"]==7200
    assert len(data["submissions"])==21
    assert all(row["minute"]<=120 for row in data["submissions"])
