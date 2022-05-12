import pytest
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "path",
    (
        "/what",
        "/this-url-does-not-exist",
        "/post/no",
        "/auth/no",
    ),
)
def test_404_returns_template(client: FlaskClient, path: str):
    response = client.get(path)
    assert b"unable to locate the page that you are looking for" in response.data
    assert b"Not Found" in response.data
