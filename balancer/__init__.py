import redis as rd
import logging.config
from flask import Flask

from balancer import config

logging.config.fileConfig(config.PATH_TO_LOG_CONFIG)

app = Flask(__name__)
redis = rd.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

from . import routes
