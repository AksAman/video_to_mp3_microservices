import logging
import pika
from decouple import config

pika_connection = pika.BlockingConnection(
    parameters=pika.ConnectionParameters(
        host=config("RABBITMQ_HOST"),
    )
)
