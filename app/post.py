from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint("post", __name__)


@bp.route("/")
def index():
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
    return render_template("post/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Allow authenticated users to create new posts."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "insert into posts (title, body, author_id) values (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()

            return redirect(url_for("post.index"))

    return render_template("post/create.html")


def get_post(post_id, check_author=True):
    """Get data for a specified post."""
    post = (
        get_db()
        .execute(
            """
        select p.id
             , p.title
             , p.body
             , p.created
             , p.author_id
             , u.username
          from posts p
               join users u
                 on u.id = p.author_id
         where p.id = ?
        """,
            (post_id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/<int:post_id>/update", methods=("GET", "POST"))
@login_required
def update(post_id):
    """Allow authenticated users to update an existing post."""
    post = get_post(post_id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                """
                update posts
                   set title = ?
                     , body = ?
                 where id = ?
                 """,
                (title, body, post_id),
            )
            db.commit()
            return redirect(url_for("post.index"))

    return render_template("post/update.html", post=post)


@bp.route("/<int:post_id>/delete", methods=("POST",))
@login_required
def delete(post_id):
    """Allow authenticated users to delete a post"""
    get_post(post_id)
    db = get_db()
    db.execute("delete from posts where id = ?", (post_id,))
    db.commit()
    return redirect(url_for("post.index"))
