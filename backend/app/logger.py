import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "hospital_chatbot.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logger = logging.getLogger("hospital_chatbot")
logger.setLevel(logging.INFO)

# Formato de log
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# Log a consola
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Log a archivo con rotación (5MB, 5 backups)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5)
file_handler.setFormatter(formatter)

# Evitar handlers duplicados
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
