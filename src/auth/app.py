from flask_migrate import Migrate
from flask import Flask
from decouple import config
from database import db

from views import basic_views, auth_views

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
app.register_blueprint(blueprint=basic_views.general_blueprint, url_prefix="/general/api/v1")
app.register_blueprint(blueprint=auth_views.auth_blueprint, url_prefix="/auth/api/v1")


db.init_app(app)

# https://flask-migrate.readthedocs.io/en/latest/
migrate = Migrate(app, db)


if __name__ == "__main__":
    print(app.url_map)
    app.run(host="0.0.0.0", port=8000)
