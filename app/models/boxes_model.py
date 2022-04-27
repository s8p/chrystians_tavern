from sqlalchemy import Column, Integer, String
from app.configs.database import db
from dataclasses import dataclass


@dataclass
class BoxesModel(db.Model):

    flag: str
    name: str
    description: str
    monthly_price: int

    __tablename__ = "boxes"

    flag = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    monthly_price = Column(Integer, nullable=False)
