from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from dataclasses import dataclass

from app.models.order_model import OrderModel
from app.models.products_model import ProductModel


@dataclass
class ProductOrderModel(db.Model):

    id: int
    product_id: ProductModel
    order_id: OrderModel
    amount: int

    __tablename__ = "product_orders"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Integer, default=1)
    productId = relationship("ProdutModel", backref=backref)
    orderId = relationship("OrderModel", backref=backref)
