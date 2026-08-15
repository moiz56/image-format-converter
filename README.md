# File COnverter

A simple file converter setup which watches over a folder and converts a file whenever it's renamed to a
different extension (e.g. `photo.png` -> `photo.jpg`). This is helpful when we want to convert the file into any format we want (v1.0 only supports formats which are readable by PIL)

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

## Configuration

Set in `.env` (see `.env.example`):

- `WATCH_FOLDER` - folder to watch. Defaults to `~/Pictures`.
- `WATCH_RECURSIVE` - watch subfolders too (`true`/`false`). Defaults to `false`.

## Run

```bash
file-watcher
```

(or `python -m file_watcher.app`). Press `Ctrl+C` to stop.

## Tests

```bash
pytest tests/ -v
```

## Logs

Logs go to stdout and `file_watcher.log`, including timing and file
size for each conversion.

## Supported conversions

Any conversion Pillow can do (see `src/file_watcher/conversions.py`).

## V1.0

For the base version the flow is very simple, it supports 1 conversion at a time. Watchdog reads over a folder as specificed in the env file and whenever a supported rename is registered we activate the conversion script which just uses PIL's built in save method, also had detailed logging into time taken , and size of file changed after conversion

Limitations:

1. PIL does not support read for some types like .pdf so code might crash whenever we reach there
2. The conversion is not atomic, the image.save method opens the file_path for writing , if we reach an error over here a conversion which the OS might not support we lose the file no backup added
