import json
import threading
import time
import signal
import sys
from pynput import keyboard

DATA_FILE = "key_counts.json"
SAVE_INTERVAL = 5  # seconds

class KeyTally:
    def __init__(self):
        self.key_counts = {}
        self.lock = threading.Lock()
        self.running = True
        self.load_counts()

    def load_counts(self):
        try:
            with open(DATA_FILE, "r") as f:
                self.key_counts = json.load(f)
            print(f"Loaded counts from {DATA_FILE}")
        except (FileNotFoundError, json.JSONDecodeError):
            self.key_counts = {}
            print(f"No existing data found. Starting fresh.")

    def save_counts(self):
        with self.lock:
            with open(DATA_FILE, "w") as f:
                json.dump(self.key_counts, f, indent=2)
            print(f"Saved counts to {DATA_FILE}")

    def on_press(self, key):
        try:
            k = key.char.lower() if hasattr(key, 'char') and key.char else str(key)
        except Exception:
            k = str(key)
        with self.lock:
            self.key_counts[k] = self.key_counts.get(k, 0) + 1

    def periodic_save(self):
        while self.running:
            time.sleep(SAVE_INTERVAL)
            self.save_counts()

    def start(self):
        # Handle graceful exit
        def signal_handler(sig, frame):
            print("\nCaught exit signal, saving data...")
            self.running = False
            self.save_counts()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Start periodic saving thread
        t = threading.Thread(target=self.periodic_save, daemon=True)
        t.start()

        # Start keyboard listener (blocking)
        with keyboard.Listener(on_press=self.on_press) as listener:
            print("KeyTally running. Press Ctrl+C to stop.")
            listener.join()

if __name__ == "__main__":
    kt = KeyTally()
    kt.start()

