from app.configs.database import db
from sqlalchemy.orm.session import Session

from app.models import BoxesModel, ProductModel
from app.exceptions.box_exc import WrongKeys, InvalidValues, BoxNotFound

import random


def verify_data(data: dict):

    data_keys = set(data.keys())

    default_keys = set(["name", "description", "flag", "monthly_price"])

    if data_keys != default_keys:
        raise WrongKeys

    for key in data_keys:

        if key == "name" or key == "description" or key == "flag":
            if type(data[key]) != str:
                raise InvalidValues

        elif key == "monthly_price":
            if type(data[key]) != int:
                raise InvalidValues

    data["name"] = data["name"].title()
    data["flag"] = data["flag"].capitalize()

    return data


def check_box(box_flag: str):
    box_flag = box_flag.capitalize()

    session: Session = db.session

    box = session.query(BoxesModel).get(box_flag)

    if not box:
        raise BoxNotFound

    return box


def random_products(box_flag: str):

    products = (
        db.session.query(ProductModel)
        .filter_by(flag=box_flag)
        .filter(ProductModel.available_amount > 0)
        .all()
    )

    random_products = []

    if len(products) > 3:

        for _ in range(3):
            random_number = random.randint(0, len(products) - 1)

            random_products.append(products.pop(random_number))

    else:

        random_products = products

    return random_products


def check_data(data: dict):

    default_keys = ["name", "description", "monthly_price"]
    data_keys = list(data.keys())

    for key in data_keys:

        if key not in default_keys:
            raise WrongKeys

        if key == "description" or key == "name":
            if type(data[key]) != str:
                raise InvalidValues

        if key == "monthly_price":
            if type(data[key]) != int:
                raise InvalidValues

    if data.get("name"):
        data["name"] = data["name"].title()

    return data
