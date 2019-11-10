import os
from pathlib import Path

DATABASE_URL = os.environ["DATABASE_URL"]
PATH_TO_LOG_CONFIG = Path(__file__).parent.parent / "logging.conf"
SERVER_PORT = 65432
