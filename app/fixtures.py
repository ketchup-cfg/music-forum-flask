import functools
from typing import Any, Callable

from flask import g, redirect, url_for
from werkzeug.wrappers.response import Response


def login_required(view) -> Callable[[dict[str, Any]], Response | Any]:
    """A decorator to use for requiring that a user be authenticated when submitting a request."""

    @functools.wraps(view)
    def wrapped_view(**kwargs) -> Response | Any:
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
