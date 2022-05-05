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
    def validate_cpf(self, _, cpf):
        cpf = str(cpf)

        cpf = cpf.replace(".", "")
        cpf = cpf.replace("-", "")

        if not cpf.isnumeric() or len(cpf) != 11:
            raise CpfInvalid

        return cpf

    @validates("name", "email")
    def validates_name_email(self, key, value):
        if value is None or not isinstance(value, str):
            raise TypeError
        if key == "name":
            return value.title()
        return value.lower()

    @validates("box_flag")
    def validate_box_flag(self, _, box_flag):
        if box_flag is not None:
            if not isinstance(box_flag, str):
                return TypeError
            return box_flag.capitalize()
