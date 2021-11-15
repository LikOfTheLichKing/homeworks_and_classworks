from flask import Blueprint

api_items_blueprint = Blueprint(
    name="api_user_blueprint", import_name=__name__, url_prefix="/api"
)


@api_items_blueprint.route("/no_ideas")
def no_idea():
    return " "


@api_items_blueprint.route("/heh")
def freeze():
    return "freeze"
