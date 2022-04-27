from flask import Blueprint

from app.controllers import products_controller

bp = Blueprint('products', __name__, url_prefix='products')

bp.post('')(products_controller.create_product)
bp.get('')(products_controller.retrieve_products)
bp.get('/<int:product_id>')(products_controller.product_by_id)
bp.patch('/<int:product_id>')(products_controller.update_product)
bp.patch('/<int:product_id>')(products_controller.delete_product)
