from typing import Type
from pathlib import Path

import flask
from flask import Flask, render_template, abort, request, jsonify

from homeworks_and_classworks.homework3.crud.Crud import UserCRUD

app: Flask = Flask(__name__)
user: Type[UserCRUD] = UserCRUD(Path(Path.cwd(), "data", "data.json"))


@app.route("/")
def home():
    return render_template("main.html")


@app.route(rule="/", methods=["POST"])
def register():
    try:
        new_user_data = request.get_json(force=True)
        nick = "".join(new_user_data.keys()[0])
        user.add_new(data=new_user_data[nick], login=new_user_data[nick]["login"])
        return "", 204
    except ValueError:
        return "", 204


@app.route(rule="/", methods=["PATCH"])
def change_password() -> tuple[str, int]:
    user_data = request.get_json(force=True)
    nick = "".join(user_data.keys())
    user.change_password(
        login=nick,
        password=user_data[nick]["password"],
        new_password=user_data[nick]["new_password"],
    )
    return "", 204


@app.route(rule="/", methods=["TRACE"])
def get_names():
    return jsonify(user.get_users_names())


@app.route(rule="/", methods=["DELETE"])
def delete_user() -> None:
    data = request.get_json(force=True)
    nick = "".join(data.keys())
    if user.check_info_on_data(login=nick, password=data["password"]):
        user.delete_item(nick)
    return "", 204


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
