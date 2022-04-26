from flask_migrate import Migrate


def init_app(app):
    Migrate(app=app, db=app.db, compare_type=True)
