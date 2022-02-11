from flask import Blueprint, jsonify
from blueprints.api.user import user_blueprint
from blueprints.api.survey import survey_blueprint
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

api_blueprint = Blueprint("api_blueprint", __name__)
api_blueprint.register_blueprint(user_blueprint)
api_blueprint.register_blueprint(survey_blueprint)


@api_blueprint.errorhandler(ValidationError)
def register_validation_error(error: ValidationError):
    return jsonify(
        {"error": type(error).__name__, "info": error.errors()}
    ), 422


@api_blueprint.errorhandler(ValueError)
def register_value_error(error: ValueError):
    return jsonify(
        {"error": type(error).__name__, "info": error.errors()}
    ), 400

@api_blueprint.errorhandler(HTTPException)
def validation_error(error: HTTPException):
    return (
        jsonify({"error": type(error).__name__, "info": error.description}),
        error.code,
    )
