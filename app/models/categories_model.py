from app.configs.database import db
from sqlalchemy import Column, String
from dataclasses import dataclass

@dataclass
class CategoriesModel(db.Model):

    name = str

    __tablename__ = "categories"

    name = Column(String, primary_key=True)
