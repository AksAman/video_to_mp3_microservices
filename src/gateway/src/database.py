import logging
from flask_pymongo import PyMongo
import gridfs


mongo = PyMongo()
fs: gridfs.GridFS = None


def init_mongo(app):
    logging.info("Initializing MongoDB")
    global fs
    mongo.init_app(app)
    fs = gridfs.GridFS(mongo.db)
    logging.info(f"MongoDB initialized, {fs=}, {mongo.db=}, {mongo=}")
