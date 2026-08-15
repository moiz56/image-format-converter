import logging
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from converter import convert_file
from conversions import is_supported


logger = logging.getLogger(__name__)

executor = ThreadPoolExecutor(max_workers=4)


class RenameHandler(FileSystemEventHandler):

    def on_moved(self, event):
        start_time = time.perf_counter()

        try:
            if event.is_directory:
                return

            old_path = Path(event.src_path)
            new_path = Path(event.dest_path)

            old_ext = old_path.suffix.lower()
            new_ext = new_path.suffix.lower()

            if not old_ext or not new_ext:
                return

            if old_ext == new_ext:
                return

            if not is_supported(old_ext, new_ext):
                logger.debug(
                    "Unsupported conversion %s -> %s for %s, skipping",
                    old_ext,
                    new_ext,
                    new_path.name,
                )
                return

            logger.info(
                "Rename detected: %s -> %s",
                old_path.name,
                new_path.name,
            )

            executor.submit(
                convert_file,
                new_path,
                old_ext,
                new_ext,
            )

        except Exception:
            logger.exception(
                "Error handling rename event for %s",
                getattr(event, "src_path", "<unknown>"),
            )

        finally:
            elapsed = time.perf_counter() - start_time
            logger.debug("on_moved handled in %.6fs", elapsed)


def start_watching(folder: Path, recursive: bool = False):
    folder = folder.expanduser().resolve()

    if not folder.exists():
        raise RuntimeError(f"Folder does not exist: {folder}")

    handler = RenameHandler()
    observer = Observer()

    try:
        observer.schedule(
            handler,
            str(folder),
            recursive=recursive,
        )

        start_time = time.perf_counter()
        observer.start()
        elapsed = time.perf_counter() - start_time

        logger.info(
            "File observer is watching over %s (recursive=%s, startup took %.3fs)",
            folder,
            recursive,
            elapsed,
        )

        while True:
            observer.join(1)

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, stopping observer")
        observer.stop()

    except Exception:
        logger.exception("Unexpected error while watching %s", folder)
        observer.stop()
        raise

    finally:
        observer.join()
        logger.info("Observer stopped")
