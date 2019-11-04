import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from server import config

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
db = SQLAlchemy(app)

from . import routes
from . import error_handlers
from . import model
