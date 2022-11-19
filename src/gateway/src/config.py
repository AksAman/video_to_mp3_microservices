from decouple import config


class Config:
    DEBUG = config("DEBUG", default=False, cast=bool)
    MONGO_HOST = config("MONGO_HOST")
    MONGO_PORT = config("MONGO_PORT", default=27017, cast=int)
    MONGO_DBNAME = config("MONGO_DBNAME")
    MONGO_USERNAME = config("MONGO_USERNAME")
    MONGO_PASSWORD = config("MONGO_PASSWORD")
    MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DBNAME}"
    RABBITMQ_HOST = config("RABBITMQ_HOST", default="rabbitmq")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
