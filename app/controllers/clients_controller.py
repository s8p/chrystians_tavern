from http import HTTPStatus

from flask import jsonify, request
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from app.exceptions.client_exc import (
    ClientNotFound,
    DuplicateProduct,
    ProductNotFound,
    UnavailableProduct,
    WrongKeys,
    UndefinedQuantity,
    InvalidValues,
)


from app.models import ClientsModel, OrderModel
from app.configs.database import db
from app.services.clients_services import (
    checking_id,
    checking_keys,
    calculate_price,
    register_products_order,
    register_client_order,
    checking_duplicate,
    packing_products,
    update_data,
    verify_data,
    update_points,
)


def retrieve_clients():
    if request.mimetype != "application/json":
        return jsonify([client for client in ClientsModel.query.all()])
    data = request.get_json()
    email = data.get("email")
    if email is None:
        return {"error": "Email necessário"}
    client = (
        db.session().query(ClientsModel).filter(ClientsModel.email == email).first()
    )
    if client:
        return jsonify(client)
    return {"error": "Email não encontrado"}, 404


def create_client():
    data = request.get_json()

    try:
        data["name"].title()
        data = checking_keys(data)

        client = ClientsModel(**data)

        session: Session = db.session

        session.add(client)
        session.commit()

    except IntegrityError as i:

        if isinstance(i.orig, UniqueViolation):
            return {"error": "Cliente já registrado!"}, HTTPStatus.CONFLICT

        if isinstance(i.orig, ForeignKeyViolation):
            return {
                "error": "`box_flag` não encontrada!"
            }, HTTPStatus.UNPROCESSABLE_ENTITY
        else:
            raise i.orig

    except WrongKeys:
        return {"error": "Chaves erradas"}, HTTPStatus.BAD_REQUEST

    return jsonify(client), HTTPStatus.CREATED


def update_client(client_id: int):
    try:
        data = request.get_json()

        data = update_data(data)

        client = checking_id(client_id)

        session: Session = db.session

        for key, value in data.items():

            setattr(client, key, value)
            session.commit()

        return jsonify(client), HTTPStatus.OK

    except WrongKeys:
        return {"error": "Chaves erradas"}, HTTPStatus.BAD_REQUEST

    except InvalidValues:
        return {"error": "Formato de valor inválido"}, HTTPStatus.BAD_REQUEST

    except ClientNotFound:
        return {"error": "Cliente não encontrado"}, HTTPStatus.NOT_FOUND


def delete_client(client_id):
    session: Session = db.session
    try:
        client = checking_id(client_id)
        session.delete(client)
        session.commit()
        return "", HTTPStatus.NO_CONTENT
    except ClientNotFound:
        return {"error": "Cliente não encontrado"}


def create_checkout(client_id: int):
    try:
        data = request.get_json()

        data = verify_data(data)

        client = checking_id(client_id)

        session: Session = db.session

        all_buying_products = packing_products(data["products"])

        buying_products = checking_duplicate(all_buying_products)

        total_price = calculate_price(buying_products)

        client = update_points(client, total_price)

        order_data = {"price": total_price}
        order = OrderModel(**order_data)

        session.add(order)
        session.commit()

        register_products_order(buying_products, order.id)
        register_client_order(client_id, order.id)

        checkout = {
            "id": order.id,
            "client_cpf": client.cpf,
            "products": buying_products,
            "total_price": order.price,
            "date": order.date,
        }

        return checkout, HTTPStatus.OK

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

    except UndefinedQuantity:
        return {
            "error": "A quantidade deve ser um valor inteiro e maior que zero"
        }, HTTPStatus.BAD_REQUEST

    except WrongKeys:
        return {"error": "Chaves erradas"}, HTTPStatus.BAD_REQUEST

    except InvalidValues:
        return {"error": "Formato de valor inválido"}, HTTPStatus.BAD_REQUEST
