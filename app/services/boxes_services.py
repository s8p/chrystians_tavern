from flask import request
from app.models.boxes_model import BoxesModel
from sqlalchemy.orm.session import Session
from app.configs.database import db


def add_box():
    data = request.get_json()

    box = BoxesModel(**data)

    session: Session = db.session()

    session.add(box)
    session.commit()
