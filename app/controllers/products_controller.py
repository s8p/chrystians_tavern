from http import HTTPStatus
from flask import jsonify, current_app, request
from app.models import ProductModel, ProductOrderModel
from app.services.products_services import (
    check_keys,
    verify_product,
    check_category,
    verify_data,
 
    
)

from sqlalchemy.exc import IntegrityError
from app.exceptions.product_exc import InvalidValues, ProductNotFound, WrongKeys
from psycopg2.errors import UniqueViolation

from sqlalchemy.orm.session import Session
from app.configs.database import db


def create_product():
    data = request.get_json()

    try:
        data = verify_data(data)
        check_category(data)

        product = ProductModel(**data)

        session: Session = db.session

        session.add(product)
        session.commit()

    except IntegrityError as i:

        if isinstance(i.orig, UniqueViolation):
            return {"error": "Produto já registrado na database."}, HTTPStatus.CONFLICT

        else:
            raise i.orig

    except WrongKeys:
        return {"error": "Chaves erradas"}, HTTPStatus.BAD_REQUEST

    except InvalidValues:
        return {"error": "Formato de valor inválido"}, HTTPStatus.BAD_REQUEST

    return jsonify(product), HTTPStatus.CREATED


def retrieve_products():
    products = ProductModel.query.all()

    return jsonify(products), HTTPStatus.OK


def product_by_id(product_id: int):
    try:
        produto = verify_product(product_id)

    except ProductNotFound:
        return {"error": "Produto não encontrado"}, HTTPStatus.NOT_FOUND

    return jsonify(produto), HTTPStatus.OK


def update_product(product_id: int):
    try:
        product = verify_product(product_id)

        data = request.get_json()

        data = check_keys(data)
        check_category(data)

        session: Session = db.session

        for key, value in data.items():
            setattr(product, key, value)

        session.commit()

        return jsonify(product), HTTPStatus.OK

    except ProductNotFound:
        return {"error": "Produto não encontrado"}, HTTPStatus.NOT_FOUND

    except InvalidValues:
        return {"error": "Formato de valor inválido"}, HTTPStatus.BAD_REQUEST

    except WrongKeys:
        return {"error": "Chaves erradas"}, HTTPStatus.BAD_REQUEST

    except IntegrityError as i:

        if isinstance(i.orig, UniqueViolation):
            return {"error": "Produto já registrado na database."}, HTTPStatus.CONFLICT

        else:
            raise i.orig


def delete_product(product_id: int):
    session: Session = db.session
    all_product_order = session.query(ProductOrderModel).all()
    if all_product_order:
        for product_order in all_product_order:
            session.delete(product_order)
            session.commit()
    try:
        produto = verify_product(product_id)
        session.delete(produto)
        session.commit()
    except ProductNotFound:
        return {"error": f"Produto {product_id} não encontrado"}, HTTPStatus.NOT_FOUND
    return "", HTTPStatus.NO_CONTENT 
