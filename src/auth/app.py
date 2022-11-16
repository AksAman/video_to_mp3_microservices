from flask_migrate import Migrate
import jwt
from flask import Flask
from decouple import config
from database import db

from views import basic_views

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
app.register_blueprint(blueprint=basic_views.auth_blueprint, url_prefix="/api/v1")


db.init_app(app)

# https://flask-migrate.readthedocs.io/en/latest/
migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
