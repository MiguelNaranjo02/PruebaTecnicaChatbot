import sys
from loguru import logger
from pathlib import Path

def setup_logger(log_file: str | None = None, level: str = "INFO"):
    logger.remove()
    logger.add(sys.stderr, level=level)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        logger.add(log_file, level=level, rotation="1 week", retention="4 weeks")
    return logger