import pytest
from flask.app import Flask
from flask.testing import FlaskClient

from app.db import get_db
from tests.conftest import AuthActions


def test_index_works(client: FlaskClient, auth: AuthActions):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Sign Up" in response.data

    auth.login()
    response = client.get("/")
    assert b"Log Out" in response.data
    assert b"test title" in response.data
    assert b"by test on 2018-01-01" in response.data
    assert b"test\nbody" in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
        "/1/delete",
    ),
)
def test_unauthenticated_requests_redirect(client: FlaskClient, path: str):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_unable_to_edit_other_user_posts(
    app: Flask, client: FlaskClient, auth: AuthActions
):
    # Switch the post author to another user
    with app.app_context():
        db = get_db()
        db.execute("update posts set author_id = 2 where id = 1")
        db.commit()

    auth.login()

    # Current user cannot modify another user's post
    assert client.post("/1/update").status_code == 403
    assert client.post("/1/delete").status_code == 403

    # The current user should not have the update post URL available to them
    assert b'href="/1/update"' not in client.get("/").data


@pytest.mark.parametrize(
    "path",
    (
        "/2/update",
        "/2/delete",
    ),
)
def test_user_cannot_edit_nonexistant_posts(
    client: FlaskClient, auth: AuthActions, path: str
):
    auth.login()
    assert client.post(path).status_code == 404


def test_created_post_adds_one_record(
    client: FlaskClient, auth: AuthActions, app: Flask
):
    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "created", "body": ""})

    with app.app_context():
        db = get_db()
        count = db.execute("select count(id) from posts").fetchone()[0]
        assert count == 2


def test_user_can_update_post(client: FlaskClient, auth: AuthActions, app: Flask):
    auth.login()
    assert client.get("/1/update").status_code == 200
    client.post("/1/update", data={"title": "updated", "body": ""})

    with app.app_context():
        db = get_db()
        post = db.execute("select * from posts where id = 1").fetchone()
        assert post["title"] == "updated"


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
    ),
)
def test_invalid_post_update_or_create_fails(
    client: FlaskClient, auth: AuthActions, path: str
):
    auth.login()
    response = client.post(path, data={"title": "", "body": ""})
    assert b"Title is required." in response.data


def test_delete_post_succeeds(client: FlaskClient, auth: AuthActions, app: Flask):
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        post = db.execute("select * from posts where id = 1").fetchone()
        assert post is None
