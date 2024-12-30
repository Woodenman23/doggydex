from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    redirect,
    url_for,
    jsonify,
)
from flask_login import logout_user, current_user

from website import db

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html.j2")


@views.route("/session_data")
def session_data():
    return jsonify(dict(session))


@views.route("/profile", methods=["POST", "GET"])
def profile():
    pass


# @views.route("/logout")
# def logout():
#     session.pop("user", None)
#     session.pop("email", None)
#     session.pop("user_id", None)
#     logout_user()
#     return redirect(url_for("views.home"))
