from flask import Blueprint, render_template

main_blueprint = Blueprint("main_blueprint", __name__)


@main_blueprint.route("/pumpkin")
def pumpkin():
    return render_template("pumpkin.html")


@main_blueprint.route("/no")
def not_pumpkin():
    return render_template("no_pumpkin.html")
