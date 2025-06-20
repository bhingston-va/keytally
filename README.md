# keytally
Heat map of keystrokes.

## Installation

This is a known compatibility issue between `pynput` and Python 3.13 on macOS (Darwin). `pynput` does not yet support Python 3.13, and the error occurs due to changes in the threading internals.
```bash
python3.12 -m venv venv
```
```bash
source venv/bin/activate
```
```bash
pip install pyinstaller
```
```bash
pip install -r requirements.txt
```

## Running the app
```bash
nohup python keytally.py > output.log 2>&1 &
```
