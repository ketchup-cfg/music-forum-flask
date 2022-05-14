from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import generate_password_hash
from werkzeug.wrappers.response import Response

from app.db import get_db
from app.exceptions import AuthenticationError
from app.users import authenticate_user

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register() -> Response | str:
    """Register a new user."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "insert into users (username, password) values (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()

            except db.IntegrityError:
                error = f"User {username} is already registered."

            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login() -> Response | str:
    """Authenticate an existing user."""
    if request.method == "POST":
        try:
            user_id = authenticate_user(
                request.form["username"], request.form["password"]
            )
            session.clear()
            session["user_id"] = user_id

            return redirect(url_for("index"))

        except AuthenticationError as ex:
            error_message = ex.args[0]
            flash(error_message)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user() -> None:
    """Get the ID of the currently authenticated user."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("select * from users where id = ?", (user_id,)).fetchone()
        )


@bp.route("/logout")
def logout() -> Response:
    """Log the user out for the current session."""
    session.clear()
    return redirect(url_for("index"))
