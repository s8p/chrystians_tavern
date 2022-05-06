from flask import Blueprint

from app.controllers import orders_controller

bp = Blueprint("orders", __name__, url_prefix="/orders")


bp.get("")(orders_controller.get_orders)
bp.get("/client/<int:client_id>")(orders_controller.get_order_by_client_id)
