import logging
from pathlib import Path

import redis as rd
from flask import Flask

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

PATH_TO_LOG_FILE = Path("/var/log/server.log")
REDIS = rd.Redis(host="redis", port=6379)
SERVER_PORT = 65432

from . import routes
from . import error_handlers
