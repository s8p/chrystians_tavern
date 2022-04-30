from http import HTTPStatus
from flask import jsonify, request
from app.models.boxes_model import BoxesModel
from sqlalchemy.orm import Query
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm.session import Session
from app.configs.database import db
from werkzeug.exceptions import NotFound
import locale
import random

from app.models.products_model import ProductModel

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


def delete_by_flag(box_flag):
    session: Session = db.session

    box = session.query(BoxesModel).get(box_flag)

    if not box:
        return {"error": "flag not found"}, HTTPStatus.NOT_FOUND

    session.delete(box)
    session.commit()
    return "", HTTPStatus.NO_CONTENT


def get_one_box(box_flag):
    base_query: Query = db.session.query(BoxesModel)
    box_query: BaseQuery = base_query.filter_by(flag=box_flag)
    try:
        box = box_query.first_or_404(description="flag not found")
        products = db.session.query(ProductModel).filter_by(flag=box_flag).all()
        random_products = []
        if len(products) > 3:
            for _ in range(3):
                random_number = round(random.random() * (len(products) - 1))
                random_products.append(products.pop(random_number))
        else:
            random_products = products
        setattr(box, "sorted_products", random_products)
        return jsonify(box), HTTPStatus.OK
    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND


def update_by_flag(box_flag):
    data = request.get_json()
    data.pop("flag")

    session: Session = db.session

    box = session.query(BoxesModel).get(box_flag)

    if not box:
        return {"error": "flag not found"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(box, key, value)

    session.commit()

    return jsonify(box)
