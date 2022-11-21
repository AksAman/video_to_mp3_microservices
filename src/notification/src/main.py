import os
import sys

from settings import Settings
from consumer import Consumer
import logging
from models.message import Message
from utils import email_utils

logging.basicConfig(level=logging.INFO)


def exit_gracefully():
    logging.info("Exiting gracefully")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


def main():
    settings = Settings()

    def send_email_callback(message: Message) -> bool:
        args = email_utils.Mp3EmailArgs(
            sender=settings.SENDER_EMAIL,
            recipient=message.email,
            url=message.mp3_url(settings.GATEWAY_DOWNLOAD_ENDPOINT),
            subject="Your mp3 is ready!",
            name=message.username,
        )

        return email_utils.send_email(
            email_args=args,
            smtp_port=settings.SMTP_PORT,
            smtp_host=settings.SMTP_HOST,
        )

    try:
        consumer = Consumer(settings=settings)
        consumer.register_callback(send_email_callback)
        consumer.start_consuming()
    except KeyboardInterrupt:
        logging.error("Interrupted by user, shutting down")
        consumer.stop_consuming()
        exit_gracefully()
    except Exception as e:
        logging.exception(e)
        exit_gracefully()


if __name__ == "__main__":
    main()
