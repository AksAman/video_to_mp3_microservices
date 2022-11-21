from dataclasses import dataclass, field
import json
from typing import Callable, List
import pika
from settings import Settings
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import logging
from models.message import Message


class CallbackException(Exception):
    def __init__(self, message: str, callback: Callable):
        super().__init__(message)
        self.callback = callback


@dataclass
class Consumer(object):
    settings: Settings

    queue_name: str = field(init=False)
    connection: pika.BlockingConnection = field(init=False)
    channel: BlockingChannel = field(init=False)

    def __post_init__(self):
        self.queue_name = self.settings.MP3_QUEUE_NAME
        self.init_pika_connection()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.setup_consumer()
        self.user_callbacks: List[Callable[[Message], bool]] = []

    def register_callback(self, callback):
        self.user_callbacks.append(callback)

    def init_pika_connection(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.settings.RABBITMQ_HOST,
                port=self.settings.RABBITMQ_PORT,
                heartbeat=600,
                blocked_connection_timeout=300,
            )
        )
        self.channel = self.connection.channel()

    def setup_consumer(self):
        if self.channel and isinstance(self.channel, BlockingChannel):
            self.channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self.mp3_callback,
            )

    def mp3_callback(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        logging.info(f"Received {body} from {self.queue_name}")

        if not self.user_callbacks:
            logging.error("No callbacks registered")
            channel.basic_nack(delivery_tag=method.delivery_tag)
            return

        try:
            message: Message = Message.from_dict(json.loads(body))
            logging.info(f"Message: {message}, {method.delivery_tag=}")
            for callback in self.user_callbacks:
                success = callback(message)
                if not success:
                    raise CallbackException(
                        f"Error processing message: {message}, while processing {callback}", callback
                    )
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except CallbackException as e:
            logging.exception(e)
            channel.basic_nack(delivery_tag=method.delivery_tag)
        except ValueError as e:
            logging.error(f"Error parsing message: {e}")
            logging.exception(e)
            channel.basic_nack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.exception(e)
            channel.basic_nack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()
