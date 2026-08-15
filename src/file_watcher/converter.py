import logging
import time
from pathlib import Path

from PIL import Image

from file_watcher.conversions import get_output_format


logger = logging.getLogger(__name__)


def convert_file(
    file_path: Path,
    old_extension: str,
    new_extension: str,
):
    logger.info(
        "Converting %s: %s -> %s",
        file_path.name,
        old_extension,
        new_extension,
    )

    output_format = get_output_format(old_extension, new_extension)

    if output_format is None:
        logger.warning(
            "Unsupported conversion %s -> %s for %s, skipping",
            old_extension,
            new_extension,
            file_path.name,
        )
        return

    start_time = time.perf_counter()

    try:
        size_before = file_path.stat().st_size

        with Image.open(file_path) as image:
            actual_format = image.format

            logger.debug("Actual format: %s", actual_format)

            image.save(
                file_path,
                format=output_format,
            )

        with Image.open(file_path) as image:
            file_format = image.format

            logger.info(
                f'''File format after conversion is {file_format} '''
            )
            if file_format != output_format:
                raise ValueError(
                    f"Expected {output_format} after save, got {file_format}"
                )

        size_after = file_path.stat().st_size
        size_delta = size_after - size_before
        elapsed = time.perf_counter() - start_time

        logger.info(
            "Conversion complete: %s (%.3fs, size %d -> %d bytes, %+d bytes)",
            file_path,
            elapsed,
            size_before,
            size_after,
            size_delta,
        )

    except FileNotFoundError as error:
        elapsed = time.perf_counter() - start_time
        logger.error(
            "Conversion failed for %s after %.3fs: file not found (%s)",
            file_path,
            elapsed,
            error,
        )

    except Exception as error:
        elapsed = time.perf_counter() - start_time
        logger.exception(
            "Conversion failed for %s after %.3fs: %s",
            file_path,
            elapsed,
            error,
        )
