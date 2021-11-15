from flask import Blueprint
from items import api_items_blueprint
from user import user_blueprint

api_blueprint = Blueprint(
    name="api__init__blueprint", import_name=__name__, url_prefix="/api"
)

api_blueprint.register_blueprint(user_blueprint)
api_blueprint.register_blueprint(api_items_blueprint)


@api_blueprint.route("/empty")
def empty():
    return "empty"


@api_blueprint.route("/lich_king")
def frozen_throne():
    return "There must always be a Lich King"
