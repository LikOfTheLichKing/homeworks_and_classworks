from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from models.user import RegistrationModel
from crud.user import UserCRUD as user_crud
from core.db import get_connection

user_blueprint = Blueprint("user_blueprint", __name__, url_prefix="/users")


@user_blueprint.route("", methods=["POST"])
def register():
    if request.json is None:
        raise HTTPException("Json not found")

    data = RegistrationModel(**request.json)

    with get_connection() as conn:
        user_crud.create(conn, data)

    return jsonify({"info": "OK"})


@user_blueprint.route("", methods=["GET"])
def get_user_data():
    auth_data = request.authorization
    if auth_data is None:
        raise HTTPException("Auth headers not provided")

    with get_connection() as conn:
        user_crud.authenticate(conn, auth_data)
        user_data = user_crud.get(conn, auth_data.username)

    return jsonify(user_data.dict())


@user_blueprint.route("", methods=["DELETE"])
def delete_user():
    auth_data = request.authorization
    if auth_data is None:
        raise HTTPException("Auth Headers No Provided")
    with get_connection() as conn:
        user_crud.delete(conn, auth_data)
    return jsonify({"info": "User Deleted", "code": 200})


@user_blueprint.route("/follows", methods=["GET"])
def get_follows():
    auth_data = request.authorization
    if auth_data is None:
        raise HTTPException("Auth headers not provided")

    with get_connection() as conn:
        if auth_data is None:
            raise HTTPException("Auth Headers No Provided")
        user_crud.authenticate(conn, auth_data)
        user_id = user_crud.get(conn, auth_data.username).id
        user_data = user_crud.get_follows_list(conn, user_id)
    if user_data is None:
        return jsonify({"info": "no follows now. Follow another users and return to this page!"})
    return jsonify(user_data)
