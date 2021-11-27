from datetime import date
from flask import Flask
from flask import render_template
from typing import Optional
import json


app = Flask(__name__)

with open("data.json") as file:
    file_data: [date, list[tuple[str, str]]] = json.load(file)

all_keys = file_data.keys()


@app.route("/", methods=["GET"])
def get_list():
    global file_data
    return render_template("main.jinja", schedule=file_data)


def main() -> None:
    app.run(debug=True)


if __name__ == "__main__":
    main()
