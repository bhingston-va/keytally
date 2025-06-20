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
<img width="220" alt="Screenshot 2025-06-20 at 3 52 23 AM" src="https://github.com/user-attachments/assets/7f8d5d83-38c5-493b-868b-227c9c27a2c7" />

```bash
kt stats --layout
```
<img width="632" alt="Screenshot 2025-06-20 at 3 52 41 AM" src="https://github.com/user-attachments/assets/2224ddb2-3fb0-4e94-be34-a6cde9ed60e5" />

```bash
kt stats --layout --heatmap
```
<img width="632" alt="Screenshot 2025-06-20 at 3 52 56 AM" src="https://github.com/user-attachments/assets/e48c4f66-8026-447f-b172-e179ca133ece" />
