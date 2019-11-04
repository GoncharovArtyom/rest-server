import os
from pathlib import Path

DATABASE_URL = os.environ["DATABASE_URL"]
PATH_TO_LOG_FILE = Path("/var/log/server.log")
SERVER_PORT = 65432
