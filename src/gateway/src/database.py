import logging
from flask_pymongo import PyMongo
import gridfs


mongo_video = PyMongo()
mongo_mp3 = None
video_fs: gridfs.GridFS = None
mp3_fs: gridfs.GridFS = None


def init_mongo(app):
    logging.info("Initializing MongoDB")
    global video_fs, mp3_fs, mongo_mp3
    mongo_video.init_app(app)

    mongo_mp3 = PyMongo(app, uri=app.config["MONGO_MP3_URI"])
    video_fs = gridfs.GridFS(mongo_video.db)
    mp3_fs = gridfs.GridFS(mongo_mp3.db)
    logging.info(f"MongoDB initialized, {video_fs=}, {mongo_video.db=}, {mongo_video=}")
