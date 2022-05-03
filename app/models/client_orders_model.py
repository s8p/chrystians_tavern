from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer
from dataclasses import dataclass


@dataclass
class ClientOrderModel(db.Model):

    id: int
    order_id: int
    client_id: int

    __tablename__ = "client_orders"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
