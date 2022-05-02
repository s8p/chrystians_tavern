from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import validates
from dataclasses import dataclass
from app.exceptions.client_exc import CpfInvalid


@dataclass
class ClientsModel(db.Model):

    id: int
    cpf: str
    name: str
    email: str
    total_points: int
    box_flag: str

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    cpf = Column(String(11), nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    total_points = Column(Integer)
    box_flag = Column(String, ForeignKey("boxes.flag"))

    @validates("cpf")
    def validate_cpf(self, key, cpf):
        cpf = str(cpf)
        
        cpf = cpf.replace(".", "")
        cpf = cpf.replace("-", "")

        if cpf.isnumeric() == False or len(cpf) != 11:
            raise CpfInvalid

        return cpf
