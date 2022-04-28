from flask import Blueprint

bp_api = Blueprint("api", __name__)


def init_app(app):


    app.register_blueprint(bp_api)
