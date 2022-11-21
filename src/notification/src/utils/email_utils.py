from dataclasses import dataclass
import email
import logging
import smtplib
from decouple import config
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


email_plain_template = """
Hi {name},

Your video has been converted to mp3 and is ready for download!
Copy the link below and paste it in your browser to download the file.
{link}
"""

email_html_template = """\
<html>
  <body>
    <p>Hi {name},<br>
       Your video has been converted to mp3 and is ready for download!<br>
         <a href="{url}">Click to Download</a>
    </p>
  </body>
</html>
"""


@dataclass
class Mp3EmailArgs:
    sender: str
    recipient: str
    subject: str
    name: str
    url: str


def send_email(email_args: Mp3EmailArgs, smtp_port: int = 465, smtp_host: str = "smtp.gmail.com") -> bool:
    """
    returns True if email was sent successfully
    """
    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            sender = email_args.sender
            recipient = email_args.recipient
            server.login(sender, config("SENDER_PASSWORD"))

            message = MIMEMultipart("alternative")
            message["Subject"] = email_args.subject
            message["From"] = sender
            message["To"] = recipient

            plain_message = MIMEText(email_plain_template.format(name=email_args.name, link=email_args.url), "plain")
            html_message = MIMEText(email_html_template.format(name=email_args.name, url=email_args.url), "html")

            message.attach(plain_message)
            message.attach(html_message)

            server.sendmail(sender, recipient, message.as_string())
            return True
    except Exception as e:
        logging.exception(e)
        return False
