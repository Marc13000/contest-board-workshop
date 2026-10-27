from datetime import datetime,timedelta,timezone
from clock import elapsed_seconds,read_start,start_once

def test_start_persists(tmp_path):
    path=tmp_path/"state.json"
    now=datetime(2026,10,27,9,tzinfo=timezone.utc)
    assert read_start(path) is None
    assert start_once(path,now)==read_start(path)==now

def test_repeated_start_does_not_reset(tmp_path):
    path=tmp_path/"state.json"
    now=datetime(2026,10,27,9,tzinfo=timezone.utc)
    start_once(path,now)
    assert start_once(path,now+timedelta(minutes=30))==now

def test_timer_stops_at_deadline():
    now=datetime(2026,10,27,9,tzinfo=timezone.utc)
    assert elapsed_seconds(now,now-timedelta(seconds=5))==0
    assert elapsed_seconds(now,now+timedelta(hours=2))==7200
    assert elapsed_seconds(now,now+timedelta(hours=4))==7200
