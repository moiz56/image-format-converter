"""Centralized logging configuration for the file watcher app."""

import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logging handlers/format.

    Call this once, from the entrypoint (app.py), before any other
    module-level logger is used.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("file_watcher.log", encoding="utf-8"),
        ],
    )
