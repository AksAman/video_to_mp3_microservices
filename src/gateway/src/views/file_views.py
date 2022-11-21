import logging
from flask.blueprints import Blueprint
from auth_svc import access
from flask import request
from utils import file_utils
from pika_connection import pika_connection
from database import video_fs, mp3_fs
from decouple import config
from bson.objectid import ObjectId
from flask import send_file


try:
    channel = pika_connection.channel()
    channel.queue_declare(queue=config("MONGO_DBNAME", "videos"), durable=True)
    channel.queue_declare(queue="messages", durable=True)
except Exception as e:
    logging.exception(e)
    channel = None

print(f"file-views {video_fs=}")

files_bp = Blueprint("files", __name__)


@files_bp.route("publish", methods=["POST"])
def publish():
    try:
        access_token, err = access.validate_token(request)
        if not access_token:
            return {"error": err[0]}, err[1]

        message, status_code = file_utils.publish_message(
            message=request.get_json(),
            channel=channel,
            token=access_token,
        )
        if status_code != 200:
            return {"error": message}, status_code

        return {"message": message}, 200
    except Exception as e:
        logging.exception(e)
        return {"error": "Internal server error"}, 500


@files_bp.route("/upload", methods=["POST"])
def upload():
    try:
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
            fs=video_fs,
            channel=channel,
            token=access_token,
        )
        if status_code != 200:
            return {"error": message}, status_code

        return {"message": message}, 200
    except Exception as e:
        logging.exception(e)
        return {"error": "Internal server error"}, 500


@files_bp.route("/download/<mp3_id>", methods=["GET"])
def download(mp3_id):
    try:
        # access_token, err = access.validate_token(request)
        # if not access_token:
        #     return {"error": err[0]}, err[1]

        # if not access_token.get("is_admin"):
        #     return {"error": "You don't have permission to download files."}, 403

        mp3_file = mp3_fs.get(ObjectId(mp3_id))
        if not mp3_file:
            return {"error": "File not found"}, 404

        return send_file(
            mp3_file,
            download_name=f"{mp3_id}.mp3",
        )
    except Exception as e:
        logging.exception(e)
        return {"error": "Internal server error"}, 500
