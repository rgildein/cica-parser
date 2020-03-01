import logging
import sys

MESSAGE_FORMAT = "%(asctime)s.%(msecs)03d: %(levelname)-6s@%(name)-15s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def set_up_logger(debug: bool = False):
    # set up global logger
    logger = logging.getLogger("")
    logger.setLevel(logging.INFO if not debug else logging.DEBUG)
    logger.handlers = []  # remove default handlers

    # set up STDERR handler
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(logging.Formatter(MESSAGE_FORMAT, datefmt=DATE_FORMAT))
    logger.addHandler(stderr_handler)

    return logger
