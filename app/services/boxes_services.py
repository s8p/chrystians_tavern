from http import HTTPStatus
from flask import jsonify, request
from app.models.boxes_model import BoxesModel
from sqlalchemy.orm import Query
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm.session import Session
from app.configs.database import db
from werkzeug.exceptions import NotFound
import locale

locale.setlocale(locale.LC_MONETARY, "pt_BR.UTF-8")


def add_box():
    data = request.get_json()

    box = BoxesModel(**data)

    session: Session = db.session()

    session.add(box)
    session.commit()
    return box


def get_all_boxes():
    session: Session = db.session
    boxes = session.query(BoxesModel).all()
    adapted_boxes = []
    for boxe in boxes:
        adapted_box = dict(**boxe.__dict__)
        adapted_box.pop("_sa_instance_state")
        adapted_box.update({"monthly_price": locale.currency(boxe.monthly_price)})
        adapted_boxes.append(adapted_box)
    return adapted_boxes


def delelete_by_flag(box_flag):
    session: Session = db.session

    box = session.query(BoxesModel).get(box_flag)

    if not box:
        return {"error": "id not found"}, HTTPStatus.NOT_FOUND

    session.delete(box)
    session.commit()
    return "", HTTPStatus.NO_CONTENT


def get_one_box(box_flag):
    base_query: Query = db.session.query(BoxesModel)

    box_query: BaseQuery = base_query.filter_by(flag=box_flag)
    try:
        box = box_query.first_or_404(description="flag not found")
    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    return jsonify(box), HTTPStatus.OK


def update_by_flag(box_flag):
    data = request.get_json()
    data.pop("flag")

    session: Session = db.session

    box = session.query(BoxesModel).get(box_flag)

    if not box:
        return {"error": "id not found"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(box, key, value)

    session.commit()

    return jsonify(box)
