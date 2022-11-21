import json
import logging

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from settings import Settings
from wrappers.mongo_wrappers import MongoWrapper
from models.message import Message
from convert import to_mp3

logging.basicConfig(level=logging.INFO)


class PikamqWrapper:
    def __init__(self, config: Settings, mongo_wrapper: MongoWrapper):
        self.config = config
        self.mongo_wrapper = mongo_wrapper
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.config.RABBITMQ_HOST))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=config.VIDEO_DB, durable=True)
        self.channel.queue_declare(queue=config.MP3_DB, durable=True)

    def start_consuming_video(self):
        self.channel.basic_consume(
            queue=self.config.VIDEO_DB,
            on_message_callback=self.callback_video,
        )

    def callback_video(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        try:
            message: Message = Message.from_dict(json.loads(body))
            to_mp3.convert_to_mp3(
                message=message,
                videos_fs=self.mongo_wrapper.videos_fs,
                mp3_fs=self.mongo_wrapper.mp3s_fs,
                pika_channel=self.channel,
                mp3_queue=self.config.MP3_DB,
            )
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.exception(e)
            channel.basic_nack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.start_consuming()
        print("Waiting for messages. To exit press CTRL+C")

    def stop_consuming(self):
        self.channel.stop_consuming()
