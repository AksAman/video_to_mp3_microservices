# https://flask.palletsprojects.com/en/2.2.x/blueprints/#blueprints
from typing import List, Optional, Tuple
from flask import Blueprint, request, jsonify
from models import (
    ResultModel,
    ResultSchema,
)
from database import db
from sqlalchemy.orm import (
    Session,
)
from marshmallow import ValidationError


general_blueprint = Blueprint(name="general", import_name=__name__)


def validate_result_json(result_json: dict) -> Tuple[bool, List[str]]:
    try:
        return ResultSchema().load(result_json) is not None, None
    except ValidationError as e:
        return False, e.messages


@general_blueprint.route("/ping", methods=["GET"])
def ping():
    return "pong pong"


@general_blueprint.route("/results", methods=["GET"])
def results():
    return [r.to_dict() for r in ResultModel.query.all()]


@general_blueprint.route("/results/<int:id>", methods=["GET"])
def result(id: int):
    existing: Optional[ResultModel] = ResultModel.query.get(id)
    if existing:
        return existing.to_dict()
    else:
        return {"error": f"Result with id:{id} Not found"}, 404


@general_blueprint.route("/results", methods=["POST"])
def create_result():
    try:
        valid, err_msgs = validate_result_json(request.json)
        if not valid:
            return err_msgs, 400
        new_result = ResultModel(name=request.json["name"])
        session: Session = db.session
        session.add(new_result)
        session.commit()
        return [r.to_dict() for r in ResultModel.query.all()]
    except Exception as e:
        return {"error": str(e)}, 500


@general_blueprint.route("/results/<int:id>", methods=["PUT"])
def update_result(id: int):
    try:
        existing: Optional[ResultModel] = ResultModel.query.get(id)
        if existing:
            existing.name = request.json["name"]
            session: Session = db.session
            session.commit()
            return existing.to_dict()
        else:
            return {"error": f"Result with id:{id} Not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500


@general_blueprint.route("/results/<int:id>", methods=["DELETE"])
def delete_result(id: int):
    existing = ResultModel.query.get(id)
    if existing:
        session: Session = db.session
        session.delete(existing)
        session.commit()
        return [r.to_dict() for r in ResultModel.query.all()]
    else:
        return {"error": f"Result with id:{id} Not found"}, 404
