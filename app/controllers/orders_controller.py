from http import HTTPStatus
from flask import jsonify

from app.configs.database import db
from app.models import OrderModel, ClientOrderModel, ProductOrderModel, ProductModel
from app.exceptions.order_exc import ClientNotFound

from sqlalchemy.orm.session import Session

from app.services.orders_services import checking_id


def get_orders():
    session: Session = db.session

    orders = session.query(OrderModel).all()

    return jsonify(orders), HTTPStatus.OK


def get_order_by_client_id(client_id: int):
    try:
        session: Session = db.session

        checking_id(client_id)

        client_orders = (
            session.query(ClientOrderModel).filter_by(client_id=client_id).all()
        )
        all_client_orders = []

        for order in client_orders:
            products = []

            product_orders = (
                session.query(ProductOrderModel).filter_by(order_id=order.id).all()
            )
            each_order = session.query(OrderModel).get(order.id)

            for product_order in product_orders:
                product = session.query(ProductModel).get(product_order.product_id)
                products.append(product)

            single_order = {
                "id": each_order.id,
                "date": each_order.date,
                "price": each_order.price,
                "products": products,
            }

            all_client_orders.append(single_order)

        return jsonify(all_client_orders), HTTPStatus.OK

    except ClientNotFound:
        return {"error": "Cliente não encontrado!"}, HTTPStatus.NOT_FOUND
