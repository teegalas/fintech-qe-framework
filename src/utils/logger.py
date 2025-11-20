"""
Central logging configuration used by API client and tests.
"""

import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger with console + file handlers.

    We guard against adding duplicate handlers so calling this
    multiple times with the same name is safe.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Console handler for quick feedback in the terminal.
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # File handler for later debugging and history.
    fh = logging.FileHandler(LOG_DIR / "tests.log")
    fh.setLevel(logging.INFO)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    ch.setFormatter(fmt)
    fh.setFormatter(fmt)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
