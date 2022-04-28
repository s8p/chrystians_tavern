from flask import Blueprint

from app.controllers import boxes_controller

bp = Blueprint("boxes", __name__, url_prefix="/boxes")


bp.post("")(boxes_controller.create_box)
bp.get("")(boxes_controller.retrieve_boxes)
bp.get("/<int:box_flag>")(boxes_controller.retrieve_box_flag)
bp.patch("/<int:box_flag>")(boxes_controller.update_box)
bp.delete("/<int:box_flag>")(boxes_controller.delete_box)
