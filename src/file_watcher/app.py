import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv

from file_watcher.logger_config import setup_logging
from file_watcher.watcher import start_watching


DEFAULT_WATCH_FOLDER = Path.home() / "Pictures"


def main():
    load_dotenv()

    watch_folder = Path(os.getenv("WATCH_FOLDER", str(DEFAULT_WATCH_FOLDER)))
    watch_recursive = os.getenv("WATCH_RECURSIVE", "false").strip().lower() in (
        "1",
        "true",
        "yes",
    )

    setup_logging()
    logger = logging.getLogger(__name__)

    start_time = time.perf_counter()
    logger.info(
        "Watching: %s (recursive=%s)",
        watch_folder,
        watch_recursive,
    )

    try:
        start_watching(watch_folder, recursive=watch_recursive)

    except RuntimeError as error:
        logger.error("Failed to start watcher: %s", error)

    except Exception:
        logger.exception("Unexpected error while running file watcher")

    finally:
        elapsed = time.perf_counter() - start_time
        logger.info("File watcher stopped after %.3fs total runtime", elapsed)


if __name__ == "__main__":
    main()
