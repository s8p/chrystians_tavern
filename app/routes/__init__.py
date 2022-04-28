from flask import Blueprint
from product_route import bp as bp_product
from client_route import bp as bp_client
from boxes_route import bp as bp_box

bp_api = Blueprint("api", __name__)


def init_app(app):
    bp_api.register_blueprint(bp_client)
    bp_api.register_blueprint(bp_product)
    bp_api.register_blueprint(bp_box)
    app.register_blueprint(bp_api)
