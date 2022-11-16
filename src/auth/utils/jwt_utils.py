import logging
from typing import Tuple
import jwt
from models import User
from config import Config
from datetime import datetime, timedelta, timezone

active_config = Config()


SIGNING_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME = timedelta(minutes=30)


def createJWT(user: User) -> str:
    return jwt.encode(
        payload={
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin,
            "iat": datetime.now(tz=timezone.utc),
            "exp": datetime.now(tz=timezone.utc) + JWT_EXPIRATION_TIME,
        },
        key=active_config.JWT_SECRET,
        algorithm=SIGNING_ALGORITHM,
    )


def validateJWT(token: str) -> Tuple[dict, str]:
    try:
        return (
            jwt.decode(
                jwt=token,
                key=active_config.JWT_SECRET,
                algorithms=[SIGNING_ALGORITHM],
            ),
            None,
        )
    except jwt.ExpiredSignatureError:
        return {}, "Token has expired"
    except jwt.InvalidTokenError as e:
        logging.exception(e)
        return {}, "Invalid token"
    except Exception as e:
        logging.exception(e)
        return {}, "Unknown error"
