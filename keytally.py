import json
import threading
import time
import signal
import sys
import argparse
from pynput import keyboard
from collections import Counter
from colorama import Fore, Style, init as colorama_init

DATA_FILE = "key_counts.json"
SAVE_INTERVAL = 5  # seconds

def show_stats_layout(key_counts, heatmap=False):
    colorama_init()

    layout = [
        ['Esc', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
        ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
        ['LCtrl', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'Enter'],
        ['LShift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'RShift'],
        ['Fn1', 'LAlt', 'LCmd', 'Space', 'RAlt', '`', 'Fn2', 'Fn1'],
    ]
    label_map = {
        'Backspace': '←',
        'LAlt': '⎇',
        'LCmd': '⌘',
        'Esc': '⎋',
    }
    key_widths = {
        'Backspace': 2,
        'Tab': 1.5,
        '\\': 1.5,
        'LCtrl': 1.8,
        'Enter': 2.4,
        'LShift': 2.4,
        'RShift': 3,
        'Fn1': 1.35,
        'LAlt': 1.35,
        'LCmd': 1.35,
        'RAlt': 1.35,
        'Space': 7.75,
        '`': 1.35,
        'Fn2': 1.35,
    }

    max_val = max(key_counts.values()) if key_counts else 1

    def color_for_freq(freq):
        if not heatmap:
            return Style.RESET_ALL
        ratio = freq / max_val
        if ratio > 0.66:
            return Fore.RED
        elif ratio > 0.33:
            return Fore.YELLOW
        elif ratio > 0:
            return Fore.GREEN
        else:
            return Style.RESET_ALL

    def normalize_key(k):
        return {
            'space': 'Key.space',
            'ctrl': 'Key.ctrl_l',
            'lctrl': 'Key.ctrl_l',
            'rctrl': 'Key.ctrl_r',
            'alt': 'Key.alt_l',
            'lalt': 'Key.alt_l',
            'ralt': 'Key.alt_r',
            'cmd': 'Key.cmd',
            'lcmd': 'Key.cmd',
            'rcmd': 'Key.cmd_r',
            'shift': 'Key.shift',
            'lshift': 'Key.shift',
            'rshift': 'Key.shift_r',
            'enter': 'Key.enter',
            'tab': 'Key.tab',
            'esc': 'Key.esc',
            'backspace': 'Key.backspace',
            'fn1': 'Fn1',
            'fn2': 'Fn2',
        }.get(k.lower(), k.lower())

    def cell_content(label, width, color):
        pad = width - len(label)
        left = pad // 2
        right = pad - left
        return f"│{color}{' ' * left}{label}{' ' * right}{Style.RESET_ALL}"

    def print_row(row):
        widths = [int(round(4 * key_widths.get(k, 1))) for k in row]

        top = "┌" + "┬".join("─" * w for w in widths) + "┐"

        labels = []
        for k, w in zip(row, widths):
            label = label_map.get(k, k)
            key_id = normalize_key(k)
            color = color_for_freq(key_counts.get(key_id, 0))
            labels.append(cell_content(label, w, color))
        mid = "".join(labels) + "│"

        counts = []
        for k, w in zip(row, widths):
            key_id = normalize_key(k)
            count_str = str(key_counts.get(key_id, 0))
            color = color_for_freq(key_counts.get(key_id, 0))
            counts.append(cell_content(count_str, w, color))
        num = "".join(counts) + "│"

        bot = "└" + "┴".join("─" * w for w in widths) + "┘"

        print(top)
        print(mid)
        print(num)
        print(bot)

    print("\n🎹 Keyboard Layout (60%) Stats" + (" — Heatmap\n" if heatmap else "\n"))
    for row in layout:
        print_row(row)


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

    def show_stats_layout(self, counts, heatmap=False):
        show_stats_layout(counts, heatmap=heatmap)


def main():
    parser = argparse.ArgumentParser(description="KeyTally - Track and view keyboard usage.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("track", help="Start tracking keyboard usage")

    stats_parser = subparsers.add_parser("stats", help="Show current key stats")
    stats_parser.add_argument("-n", "--top", type=int, help="Show top N keys only")
    stats_parser.add_argument("--layout", action="store_true", help="Show keyboard layout view")
    stats_parser.add_argument("--heatmap", action="store_true", help="Color keys by usage")

    args = parser.parse_args()
    kt = KeyTally()

    if args.command == "track":
        kt.start_tracking()
    elif args.command == "stats":
        if args.layout:
            kt.show_stats_layout(kt.key_counts, heatmap=args.heatmap)
        else:
            kt.show_stats(top_n=args.top)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

