import os, json
from flask import Flask
from database import mongo
from decouple import config

from views.auth_views import auth_bp
from views.file_views import files_bp

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

app.register_blueprint(auth_bp, url_prefix="/auth/api/v1")
app.register_blueprint(files_bp, url_prefix="/files/api/v1")

mongo.init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
