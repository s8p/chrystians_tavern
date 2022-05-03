from http import HTTPStatus
from flask import request, jsonify, current_app
from app.services.products_services import get_product, post_product, verify_products


def create_product():
    produto = post_product()
    current_app.db.session.add(produto)
    current_app.db.session.commit()
    return jsonify(produto), HTTPStatus.CREATED


def retrieve_products():
    product = get_product()
    return jsonify(product), HTTPStatus.OK


def product_by_id(product_id):
    produto = verify_products(product_id)
    return jsonify(produto), HTTPStatus.OK


# def update_product(product_id):
#     produto_id = verify_products(product_id)

#     product_new = session.query(ProductModel).filter(ProductModel.id == produto_id).first()
#     current_app.db.session.add(product_new)
#     current_app.db.session.commit()

#     return {'atualizado':product_new}, HTTPStatus.CREATED


def delete_product(product_id):
    produto = verify_products(product_id)
    current_app.db.session.delete(produto)
    current_app.db.session.commit()
    return "", HTTPStatus.NO_CONTENT
