from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

logger.add(
    "logs/{time:YYYY-MM-DD_HH-mm-ss}.log",
    level="DEBUG",
    rotation="10 MB"
)