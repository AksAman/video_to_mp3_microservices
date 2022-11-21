from decouple import config


class Settings:
    DEBUG: bool = config("DEBUG", default=False, cast=bool)

    RABBITMQ_HOST: str = config("RABBITMQ_HOST", default="rabbitmq")
    RABBITMQ_PORT: int = config("RABBITMQ_PORT", default=5672, cast=int)

    MP3_QUEUE_NAME: str = config("MP3_QUEUE_NAME", default="mp3s")
    SENDER_EMAIL: str = config("SENDER_EMAIL", default="")

    SMTP_HOST: str = config("SMTP_HOST", default="")
    SMTP_PORT: int = config("SMTP_PORT", default=587, cast=int)

    GATEWAY_DOWNLOAD_ENDPOINT: str = config(
        "GATEWAY_DOWNLOAD_ENDPOINT", default="http://localhost:8000/files/api/v1/download"
    )
