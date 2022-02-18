from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from models.survey import CreationSurveyModel
from crud.survey import SurveyCrud
from core.db import get_connection

survey_blueprint = Blueprint("survey_blueprint", __name__, url_prefix="/polls")


@survey_blueprint.route("/list", methods=["GET"])
def get_polls_list():
    with get_connection() as connection:
        polls_list = SurveyCrud.get_polls_list(conn=connection)

    return jsonify(polls_list)


@survey_blueprint.route("", methods=["POST"])
def create_survey():
    if request.json is None:
        raise HTTPException("Json not found")

    survey_data = CreationSurveyModel(**request.json)
    auth_data = request.authorization
    print(auth_data)
    if auth_data is None:
        raise HTTPException("Auth headers not provided")
    with get_connection() as connection:
        SurveyCrud.create(connection, survey_data, auth_data)

    return jsonify({"Info": "OK"}, 200)


@survey_blueprint.route("", methods=["PUT"])
def register_user_response():
    if request.json["answer_id"] is None:
        raise HTTPException("Json not found")

    auth_data = request.authorization
    if auth_data is None:
        raise HTTPException("Auth headers not provided")
    with get_connection() as connection:
        SurveyCrud.add_user_answer(
            connection, request.json["answer_id"], auth_data
        )

    return jsonify({"Info": "OK"}, 200)


@survey_blueprint.route("/list/by_creator/<id>", methods=["GET"])
def get_polls_by_creator(id):
    with get_connection() as conn:
        polls_list = SurveyCrud.get_polls_by_user(SurveyCrud, conn, id)
    return jsonify(polls_list)


@survey_blueprint.route("/list/by_followed", methods=["GET"])
def get_polls_by_follows():
    auth_data = request.authorization
    if auth_data is None:
        raise HTTPException("Auth headers not provided")
    with get_connection() as conn:
        return jsonify(
            SurveyCrud.get_polls_by_followed(SurveyCrud, conn, auth_data)
            )
