# === CONFIG ===
APP_NAME = kt        # final binary name
ENTRYPOINT = keytally.py
VENV_DIR = venv
REQ_FILE = requirements.txt
DIST_DIR = dist

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
	@echo "🏗 Building standalone binary: $(APP_NAME)"
	$(VENV_DIR)/bin/pyinstaller --onefile --name $(APP_NAME) $(ENTRYPOINT)

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

