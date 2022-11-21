from settings import Settings
from utils.email_utils import send_email, Mp3EmailArgs
from models.message import Message

settings = Settings()


def send_email_callback(message: Message) -> bool:
    args = Mp3EmailArgs(
        sender=settings.SENDER_EMAIL,
        recipient=settings.SENDER_EMAIL,
        url=message.mp3_url(settings.GATEWAY_DOWNLOAD_ENDPOINT),
        subject="Your mp3 is ready!",
        name=message.username,
    )

    return send_email(
        email_args=args,
        smtp_port=settings.SMTP_PORT,
        smtp_host=settings.SMTP_HOST,
    )


if __name__ == "__main__":
    send_email_callback(
        Message(
            username="test",
            email=settings.SENDER_EMAIL,
            mp3_fid="test-mp3",
            video_fid="test-video",
        )
    )
