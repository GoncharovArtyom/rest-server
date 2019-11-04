import redis as rd
from flask import Flask

from balancer import config

app = Flask(__name__)
redis = rd.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

from . import routes
