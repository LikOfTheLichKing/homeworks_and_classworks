from blueprints.pages.objects import objects_blueprint
from flask import Blueprint, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

pages_blueprint = Blueprint("pages_blueprint", __name__)
pages_blueprint.register_blueprint(objects_blueprint)


@pages_blueprint.errorhandler(ValidationError)
def register_validation_error(error: ValidationError):
    return jsonify(
        {"error": type(error).__name__, "info": error.errors()}
    ), 422


@pages_blueprint.errorhandler(ValueError)
def register_value_error(error: ValueError):
    return jsonify(
        {"error": type(error).__name__}
    ), 400


@pages_blueprint.errorhandler(HTTPException)
def validation_error(error: HTTPException):
    return (
        jsonify({"error": type(error).__name__, "info": error.description}),
        error.code,
    )
