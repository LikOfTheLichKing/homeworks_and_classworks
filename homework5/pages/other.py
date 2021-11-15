from flask import Blueprint, render_template

other_blueprint = Blueprint(name="other_blueprint", import_name=__name__)


@other_blueprint.route("/")
def six():
    return render_template("six.html")


@other_blueprint.route("/")
def five():
    return render_template("five.html")
