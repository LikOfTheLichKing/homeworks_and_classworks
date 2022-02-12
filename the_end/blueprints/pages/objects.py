from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from crud.survey import SurveyCrud
from core.db import get_connection


objects_blueprint = Blueprint("objects_blueprint", __name__, url_prefix="/objects")


@objects_blueprint.route("survey/<id>", methods=["GET"])
def get_survey_info(id):
    with get_connection() as connection:
        return jsonify(SurveyCrud.get_survey(connection, id)) 


@objects_blueprint.route("survey/<id>", methods=["DELETE"])
def vote(id):
    auth = request.authorization
    if auth is None:
        raise HTTPException("Auth headers not provided")

    with get_connection() as connection:
        SurveyCrud.delete_survey(connection, id, auth)
    return jsonify({"info": "OK", "status_code": 200})