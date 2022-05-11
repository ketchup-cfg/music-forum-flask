import pytest
from flask import g, session
from flask.app import Flask
from flask.testing import FlaskClient

from app.db import get_db
from tests.conftest import AuthActions


def test_register_valid_input(client: FlaskClient, app: Flask):
    assert client.get("/auth/register").status_code == 200
    response = client.post("/auth/register", data={"username": "a", "password": "a"})
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert (
            get_db()
            .execute(
                "select * from users where username = 'a'",
            )
            .fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("a", "", b"Password is required."),
        ("test", "test", b"already registered"),
    ),
)
def test_register_invalid_input(
    client: FlaskClient, username: str, password: str, message: str
):
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in response.data


def test_login_valid_input(client: FlaskClient, auth: AuthActions):
    assert client.get("/auth/login").status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "test", b"Incorrect username."),
        ("test", "a", b"Incorrect password."),
    ),
)
def test_login_invalid_input(
    auth: AuthActions, username: str, password: str, message: str
):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client: FlaskClient, auth: AuthActions):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
