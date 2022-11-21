import logging
import os
import sys
from dataclasses import dataclass
from settings import Settings

logging.basicConfig(level=logging.INFO)

from wrappers.pika_wrapper import PikamqWrapper
from wrappers.mongo_wrappers import MongoWrapper

config = Settings()


def main():
    try:
        mongo_wrapper = MongoWrapper(config)
        pika_wrapper = PikamqWrapper(config, mongo_wrapper)
        pika_wrapper.start_consuming_video()
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down")
        if pika_wrapper and hasattr(pika_wrapper, "stop_consuming"):
            pika_wrapper.stop_consuming()
        exit_gracefully()
    except Exception as e:
        print(f"Error: {e}")
        exit_gracefully()


def exit_gracefully():
    logging.info("Exiting gracefully")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


if __name__ == "__main__":
    main()
