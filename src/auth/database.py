from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
# https://flask-migrate.readthedocs.io/en/latest/

from models import *
