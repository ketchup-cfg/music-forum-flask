import sqlite3


import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask.app import Flask
from flask.testing import FlaskCliRunner

from app.db import get_db


def test_close_db_closes_get_db_connection(app: Flask):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command_inits_database(
    runner: FlaskCliRunner, monkeypatch: MonkeyPatch
):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("app.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
