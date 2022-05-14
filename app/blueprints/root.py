from flask import Blueprint, render_template

from app.db import get_db

bp = Blueprint("root", __name__)


@bp.route("/")
def index() -> str:
    """Handle all requests sent to the root URL and return all existing posts."""
    db = get_db()
    posts = db.execute(
        """
        select p.id
             , p.title
             , p.body
             , p.created
             , p.author_id
             , u.username
          from posts p
               join users u
                 on p.author_id = u.id
        order by p.created desc
        """
    ).fetchall()
    return render_template("posts/index.html", posts=posts)
