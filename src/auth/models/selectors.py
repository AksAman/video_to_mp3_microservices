import logging
from typing import Optional
from sqlalchemy.orm import Session
from database import db
from models import User


def get_user_by_username(username: str) -> Optional[User]:
    try:
        return User.query.filter_by(username=username).first()
    except Exception as e:
        logging.exception(e)
        return None
