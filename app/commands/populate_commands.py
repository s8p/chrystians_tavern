import os
import random
from faker import Faker
from flask.cli import AppGroup
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
import click

from app.models.clients_model import ClientsModel
from app.configs.database import db


def populate_cli():
    fake = Faker("pt_BR")
    user_group = AppGroup("populate", help="Populates database")

    @user_group.command("clients")
    @click.argument("amount", type=int)
    def create_users(amount):
        session: Session = db.session
        clients = list()
        emails_used = list()
        cpf_used = list()
        print("Gerando Clientes")
        while len(clients) != amount:
            client = ClientsModel(
                name=fake.name(),
                email=fake.email(),
                cpf=fake.cpf(),
                total_points=random.randint(0, 10000),
                box_flag=random.choice(["Gold", "Silver", "Bronze", None]),
            )
            if client.email not in emails_used and client.cpf not in cpf_used:
                emails_used.append(client.email)
                cpf_used.append(client.cpf)
                clients.append(client)

        try:
            print("Salvando Clientes")
            session.add_all(clients)
            session.commit()
        except IntegrityError as e:
            if isinstance(e.orig, ForeignKeyViolation):
                print("Error: Chave estrangeira não existe")
                print(e.orig.args[0])
            if isinstance(e.orig, UniqueViolation):
                print("Error: Email ou CPF já existe na database.")
                print("Remova todos os clientes com o comando abaixo:")
                print(
                    f"\npsql -d {os.getenv('DATABASE_URI').split('/')[-1]} -c 'DELETE FROM {ClientsModel.__tablename__};'"
                )
            else:
                raise e.orig

    return user_group
