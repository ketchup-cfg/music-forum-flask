import os
import tempfile

import pytest
from flask.app import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from werkzeug.test import TestResponse

from app import create_app
from app.db import get_db, init_db


def parse_sql_script() -> str:
    """Parse the test SQL script and return as a string."""
    sql_script: str

    with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
        sql_script = f.read().decode("utf8")

    return sql_script


@pytest.fixture
def app() -> Flask:
    """Provide a test application for running tests."""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": db_path,
        }
    )



    with app.app_context():
        init_db()
        get_db().executescript(parse_sql_script())

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def runner(app) -> FlaskCliRunner:
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client: FlaskClient):
        self._client = client

    def login(self, username="test", password="test") -> TestResponse:
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self) -> TestResponse:
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client) -> AuthActions:
    return AuthActions(client)
