from flask import request, session
from sqlalchemy.orm.session import Session

from app.exceptions.client_exc import (
    DuplicateProduct,
    ClientNotFound,
    ProductNotFound,
    WrongKeys,
    UnavailableProduct,
)
from app.configs.database import db
from app.models import ClientsModel, ProductOrderModel, ClientOrderModel
from app.models.products_model import ProductModel


def checking_keys(data: dict):
    box_flag = data.get("box_flag")

    if not box_flag:
        data["box_flag"] = box_flag
    else:
        data["box_flag"] = box_flag.capitalize()

    data["total_points"] = 0

    data_keys = set(data.keys())

    default_keys = ["cpf", "name", "email", "box_flag", "total_points"]
    default_keys = set(default_keys)

    if data_keys != default_keys:
        raise WrongKeys

    return data


def checking_id(id: int):
    session: Session = db.session

    client = session.query(ClientsModel).get(id)

    if not client:
        raise ClientNotFound

    return client


def packing_products(products: list):
    session: Session = db.session

    all_buying_products = []

    for each_product in products:
        product = session.query(ProductModel).get(each_product["product_id"])

        if product == None:
            raise ProductNotFound

        product = product.__dict__

        product = {
            key: value for key, value in product.items() if key != "_sa_instance_state"
        }

        product["quantity"] = each_product["quantity"]

        all_buying_products.append(product)

    return all_buying_products


def checking_duplicate(products: list):
    product_id_list = [product["id"] for product in products]

    product_list_check = []

    for product_id in product_id_list:
        if product_id not in product_list_check:
            product_list_check.append(product_id)
        else:
            raise DuplicateProduct

    return products


def check_available_amount(products: list):
    for product in products:

        if product["available_amount"] < product["quantity"]:
            raise UnavailableProduct


def calculate_price(products: list):
    session: Session = db.session

    total_price = 0

    check_available_amount(products)

    for product in products:

        current_product = session.query(ProductModel).get(product["id"])

        remaining_products = current_product.available_amount - product["quantity"]

        setattr(current_product, "available_amount", remaining_products)
        session.commit()

        total_price += product["price"] * product["quantity"]

    return total_price


def register_products_order(products: list, order_id: int):
    session: Session = db.session

    for product in products:

        product_order_data = {
            "product_id": product["id"],
            "order_id": order_id,
            "amount": product["quantity"],
        }
        product_order = ProductOrderModel(**product_order_data)

        session.add(product_order)
        session.commit()


def register_client_order(client_id: int, order_id: int):
    session: Session = db.session

    client_order_data = {"client_id": client_id, "order_id": order_id}

    client_order = ClientOrderModel(**client_order_data)

    session.add(client_order)
    session.commit()
