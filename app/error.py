from flask import render_template


def page_not_found(e):
    """Handle any 404 errors by returning a 404 error page."""
    return render_template("error/404.html"), 404

