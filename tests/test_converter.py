import logging
import shutil
from pathlib import Path

import pytest
from PIL import Image

from file_watcher.converter import convert_file
from file_watcher.conversions import is_supported


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    "fixture_name",
    ["small.png", "photo_100kb.png", "photo_1mb.png", "photo_10mb.png"],
)
def test_png_to_jpeg_conversion_across_sizes(tmp_path, fixture_name):
    source = FIXTURES / fixture_name
    target = tmp_path / Path(fixture_name).with_suffix(".jpg").name
    shutil.copyfile(source, target)

    size_before = target.stat().st_size

    convert_file(target, ".png", ".jpg")

    assert target.exists()

    with Image.open(target) as image:
        assert image.format == "JPEG"

    size_after = target.stat().st_size
    assert size_after > 0
    assert size_after != size_before  # JPEG re-encoding changes the byte size


def test_unsupported_extension_is_skipped(tmp_path):
    source = FIXTURES / "small.png"
    target = tmp_path / "small.xyz"
    shutil.copyfile(source, target)

    assert not is_supported(".png", ".xyz")

    original_bytes = target.read_bytes()
    convert_file(target, ".png", ".xyz")

    # convert_file should have bailed out before touching the file
    assert target.read_bytes() == original_bytes


def test_corrupt_file_content_is_caught_not_raised(tmp_path, caplog):
    source = FIXTURES / "fake_image.png"
    target = tmp_path / "fake_image.jpg"
    shutil.copyfile(source, target)

    with caplog.at_level(logging.ERROR):
        convert_file(target, ".png", ".jpg")  # should not raise

    assert any("Conversion failed" in record.message for record in caplog.records)


def test_missing_file_is_caught_not_raised(tmp_path, caplog):
    missing = tmp_path / "does_not_exist.png"

    with caplog.at_level(logging.ERROR):
        convert_file(missing, ".png", ".jpg")  # should not raise

    assert any(
        "file not found" in record.message for record in caplog.records
    )


def test_unsupported_txt_extension_is_skipped(tmp_path):
    source = FIXTURES / "unsupported.txt"
    target = tmp_path / "unsupported.abc"
    shutil.copyfile(source, target)

    assert not is_supported(".txt", ".abc")

    original_bytes = target.read_bytes()
    convert_file(target, ".txt", ".abc")

    assert target.read_bytes() == original_bytes
