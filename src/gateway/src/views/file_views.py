from flask.blueprints import Blueprint
from auth_svc import access
from flask import request
from utils import file_utils
from pika_connection import pika_connection
from database import fs

files_bp = Blueprint("files", __name__)


@files_bp.route("/upload", methods=["POST"])
def upload():
    access_token, err = access.validate_token(request)
    if not access_token:
        return {"error": err[0]}, err[1]

    if not access_token.get("is_admin"):
        return {"error": "You don't have permission to upload files."}, 403

    if len(request.files) != 1:
        return {"error": "Exactly 1 files is required"}, 400
    file = list(request.files.values())[0]

    message, status_code = file_utils.upload(
        file=file,
        fs=fs,
        channel=pika_connection.channel(),
        token=access_token,
    )
    if status_code != 200:
        return {"error": message}, status_code

    return {"message": message}, 200


@files_bp.route("/download", methods=["GET"])
def download():
    pass
