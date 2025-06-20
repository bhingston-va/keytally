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

## Building the app

```bash
make build
```
```bash
make install-bin
```
```bash
make link-bin
```

## Running the app
### Tracking keystrokes in the background
```bash
nohup kt track > output.log 2>&1 &
```

### Viewing stats
```bash
kt stats
```
```bash
kt stats --layout
```
```bash
kt stats --layout --heatmap
```
