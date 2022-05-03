from http import HTTPStatus
from random import random
from flask import jsonify, request
from app.models.boxes_model import BoxesModel
from app.models.products_model import ProductModel
from app.configs.database import db
from app.services import boxes_services
from sqlalchemy.orm import Query
from flask_sqlalchemy import BaseQuery
from werkzeug.exceptions import NotFound
from sqlalchemy.orm.session import Session


def create_box():
    data = request.get_json()

    box = BoxesModel(**data)

    session: Session = db.session()

    session.add(box)
    session.commit()
    return jsonify(box), HTTPStatus.CREATED


def retrieve_boxes():
    session: Session = db.session
    boxes = session.query(BoxesModel).all()
    adapted_boxes = []
    for boxe in boxes:
        adapted_box = dict(**boxe.__dict__)
        adapted_box.pop("_sa_instance_state")
        adapted_box.update({"monthly_price": boxe.monthly_price})
        adapted_boxes.append(adapted_box)
    return jsonify(adapted_boxes), HTTPStatus.OK


def retrieve_box_flag(box_flag: str):
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


def update_box(box_flag: str):
    data = request.get_json()
    data.pop("flag")

    session: Session = db.session

    try:
        box = session.query(BoxesModel).get(box_flag)
        for key, value in data.items():
            setattr(box, key, value)

        session.commit()

        return jsonify(box), HTTPStatus.OK

    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND


def delete_box(box_flag: str):
    session: Session = db.session

    try:

        box = session.query(BoxesModel).get(box_flag)
        session.delete(box)
        session.commit()

        return "", HTTPStatus.NO_CONTENT

    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND
