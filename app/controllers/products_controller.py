from http import HTTPStatus
from flask import jsonify, current_app, request
from app.models import ProductModel, CategoriesModel
from app.services.products_services import (
    get_product,
    post_product,
    verify_products,
    check_category,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from app.exceptions.product_exc import ProductNotFound
from psycopg2.errors import UniqueViolation

from sqlalchemy.orm.session import Session
from app.configs.database import db


def create_product():
    data = request.get_json()
    try:
        check_category(data)
        produto = post_product(data)
        current_app.db.session.add(produto)
        current_app.db.session.commit()

    except IntegrityError as i:
        if isinstance(i.orig, UniqueViolation):
            return {"error": "product already registered."}, HTTPStatus.CONFLICT
        else:
            raise i.orig
    # except UnmappedInstanceError:
    #     return jsonify({'error':'Invalid format.'})
    # except KeyError:
    #     return jsonify({'error':'missing parameters'})

    return jsonify(produto), HTTPStatus.CREATED


def retrieve_products():
    product = get_product()
    return jsonify(product), HTTPStatus.OK


def product_by_id(product_id):
    try:
        produto = verify_products(product_id)
    except ProductNotFound:
        return {"error": f"Product {product_id} not found"}, HTTPStatus.NOT_FOUND
    return jsonify(produto), HTTPStatus.OK


def update_product(product_id):

    data = request.get_json()

    check = ["name", "price", "category", "available_amount"]
    data_keys = data.keys()
    extra_product = [key for key in data_keys if key not in check]

    if len(data) == 0:
        return {
            "error": "Invalid keys",
            "invalid_keys": extra_product,
        }, HTTPStatus.BAD_REQUEST

    if len(extra_product) > 0:
        return {
            "error": "Invalid keys",
            "invalid_keys": extra_product,
        }, HTTPStatus.BAD_REQUEST

    session: Session = db.session
    produto = session.query(ProductModel).get(product_id)
    if type(data["category"]) and type(data["name"]) != str:
        return jsonify({"error": "Unexpected shape."})
    if type(data["price"]) and type(data["available_amount"]) != int:
        return jsonify({"error": "Unexpected shape"})
    if not produto:
        return {"error": f"Product {product_id} not found"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(produto, key, value)

    session.commit()
    return jsonify(produto), HTTPStatus.OK


def delete_product(product_id):
    try:
        produto = verify_products(product_id)
        current_app.db.session.delete(produto)
        current_app.db.session.commit()
    except ProductNotFound:
        return {"error": f"Product {product_id} not found"}, HTTPStatus.NOT_FOUND
    return "", HTTPStatus.NO_CONTENT
