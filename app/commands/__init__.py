from .populate_commands import populate_cli


def init_app(app):
    app.cli.add_command(populate_cli())
