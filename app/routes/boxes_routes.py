from flask import Blueprint

from app.controllers import boxes_controllers

bp = Blueprint("boxes", __name__, url_prefix="/boxes")


bp.post("")(boxes_controllers.create_box)
bp.get("")(boxes_controllers.retrieve_boxes)
bp.get("/<int:box_flag>")(boxes_controllers.retrieve_box_flag)
bp.patch("/<int:box_flag>")(boxes_controllers.update_box)
bp.delete("/<int:box_flag>")(boxes_controllers.delete_box)
