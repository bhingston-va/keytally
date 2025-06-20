import json
import threading
import time
import signal
import sys
import argparse
from pynput import keyboard
from collections import Counter

DATA_FILE = "key_counts.json"
SAVE_INTERVAL = 5  # seconds

class KeyTally:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.key_counts = {}
        self.lock = threading.Lock()
        self.running = True
        self.load_counts()

    def load_counts(self):
        try:
            with open(self.data_file, "r") as f:
                self.key_counts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.key_counts = {}

    def save_counts(self):
        with self.lock:
            with open(self.data_file, "w") as f:
                json.dump(self.key_counts, f, indent=2)

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

    def start_tracking(self):
        def signal_handler(sig, frame):
            print("\nCaught exit signal, saving data...")
            self.running = False
            self.save_counts()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        t = threading.Thread(target=self.periodic_save, daemon=True)
        t.start()

        with keyboard.Listener(on_press=self.on_press) as listener:
            print("KeyTally running. Press Ctrl+C to stop.")
            listener.join()

    def show_stats(self, top_n=None):
        if not self.key_counts:
            print("No data collected yet.")
            return
        sorted_keys = Counter(self.key_counts).most_common(top_n)
        print(f"{'Key':<15}Count")
        print("-" * 25)
        for key, count in sorted_keys:
            print(f"{key:<15}{count}")
        print(f"\nTotal unique keys: {len(self.key_counts)}")


def main():
    parser = argparse.ArgumentParser(description="KeyTally - Track and view keyboard usage.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("track", help="Start tracking keyboard usage")
    stats_parser = subparsers.add_parser("stats", help="Show current key stats")
    stats_parser.add_argument("-n", "--top", type=int, help="Show top N keys only")

    args = parser.parse_args()
    kt = KeyTally()

    if args.command == "track":
        kt.start_tracking()
    elif args.command == "stats":
        kt.show_stats(top_n=args.top)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

