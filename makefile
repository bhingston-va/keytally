# | Command            | What it does                                |
# | ------------------ | ------------------------------------------- |
# | `make`             | Set up venv, install deps, build the binary |
# | `make run`         | Run key tracker via Python in venv          |
# | `make stats`       | Show CLI stats                              |
# | `make clean`       | Remove build artifacts                      |
# | `make purge`       | Remove venv and build artifacts             |
# | `make install-bin` | Copy compiled binary to `/usr/local/bin/kt` |

# === CONFIG ===
APP_NAME = kt        # final binary name
ENTRYPOINT = keytally.py
VENV_DIR = venv
REQ_FILE = requirements.txt
DIST_DIR = dist
VERSION = $(shell cat VERSION)

# === DEFAULTS ===
.PHONY: all
all: build

# === SETUP ===

$(VENV_DIR)/bin/activate:
	python3.12 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r $(REQ_FILE)

install: $(VENV_DIR)/bin/activate
	@echo "✓ Virtualenv set up with dependencies."

# === BUILD ===

build: install
	@echo "🏗 Building standalone binary: $(APP_NAME) version $(VERSION)"
	sed "s/__version__ = \".*\"/__version__ = \"$(VERSION)\"/" $(ENTRYPOINT) > _tmp.py
	$(VENV_DIR)/bin/pyinstaller --onefile --name $(APP_NAME) _tmp.py
	rm _tmp.py

# === RUN ===

run:
	$(VENV_DIR)/bin/python $(ENTRYPOINT) track

stats:
	$(VENV_DIR)/bin/python $(ENTRYPOINT) stats

# === CLEANUP ===

clean:
	rm -rf build $(DIST_DIR) *.spec __pycache__ .pytest_cache

purge: clean
	rm -rf $(VENV_DIR)

# === INSTALL TO PATH ===

install-bin:
	cp $(DIST_DIR)/$(APP_NAME) /usr/local/bin/$(APP_NAME)
	@echo "✓ Installed $(APP_NAME) to /usr/local/bin"

