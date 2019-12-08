import os
from pathlib import Path

SERVER0_URL = os.environ["SERVER0_URL"]
SERVER1_URL = os.environ["SERVER1_URL"]
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]

PATH_TO_LOG_CONFIG = Path(__file__).parent.parent / "logging.conf"
BALANCER_PORT = 65433
