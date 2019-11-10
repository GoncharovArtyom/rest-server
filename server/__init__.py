import logging.config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from server import config

logging.config.fileConfig(config.PATH_TO_LOG_CONFIG)
werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.CRITICAL)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
db = SQLAlchemy(app)

from . import routes
from . import error_handlers
from . import model
