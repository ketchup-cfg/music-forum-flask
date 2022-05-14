import os
from typing import Any, Mapping

from flask import Flask

from app import db, errors
from app.blueprints import auth, posts, root


def create_app(test_config: Mapping[str, Any] = None) -> Flask:
    """Create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "hmm.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    # Set up a route that can be used for testing purposes
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # Setup error handlers
    app.register_error_handler(404, errors.page_not_found)

    # Setup routes
    app.register_blueprint(root.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(posts.bp)
    app.add_url_rule("/", endpoint="index")

    return app
