import logging
import sys
from datetime import datetime
from typing import Optional

MESSAGE_FORMAT = "%(asctime)s.%(msecs)03d: %(levelname)-6s@%(name)-15s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def set_up_logger(debug: bool = False, std: bool = False, log_file: Optional[str] = None):
    # set up global logger
    logger = logging.getLogger("")
    logger.setLevel(logging.INFO if not debug else logging.DEBUG)
    logger.handlers = []  # remove default handlers

    if std:
        # set up STDERR handler
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setFormatter(logging.Formatter(MESSAGE_FORMAT, datefmt=DATE_FORMAT))
        logger.addHandler(stderr_handler)

    # set up log file
    file_handler = logging.FileHandler(log_file or f"cica-{datetime.now():%Y%m%d-%H%M}.log", mode="w")
    file_handler.setFormatter(logging.Formatter(MESSAGE_FORMAT, datefmt=DATE_FORMAT))
    logger.addHandler(file_handler)

    return logger
