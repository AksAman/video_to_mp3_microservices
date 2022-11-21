import json
import logging
from gridfs import GridFS
from pika.adapters.blocking_connection import BlockingChannel
from werkzeug.datastructures import FileStorage
import pika


def upload(file: FileStorage, fs: GridFS, channel: BlockingChannel, token: str) -> tuple[dict, int]:
    """
    Uploads a file to the database and sends a message to the RabbitMQ broker.
    """
    try:
        file_id = fs.put(file)
    except Exception as e:
        logging.exception(e)
        return {"error": str(e)}, 500

    try:
        message = {
            "video_fid": str(file_id),
            "mp3_fid": None,
            "username": token["username"],
        }
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent.value,
            ),
        )

        return {"message": "upload queued"}, 200
    except Exception as e:
        # cleanup
        fs.delete(file_id)
        logging.exception(e)
        return {"error": str(e)}, 500


def download():
    pass


def publish_message(message: dict, channel: BlockingChannel, token: dict):
    try:
        message["username"] = token["username"]
        channel.basic_publish(
            exchange="",
            routing_key="messages",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent.value,
            ),
        )
        return {"message": "message queued"}, 200
    except Exception as e:
        logging.exception(e)
        return {"error": str(e)}, 500
