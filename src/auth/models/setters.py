import logging
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from database import db
from models import User
from models.selectors import (
    get_user_by_username,
)


def create_user(
    username: str, raw_password: str, email: str, first_name: str, last_name: str, is_admin: bool = False
) -> Tuple[Optional[User], str]:
    try:
        exiting_user = get_user_by_username(username)
        if exiting_user:
            logging.error(f"User with username:{username} already exists")
            return None, f"User with username:{username} already exists"
        new_user: User = User(
            username=username,
            password=raw_password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
        )
        session: Session = db.session
        session.add(new_user)
        session.commit()
        return new_user, None
    except Exception as e:
        logging.exception(e)
        return None, "Something went wrong"
