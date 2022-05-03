from http import HTTPStatus

from flask import jsonify, request
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from app.exceptions.client_exc import (
    ClientNotFound,
    DuplicateProduct,
    ProductNotFound,
    UnavailableProduct,
    WrongKeys,
)


from app.models import ClientsModel, ProductModel, OrderModel
from app.configs.database import db
from app.services.clients_services import (
    checking_id,
    checking_keys,
    calculate_price,
    register_products_order,
    register_client_order,
    checking_duplicate,
    packing_products,
)


def retrieve_clients():
    ...


def create_client():
    data = request.get_json()

    try:
        data = checking_keys(data)

        client = ClientsModel(**data)

        session: Session = db.session

        session.add(client)
        session.commit()

    except IntegrityError as i:

        if isinstance(i.orig, UniqueViolation):
            return {"error": "Cliente já registrado!"}, HTTPStatus.CONFLICT

        else:
            raise i.orig

    except WrongKeys:
        return {
            "error": "Confira as chaves usadas. Chaves esperadas: ['cpf', 'name', 'email', 'box_flag', 'total_points']"
        }, HTTPStatus.BAD_REQUEST

    return jsonify(client), HTTPStatus.CREATED


def client_by_id():
    ...


def update_client():
    ...


def delete_client():
    ...


def create_checkout(client_id: int):
    try:

        data = request.get_json()

        client = checking_id(client_id)

        session: Session = db.session

        all_buying_products = packing_products(data["products"])

        buying_products = checking_duplicate(all_buying_products)

        total_price = calculate_price(buying_products)

        order_data = {"price": total_price}
        order = OrderModel(**order_data)

        session.add(order)
        session.commit()

        register_products_order(buying_products, order.id)
        register_client_order(client_id, order.id)

        return jsonify(client), HTTPStatus.OK

    except UnavailableProduct:
        return {
            "error": "Produto não disponível ou demanda excedente ao estoque"
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    except ClientNotFound:
        return {"error": "Cliente não encontrado, verifique o id"}, HTTPStatus.NOT_FOUND

    except DuplicateProduct:
        return {
            "error": "Produto pedido mais de uma vez na mesma compra, considere incrementar a quantidade"
        }, HTTPStatus.BAD_REQUEST

    except ProductNotFound:
        return {"error": "Produto pedido não encontrado"}, HTTPStatus.NOT_FOUND
