from flask import Blueprint, render_template

login_blueprint = Blueprint("login_blueprint", __name__)


@login_blueprint.route("/login")
def get_login_page():
    return render_template("login.html")
