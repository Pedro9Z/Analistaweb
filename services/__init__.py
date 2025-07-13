import logging
from logging.handlers import RotatingFileHandler
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logger = logging.getLogger("analistaweb")
logger.setLevel(LOG_LEVEL)
if not logger.handlers:
    handler = RotatingFileHandler("analistaweb.log", maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
