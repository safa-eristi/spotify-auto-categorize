import os
import logging
import sys

from flask import Flask, jsonify

from flaskapp.config import config_by_name


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_by_name[test_config or 'test'])

    # logging configuration
    level_name = app.config['LOG_LEVEL']
    level = logging.getLevelName(level_name)
    formatter = logging.Formatter(
        '%(asctime)s | '
        '%(process)d | '
        '%(levelname)s | '
        '%(pathname)s | '
        '%(funcName)s | '
        '%(lineno)d | '
        '%(message)s'
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(level)

    @app.route("/health")
    def hello():
        return jsonify('healthy')

    import flaskapp.blueprints.oauth
    # apply the blueprints to the app
    app.register_blueprint(flaskapp.blueprints.oauth.bp, url_prefix='/oauth')

    from . import commands
    app.cli.add_command(commands.start)

    return app
