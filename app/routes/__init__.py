from flask import Blueprint
from app.routes.boxes_routes import bp as bp_box


bp_api = Blueprint("api", __name__)


def init_app(app):

    bp_api.register_blueprint(bp_box)

    app.register_blueprint(bp_api)
