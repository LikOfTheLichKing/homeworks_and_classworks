from flask import Blueprint
from .login import login_blueprint

pages_blueprint = Blueprint("pages_blueprint", __name__)
pages_blueprint.register_blueprint(login_blueprint)
