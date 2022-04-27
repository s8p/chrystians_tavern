from datetime import datetime
from app.configs.database import db
from sqlalchemy import Column, Integer, DateTime
from dataclasses import dataclass
from datetime import datetime

@dataclass
class OrderModel(db.Model):

    data_atual = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
    
    id : int
    date : str
    price : int

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=data_atual)
    price = Column(Integer, nullable=False)