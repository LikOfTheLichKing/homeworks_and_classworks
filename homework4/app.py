from flask import Flask
from pages.init import pages_blueprint
from api.init import api_blueprint

app = Flask(__name__)
app.register_blueprint(api_blueprint)
app.register_blueprint(pages_blueprint)

if __name__ == "__main__":
    app.run()
