import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv

from logger_config import setup_logging
from watcher import start_watching


load_dotenv()

DEFAULT_WATCH_FOLDER = Path.home() / "Pictures"

WATCH_FOLDER = Path(os.getenv("WATCH_FOLDER", str(DEFAULT_WATCH_FOLDER)))
WATCH_RECURSIVE = os.getenv("WATCH_RECURSIVE", "false").strip().lower() in (
    "1",
    "true",
    "yes",
)

setup_logging()
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    start_time = time.perf_counter()
    logger.info(
        "Watching: %s (recursive=%s)",
        WATCH_FOLDER,
        WATCH_RECURSIVE,
    )

    try:
        start_watching(WATCH_FOLDER, recursive=WATCH_RECURSIVE)

    except RuntimeError as error:
        logger.error("Failed to start watcher: %s", error)

    except Exception:
        logger.exception("Unexpected error while running file watcher")

    finally:
        elapsed = time.perf_counter() - start_time
        logger.info("File watcher stopped after %.3fs total runtime", elapsed)
