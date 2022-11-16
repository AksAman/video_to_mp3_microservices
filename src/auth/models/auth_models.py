from models.base_models import BaseModel
import sqlalchemy as sa
from marshmallow import Schema, fields, validate
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)


class User(BaseModel):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(80), nullable=False, unique=True)
    password = sa.Column(sa.String(128), nullable=False)
    first_name = sa.Column(sa.String(80), nullable=False)
    last_name = sa.Column(sa.String(80), nullable=False)
    email = sa.Column(sa.String(80), nullable=False, unique=True)
    is_admin = sa.Column(sa.Boolean, default=False)

    _default_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_password(self.password)

    def set_password(self, password):
        self.password = generate_password_hash(password, method="pbkdf2:sha256:80000")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class UserRegisterSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(1))
    password = fields.String(required=True, validate=validate.Length(1))
    first_name = fields.String(required=True, validate=validate.Length(1))
    last_name = fields.String(required=True, validate=validate.Length(1))
    email = fields.String(required=True, validate=validate.Length(1))
    is_admin = fields.Boolean(required=False, default=False)

    class Meta:
        ordered = True
