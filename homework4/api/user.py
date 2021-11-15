from flask import Blueprint, request, jsonify
from pydantic import BaseModel
import pydantic
from typing import Optional

user_blueprint = Blueprint(
    name="user_blueprint", import_name=__name__, url_prefix="/api"
)


class NewUserModel(BaseModel):
    login: str
    password: str
    items: Optional[list]


@user_blueprint.route("/", methods=["POST"])
def post11():
    try:
        data = NewUserModel(**request.get_json(force=True))
        return "all done", 200
    except pydantic.error_wrappers.ValidationError:
        return jsonify({"info": "Invalid data format"}, 500)


@user_blueprint.route("/")
def get():
    return "you get this str"
