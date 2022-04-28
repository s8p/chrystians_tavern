from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref, validates
from dataclasses import dataclass
from app.models.exc import CpfInvalid
from app.models.boxes_model import BoxesModel

@dataclass
class ClientsModel(db.Model):
   
    id : int
    cpf : str
    name : str
    email : str
    total_points : int
    box : BoxesModel


    __tablename__ = "clients"   

    id = Column(Integer, primary_key=True)
    cpf = Column(String(11), nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    total_points = Column(Integer)
    box_flag = Column(String, ForeignKey("boxes.flag"))
    box = relationship("BoxesModel", backref=backref("client", uselist=False))


    @validates("cpf")
    def validate_cpf(self, key, cpf):
        key = key.replace(".", "")
        key = key.replace("-","")

        if key.isnumeric() == False and len(key) != 11:
            raise CpfInvalid
        return key



