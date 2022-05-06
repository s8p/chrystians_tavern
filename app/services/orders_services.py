from sqlalchemy.orm.session import Session

from app.configs.database import db
from app.exceptions.order_exc import ClientNotFound
from app.models import ClientsModel

def checking_id(id: int):
    session: Session = db.session

    client = session.query(ClientsModel).get(id)

    if not client:
        raise ClientNotFound

    return client
