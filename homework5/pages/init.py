from flask import Blueprint, render_template
from other import other_blueprint
from main import main_blueprint

pages_blueprint = Blueprint(name="pages_blueprint", import_name=__name__)

pages_blueprint.register_blueprint(other_blueprint)
pages_blueprint.register_blueprint(main_blueprint)


@pages_blueprint.route("/heh")
def heh():
    return render_template("heh.html")


@pages_blueprint.route("/kek")
def kek():
    return render_template("kek.html")
