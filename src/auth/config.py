from decouple import config


class Config:
    DEBUG = config("DEBUG", default=False, cast=bool)
    SQLALCHEMY_TRACK_MODIFICATIONS = config("SQLALCHEMY_TRACK_MODIFICATIONS", default=False, cast=bool)
    POSTGRES_SCHEMA = config("POSTGRES_SCHEMA")
    POSTGRES_USER = config("POSTGRES_USER")
    POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
    POSTGRES_HOST = config("POSTGRES_HOST")
    POSTGRES_PORT = config("POSTGRES_PORT")
    POSTGRES_DB = config("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI = (
        f"{POSTGRES_SCHEMA}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    JWT_SECRET: str = config("JWT_SECRET", default="")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
