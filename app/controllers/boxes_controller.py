from http import HTTPStatus
from flask import jsonify, request

from app.models.boxes_model import BoxesModel
from app.configs.database import db
from app.services.boxes_services import check_box, verify_data, random_products, check_data
from app.exceptions.product_exc import BoxNotFound, WrongKeys, InvalidValues

from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation



def create_box():
    try: 
        data = request.get_json()
        data = verify_data(data)

        box = BoxesModel(**data)

        session: Session = db.session()

        session.add(box)
        session.commit()
        
        return jsonify(box), HTTPStatus.CREATED

    except IntegrityError as i:

        if isinstance(i.orig, UniqueViolation):
            return {"error": "Box já registrada!"}, HTTPStatus.CONFLICT

        else:
            raise i.orig
    
    except WrongKeys:
        return {"error": "Chaves erradas"}, HTTPStatus.BAD_REQUEST
    
    except InvalidValues:
        return {"error": "Formato de valor inválido"}, HTTPStatus.BAD_REQUEST

    


def retrieve_boxes():
    session: Session = db.session

    boxes = session.query(BoxesModel).all()
    
    return jsonify(boxes), HTTPStatus.OK


def retrieve_box_flag(box_flag: str):
    try:
    
        box_flag = box_flag.capitalize()

        box = check_box(box_flag)

        products = random_products(box_flag)

        box = {key: value for key, value in box.__dict__.items() if key != '_sa_instance_state'}
        
        box['month_products'] = products

        return box, HTTPStatus.OK
    
    except BoxNotFound :
        return {"error": 'Box não encontrada'}, HTTPStatus.NOT_FOUND


def update_box(box_flag: str):
    data = request.get_json()

    data = check_data(data)

    session: Session = db.session

    try:
        box = check_box(box_flag)

        for key, value in data.items():
            setattr(box, key, value)

        session.commit()

        return jsonify(box), HTTPStatus.OK

    except BoxNotFound :
        return {"error": 'Box não encontrada'}, HTTPStatus.NOT_FOUND
    
    except WrongKeys:
        return {'error': 'Chaves Inválidas'}, HTTPStatus.BAD_REQUEST


def delete_box(box_flag: str):
    # session: Session = db.session

    # try:

    #     box = session.query(BoxesModel).get(box_flag)
    #     session.delete(box)
    #     session.commit()

    #     return "", HTTPStatus.NO_CONTENT

    # except BoxNotFound :
    #     return {"error": 'Box não encontrada'}, HTTPStatus.NOT_FOUND

    return {'loading': 'Rota em desenvolvimento'}, HTTPStatus.NOT_IMPLEMENTED
