import logging

from src.logging_config import setup_logging
from src.settings import settings

setup_logging()

logger = logging.getLogger(__name__)

logger.info(settings)
logger.info("Hello, world! This is a log message from the main module.")
