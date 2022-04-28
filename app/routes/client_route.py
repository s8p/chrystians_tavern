from flask import Blueprint
from app.controllers import clients_controller

bp = Blueprint("clients", __name__, url_prefix="/clients")

bp.get("")(clients_controller.retrieve_clients)
bp.post("")(clients_controller.create_client)
bp.get("/<int:client_id>")(clients_controller.client_by_id)
bp.patch("/<int:client_id>")(clients_controller.update_client)
bp.delete("/<int:client_id>")(clients_controller.delete_client)
bp.post("/<int:client_id>/checkout")(clients_controller.create_checkout)
