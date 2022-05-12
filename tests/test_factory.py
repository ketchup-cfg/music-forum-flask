from flask.testing import FlaskClient

from app import create_app


def test_config_gets_loaded():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello_route_says_hi_back(client: FlaskClient):
    response = client.get("/hello")
    assert response.data == b"Hello, World!"
