import logging

import gridfs
from pymongo import MongoClient
from pymongo.database import Database

from settings import Settings

logging.basicConfig(level=logging.INFO)


class MongoWrapper:
    client: MongoClient = None
    videos_db: Database = None
    mp3s_db: Database = None
    mp3s_fs: gridfs.GridFS = None
    videos_fs: gridfs.GridFS = None

    def __init__(self, config: Settings):
        self.config = config
        self.videos_client = MongoClient(self.config.MONGO_URI + f"/{self.config.VIDEO_DB}")
        self.mp3s_client = MongoClient(self.config.MONGO_URI + f"/{self.config.MP3_DB}")
        self.videos_db: Database = self.videos_client[self.config.VIDEO_DB]
        self.mp3s_db: Database = self.mp3s_client[self.config.MP3_DB]

        logging.info(f"Connected to {self.config.MONGO_URI}")
        logging.info(f"{self.config.VIDEO_DB=} database: {self.videos_db=}")
        logging.info(f"{self.config.MP3_DB=} database: {self.mp3s_db=}")

        self.videos_fs = gridfs.GridFS(self.videos_db)
        self.mp3s_fs = gridfs.GridFS(self.mp3s_db)
