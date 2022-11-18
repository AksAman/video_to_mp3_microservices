import os
from flask import Flask
from database import init_mongo
from decouple import config

from views.auth_views import auth_bp
from views.file_views import files_bp

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
init_mongo(app=app)

app.register_blueprint(auth_bp, url_prefix="/auth/api/v1")
app.register_blueprint(files_bp, url_prefix="/files/api/v1")
hostname = os.environ.get("HOSTNAME") or os.environ.get("NAME") or "unknown"


@app.route("/")
def hello():
    return {
        "message": "home",
        "host": hostname,
    }


@app.route("/ping")
def ping():
    return {
        "message": "pong",
        "host": hostname,
    }


if __name__ == "__main__":
    print("Starting app")
    print(app.url_map)
    app.run(host="0.0.0.0", port=8080)
