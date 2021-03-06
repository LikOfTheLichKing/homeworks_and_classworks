from flask import Blueprint, jsonify, request
from crud import posts_crud
from core.db import get_connection
from blueprints import deps
from schemas.posts import BaseCreatePostModel

posts_blueprint = Blueprint("posts_blueprint", __name__, url_prefix="/posts")


@posts_blueprint.route("", methods=["POST"])
def create_post():
    current_user = deps.get_current_user()
    post_data = deps.get_input(BaseCreatePostModel)

    with get_connection() as conn:
        posts_crud.create(conn, post_data, current_user)

    return jsonify({"info": "OK"}), 201


@posts_blueprint.route("")
def get_posts():
    user = deps.get_current_user()

    with get_connection() as conn:
        posts = posts_crud.get_by_follower(conn, user)

    return jsonify([post.dict() for post in posts])


@posts_blueprint.route("", methods=["DELETE"])
def delete_post():
    id = request.get_json(force=True)["ID"]
    with get_connection() as conn:
        posts_crud.delete(conn, id)
    return jsonify({"info": "post has been deleted "}), 201
