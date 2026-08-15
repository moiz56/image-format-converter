"""Conversion format lookup — delegates entirely to Pillow.

Rather than hardcoding an allowlist of extension pairs, this asks Pillow
which formats it has registered. Any extension Pillow recognizes as a
readable format can be a source; any extension mapping to a format
Pillow has a save plugin for can be a target. New formats become
supported automatically the moment Pillow (or a plugin, e.g. for HEIF
or AVIF) registers them - no code changes needed here.
"""

from PIL import Image


Image.init()  # populate Image.registered_extensions() / Image.SAVE


def _normalize(extension: str) -> str:
    extension = extension.lower()
    return extension if extension.startswith(".") else f".{extension}"


def get_output_format(old_extension: str, new_extension: str):
    """Return the Pillow format string for a conversion, or None if unsupported."""
    old_extension = _normalize(old_extension)
    new_extension = _normalize(new_extension)

    if old_extension == new_extension:
        return None

    extensions = Image.registered_extensions()

    if old_extension not in extensions:
        return None

    output_format = extensions.get(new_extension)

    if output_format is None or output_format not in Image.SAVE:
        return None

    return output_format


def is_supported(old_extension: str, new_extension: str) -> bool:
    return get_output_format(old_extension, new_extension) is not None
