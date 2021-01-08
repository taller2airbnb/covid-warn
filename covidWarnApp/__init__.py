import logging
import os

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS

import covidWarnApp.commands
import covidWarnApp.database
import covidWarnApp.model
from covidWarnApp.api.home_info import bp_homeinfo
from covidWarnApp.api.params import bp_params


def create_app(my_config=None):
    # setup app
    app = Flask(__name__)
    # setup CORS
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    # setup with the configuration provided by the user / environment
    if my_config is None:
        app.config.from_object(os.environ['APP_SETTINGS'])
    else:
        app.config.from_object(my_config)
    # setup all our dependencies, for now only database using application factory pattern
    database.init_app(app)
    commands.init_app(app)

    CORS(bp_homeinfo)  # enable CORS on the bp_stinfo blue print
    CORS(bp_params)  # enable CORS on the bp_stinfo blue print

    @app.before_first_request
    def create_db():
        database.create_tables()
        model.insert_initial_values()

    app.register_blueprint(bp_homeinfo)
    app.register_blueprint(bp_params)

    # setup swagger
    swagger = Swagger(app)

    # setup logging
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.logger.info('New session started. Database up and running')

    return app
