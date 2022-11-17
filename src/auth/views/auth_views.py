# https://flask.palletsprojects.com/en/2.2.x/blueprints/#blueprints
import logging
from typing import List, Tuple

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from database import db
from models import User, UserRegisterSchema
from models.setters import (
    create_user,
)
from models.selectors import (
    get_user_by_username,
)
from utils.jwt_utils import (
    createJWT,
    validateJWT,
)

auth_blueprint = Blueprint(name="auth", import_name=__name__)


@auth_blueprint.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return jsonify({"message": "missing credentials"}), 401

    username = auth.username
    password = auth.password

    if not username or not password:
        return jsonify({"message": "missing credentials"}), 401

    existing_user: User = User.query.filter_by(username=username).first()
    if not existing_user:
        return jsonify({"message": "user not found"}), 404

    if not existing_user.verify_password(password):
        return jsonify({"message": "invalid password"}), 401

    return jsonify({"access": createJWT(user=existing_user)}), 200


@auth_blueprint.route("/register", methods=["POST"])
def register():
    def validate_user_json(user_json: dict) -> Tuple[list | dict, List[str]]:
        try:
            return UserRegisterSchema().load(user_json), None
        except ValidationError as e:
            return None, e.messages

    try:
        user_from_schema, err_msgs = validate_user_json(request.json)
        if not user_from_schema:
            return {"error": err_msgs}, 400
        username = user_from_schema["username"]
        exiting_user = get_user_by_username(username)
        if exiting_user:
            return {"error": f"User with username:{username} already exists"}, 400
        new_user, error_message = create_user(
            username=username,
            raw_password=user_from_schema.get("password"),
            email=user_from_schema.get("email"),
            first_name=user_from_schema.get("first_name"),
            last_name=user_from_schema.get("last_name"),
            is_admin=user_from_schema.get("is_admin", False),
        )
        if not new_user:
            return {"error": error_message}, 500
        return new_user.to_dict(), 201
    except Exception as e:
        logging.exception(e)
        return {"error": str(e)}, 500


@auth_blueprint.route("/logout", methods=["POST"])
def logout():
    # TODO: implement logout properly
    return jsonify({"message": "logout successful"}), 200


@auth_blueprint.route("/validate-token", methods=["POST"])
def validate_token():
    try:
        auth_header = request.headers.get("Authorization")
        try:
            auth_type, auth_info = auth_header.split(None, 1)
            auth_type = auth_type.lower()
        except ValueError:
            return {"error": "missing token"}, 400

        if auth_type != "bearer":
            return {"error": "invalid token type"}, 400

        decoded_token, error_message = validateJWT(token=auth_info)
        if error_message:
            return {"error": error_message}, 401

        return {
            "message": "token is valid",
            "user": decoded_token,
        }, 200
    except Exception as e:
        logging.exception(e)
        return {"error": str(e)}, 500
