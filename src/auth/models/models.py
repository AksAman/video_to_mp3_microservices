from models.base_models import BaseModel
import sqlalchemy as sa
from marshmallow import Schema, fields, validate


# https://docs.sqlalchemy.org/en/14/orm/quickstart.html#declare-models


class ResultModel(BaseModel):
    __tablename__ = "results"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(80), nullable=False)

    _default_fields = [
        "name",
    ]


class ResultSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(1))

    class Meta:
        ordered = True
