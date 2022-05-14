from werkzeug.security import check_password_hash

from app.db import get_db
from app.exceptions import AuthenticationError


def authenticate_user(username: str, password: str) -> int:
    """Check if the username and password are valid, and if they are, return the user's ID."""
    db = get_db()
    user = db.execute(
        "select password from users where username = ?", (username,)
    ).fetchone()

    if user is None:
        raise AuthenticationError("Incorrect username.")
    elif not check_password_hash(user["password"], password):
        raise AuthenticationError("Incorrect password.")

    return user["id"]
