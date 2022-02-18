from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from crud.survey import SurveyCrud
from core.db import get_connection
from crud.user import UserCRUD

objects_blueprint = Blueprint(
    "objects_blueprint", __name__, url_prefix="/objects"
    )


@objects_blueprint.route("polls/<id>", methods=["GET"])
def get_survey_info(id):
    with get_connection() as connection:
        return jsonify(SurveyCrud.get_survey(connection, id))


@objects_blueprint.route("polls/<id>", methods=["DELETE"])
def vote(id):
    auth = request.authorization
    if auth is None:
        raise HTTPException("Auth headers not provided")

    with get_connection() as connection:
        SurveyCrud.delete_survey(connection, id, auth)
    return jsonify({"info": "OK", "status_code": 200})


@objects_blueprint.route("/users/<followed_id>", methods=["POST"])
def follow(followed_id):
    auth = request.authorization
    if auth is None:
        raise HTTPException("Auth headers not provided")
    with get_connection() as connection:
        user_id = UserCRUD.get(connection, auth.username).id
        UserCRUD.follow(connection, user_id, followed_id)
    return jsonify({"info": "OK", "status_code": 200})


@objects_blueprint.route("/users/<username>", methods=["GET"])
def get_user(username):
    with get_connection() as conn:
        user_data = UserCRUD.get(conn, username)
    return jsonify(user_data.dict())
