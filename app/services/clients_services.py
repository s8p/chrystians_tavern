from sqlalchemy.orm.session import Session

from app.exceptions.client_exc import IdNotFound, WrongKeys
from app.configs.database import db
from app.models import ClientsModel


def checking_keys(data: dict):
    box_flag = data.get("box_flag")

    if not box_flag:
        data["box_flag"] = box_flag
    else:
        data["box_flag"] = box_flag.capitalize()

    data["total_points"] = 0

    data_keys = set(data.keys())

    default_keys = ["cpf", "name", "email", "box_flag", "total_points"]
    default_keys = set(default_keys)

    if data_keys != default_keys:
        raise WrongKeys

    return data


def checking_id(id: int):
    session: Session = db.session

    client = session.query(ClientsModel).get(id)

    if not client:
        raise IdNotFound

    return client
