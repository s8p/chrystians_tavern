from http import HTTPStatus

from flask import jsonify, request
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from app.exceptions.client_exc import WrongKeys

from app.models import ClientsModel
from app.configs.database import db
from app.services.clients_services import checking_id, checking_keys


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
    print("-" * 100)

    # print(client_id)

    client = checking_id(client_id)
    print(client)

    print("-" * 100)
    return {"msg": "create checkout"}, HTTPStatus.OK
