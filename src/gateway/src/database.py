from flask_pymongo import PyMongo
import gridfs


mongo = PyMongo()
fs = gridfs.GridFS(mongo.db)
