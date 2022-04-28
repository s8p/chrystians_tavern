from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref
from dataclasses import dataclass
from app.models.boxes_model import BoxesModel
from app.models.categories_model import CategoriesModel


@dataclass
class ProductModel(db.Model):

    id: int
    name: str
    price: int
    available_amount: int
    flag: BoxesModel
    category: CategoriesModel

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    available_amount = Column(Integer, nullable=False, default=0)
    flag = Column(String, ForeignKey("box.flag"))
    category = Column(String, ForeignKey("categories.name"))
    flagId = relationship("BoxesModel", backref=backref("flag", uselist=False))
    categoryName = relationship(
        "CategoriesModel", backref=backref("category", uselist=False)
    )
