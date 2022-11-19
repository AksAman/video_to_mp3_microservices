import logging
import pika
from decouple import config

print(f'{config("RABBITMQ_HOST")=}')

try:
    pika_connection = pika.BlockingConnection(
        parameters=pika.ConnectionParameters(
            host=config("RABBITMQ_HOST"),
        )
    )
except Exception as e:
    logging.exception(e)
    pika_connection = None
