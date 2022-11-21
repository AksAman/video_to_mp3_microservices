from decouple import config


class Settings:
    DEBUG: bool = config("DEBUG", default=False, cast=bool)
    MONGO_HOST: str = config("MONGO_HOST")
    MONGO_PORT: int = config("MONGO_PORT", default=27017, cast=int)
    MONGO_USERNAME: str = config("MONGO_USERNAME")
    MONGO_PASSWORD: str = config("MONGO_PASSWORD")
    MONGO_URI: str = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
    RABBITMQ_HOST: str = config("RABBITMQ_HOST", default="rabbitmq")

    VIDEO_DB: str = config("VIDEO_DB", default="videos")
    MP3_DB: str = config("MP3_DB", default="mp3s")
