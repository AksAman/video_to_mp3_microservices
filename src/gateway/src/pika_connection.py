import logging
import pika
from decouple import config

try:
    pika_connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters(
            host=config("RABBITMQ_HOST"),
        )
    )
except Exception as e:
    logging.error(e)
    pika_connection = None
