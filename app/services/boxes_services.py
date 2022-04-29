from http import HTTPStatus
from flask import request
from app.models.boxes_model import BoxesModel
from sqlalchemy.orm.session import Session
from app.configs.database import db
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
