from flask_pymongo import PyMongo
import gridfs


mongo = PyMongo()
fs: gridfs.GridFS = None


def init_mongo(app):
    global fs
    mongo.init_app(app)
    fs = gridfs.GridFS(mongo.db)
