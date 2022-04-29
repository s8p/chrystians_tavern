from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String
from dataclasses import dataclass


@dataclass
class ProductModel(db.Model):

    id: int
    name: str
    price: int
    available_amount: int
    flag: str
    category: str

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    available_amount = Column(Integer, nullable=False, default=0)
    flag = Column(String, ForeignKey("boxes.flag"))
    category = Column(String, ForeignKey("categories.name"))
    
