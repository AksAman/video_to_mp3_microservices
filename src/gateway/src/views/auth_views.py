from flask.blueprints import Blueprint
from auth_svc import access
from flask import request

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if not token:
        return {"error": err[0]}, err[1]

    return token, 200
