import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """Get an existing database session or create a new one."""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Close an existing database session, if one exists."""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Initialize the application database."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Set up a cli command to allow for users to be able to clear and initialize the application database."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Initialize the application."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
